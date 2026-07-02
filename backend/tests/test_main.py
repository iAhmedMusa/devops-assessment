import uuid

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


@pytest.mark.asyncio
async def test_patch_with_same_value_does_not_bump_updated_at(client):
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
    profile_id = created["id"]

    patch_response = await client.patch(
        f"/api/profiles/{profile_id}", json={"fullName": "Ada Lovelace"}
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["updatedAt"] == created["updatedAt"]


@pytest.mark.asyncio
async def test_patch_with_explicit_null_clears_optional_field(client):
    payload = {
        "fullName": "Ada Lovelace",
        "email": "ada@example.com",
        "phoneNumber": "123456789",
        "country": "UK",
        "isActive": True,
    }
    create_response = await client.post("/api/profiles", json=payload)
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    patch_response = await client.patch(
        f"/api/profiles/{profile_id}", json={"phoneNumber": None}
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["phoneNumber"] is None


@pytest.mark.asyncio
async def test_patch_with_different_value_bumps_updated_at(client):
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
    profile_id = created["id"]

    patch_response = await client.patch(
        f"/api/profiles/{profile_id}", json={"fullName": "Grace Hopper"}
    )
    assert patch_response.status_code == 200
    assert patch_response.json()["updatedAt"] != created["updatedAt"]


@pytest.mark.asyncio
async def test_delete_profile_then_get_returns_404(client):
    payload = {
        "fullName": "Ada Lovelace",
        "email": "ada@example.com",
        "phoneNumber": "123456789",
        "country": "UK",
        "isActive": True,
    }
    create_response = await client.post("/api/profiles", json=payload)
    assert create_response.status_code == 201
    profile_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/profiles/{profile_id}")
    assert delete_response.status_code == 200

    get_response = await client.get(f"/api/profiles/{profile_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_get_patch_delete_nonexistent_profile_returns_404(client):
    missing_id = str(uuid.uuid4())

    get_response = await client.get(f"/api/profiles/{missing_id}")
    assert get_response.status_code == 404

    patch_response = await client.patch(
        f"/api/profiles/{missing_id}", json={"fullName": "Nobody"}
    )
    assert patch_response.status_code == 404

    delete_response = await client.delete(f"/api/profiles/{missing_id}")
    assert delete_response.status_code == 404
