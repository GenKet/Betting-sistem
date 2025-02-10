import pytest
from datetime import datetime, timedelta


@pytest.mark.asyncio
async def test_list_events(ac):
    event_data = {
        "id": 2,
        "odds": 1.75,
        "name": "England-Spain",
        "deadline": (datetime.utcnow() + timedelta(minutes=1)).isoformat()
    }
    await ac.post("/api/events/", json=event_data)
    response = await ac.get("/api/events/")
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == 2

@pytest.mark.asyncio
async def test_create_event(ac):
    event_data = {
        "id": 1,
        "odds": 2.50,
        "name": "England-Spain",
        "deadline": (datetime.utcnow() + timedelta(minutes=1)).isoformat()
    }
    response = await ac.post("/api/events/", json=event_data)

    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["id"] == 1
    assert data["odds"] == 2.5
    assert data["name"] == "England-Spain"
    assert data["status"] == "unfinished"



@pytest.mark.asyncio
async def test_update_event_status(ac):
    event_data = {
        "id": 3,
        "odds": 2.00,
        "name": "England-Spain",
        "deadline": (datetime.utcnow() + timedelta(minutes=1)).isoformat()
    }
    await ac.post("/api/events/", json=event_data)
    update_data = {"status": "team_1_win"}
    response = await ac.patch("/api/events/3/status/", json=update_data)
    assert response.status_code == 200, f"Response: {response.text}"
    data = response.json()
    assert data["id"] == 3
    assert data["status"] == "team_1_win"


@pytest.mark.asyncio
async def test_update_nonexistent_event(ac):
    update_data = {"status": "team_1_win"}
    response = await ac.patch("/api/events/999/status/", json=update_data)
    assert response.status_code == 404