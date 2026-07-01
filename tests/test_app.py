from fastapi.testclient import TestClient

from src import app as app_module


client = TestClient(app_module.app)


def setup_function():
    app_module.activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["existing@mergington.edu"],
        }
    }


def test_duplicate_signup_returns_conflict():
    response = client.post(
        "/activities/Chess Club/signup?email=existing@mergington.edu"
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Student is already signed up for this activity"
    assert app_module.activities["Chess Club"]["participants"] == [
        "existing@mergington.edu"
    ]


def test_unregister_removes_participant():
    response = client.delete(
        "/activities/Chess Club/signup?email=existing@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed existing@mergington.edu from Chess Club"
    assert app_module.activities["Chess Club"]["participants"] == []
