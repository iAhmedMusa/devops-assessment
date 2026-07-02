from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from datetime import datetime

MONGO_URI = os.getenv('MONGO_URI')
DB_NAME = os.getenv('DB_NAME')
FRONTEND_ORIGINS = os.getenv('FRONTEND_ORIGINS')

# DB client and collection are configured at startup using environment variables
client: Optional[AsyncIOMotorClient] = None
db = None
collection = None

app = FastAPI()

# Configure CORS middleware at import time (must be added before the app starts)
if not FRONTEND_ORIGINS:
    raise RuntimeError("Missing required environment variable: FRONTEND_ORIGINS")
origins = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]
if not origins:
    raise RuntimeError("FRONTEND_ORIGINS must contain at least one origin")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)


class UserProfileBase(BaseModel):
    fullName: str
    email: EmailStr
    phoneNumber: Optional[str] = None
    country: Optional[str] = None
    isActive: bool = True


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    fullName: Optional[str] = None
    email: Optional[EmailStr] = None
    phoneNumber: Optional[str] = None
    country: Optional[str] = None
    isActive: Optional[bool] = None


class UserProfileOut(UserProfileBase):
    id: str = Field(..., alias="_id")
    createdAt: datetime
    updatedAt: datetime

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: lambda v: str(v),
            datetime: lambda v: v.isoformat(),
        }


@app.on_event("startup")
async def startup_db_client():
    # Require env vars (no hardcoded fallbacks)
    missing = []
    for name, val in (("MONGO_URI", MONGO_URI), ("DB_NAME", DB_NAME)):
        if not val:
            missing.append(name)
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

    # Initialize DB client and collection
    global client, db, collection
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['user_profiles']

    # Warm DB connection (non-fatal if Mongo isn't reachable yet)
    try:
        await client.server_info()
    except Exception:
        # If Mongo isn't ready, we'll let runtime errors surface on DB ops instead of failing app startup
        pass


@app.post('/api/profiles', response_model=UserProfileOut, status_code=status.HTTP_201_CREATED)
async def create_profile(profile: UserProfileCreate):
    now = datetime.utcnow()
    payload = profile.dict()
    payload.update({"createdAt": now, "updatedAt": now})
    result = await collection.insert_one(payload)
    created = await collection.find_one({"_id": result.inserted_id})
    created['_id'] = str(created['_id'])
    return created


@app.get('/api/profiles', response_model=List[UserProfileOut])
async def list_profiles():
    cursor = collection.find().sort('createdAt', -1)
    profiles = []
    async for doc in cursor:
        doc['_id'] = str(doc['_id'])
        profiles.append(doc)
    return profiles


@app.get('/api/profiles/{profile_id}', response_model=UserProfileOut)
async def get_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=404, detail='Profile not found')
    profile = await collection.find_one({"_id": ObjectId(profile_id)})
    if not profile:
        raise HTTPException(status_code=404, detail='Profile not found')
    profile['_id'] = str(profile['_id'])
    return profile


@app.patch('/api/profiles/{profile_id}', response_model=UserProfileOut)
async def update_profile(profile_id: str, payload: UserProfileUpdate):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=404, detail='Profile not found')
    update_data = {k: v for k, v in payload.dict(exclude_unset=True).items() if v is not None}
    if update_data:
        update_data['updatedAt'] = datetime.utcnow()
        result = await collection.find_one_and_update(
            {"_id": ObjectId(profile_id)},
            {"$set": update_data},
            return_document=True,
        )
    else:
        result = await collection.find_one({"_id": ObjectId(profile_id)})

    if not result:
        raise HTTPException(status_code=404, detail='Profile not found')
    result['_id'] = str(result['_id'])
    return result


@app.delete('/api/profiles/{profile_id}', status_code=status.HTTP_200_OK)
async def delete_profile(profile_id: str):
    if not ObjectId.is_valid(profile_id):
        raise HTTPException(status_code=404, detail='Profile not found')
    res = await collection.delete_one({"_id": ObjectId(profile_id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail='Profile not found')
    return {"message": "Profile deleted successfully"}
