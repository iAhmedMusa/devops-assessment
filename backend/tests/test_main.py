import pytest


@pytest.mark.asyncio
async def test_root_returns_running_message(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == "Application is running"


@pytest.mark.asyncio
async def test_health_returns_ok(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_create_and_get_profile(client):
    payload = {
        "fullName": "Ada Lovelace",
        "email": "ada@example.com",
        "phoneNumber": "123456789",
        "country": "UK",
        "isActive": True,
    }
    create_response = await client.post("/api/profiles", json=payload)
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["fullName"] == "Ada Lovelace"
    profile_id = created["id"]

    list_response = await client.get("/api/profiles")
    assert list_response.status_code == 200
    assert any(p["id"] == profile_id for p in list_response.json())

    get_response = await client.get(f"/api/profiles/{profile_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == "ada@example.com"
