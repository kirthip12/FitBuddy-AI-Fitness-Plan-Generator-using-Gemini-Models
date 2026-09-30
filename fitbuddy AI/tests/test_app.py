import os
from pathlib import Path


TEST_DB = Path("test_fitbuddy.db")


if TEST_DB.exists():

    TEST_DB.unlink()


os.environ[
    "DATABASE_URL"
] = (
    f"sqlite:///{TEST_DB.absolute()}"
)


os.environ.pop(
    "GEMINI_API_KEY",
    None
)


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def teardown_module():

    if TEST_DB.exists():

        TEST_DB.unlink()


def test_homepage():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_generate_workout():

    response = client.post(

        "/api/generate-workout",

        json={

            "name":
            "Arun",

            "user_id":
            "TEST1001",

            "age":
            21,

            "weight":
            68,

            "goal":
            "muscle gain",

            "intensity":
            "medium",

            "experience_level":
            "beginner"
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["mode"] == "demo"

    assert "DAY 1" in data["workout_plan"]

    assert data["nutrition_tip"]


def test_feedback():

    response = client.post(

        "/api/submit-feedback",

        json={

            "user_id":
            "TEST1001",

            "feedback":
            "Please add more cardio and one extra rest day."
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["mode"] == "demo"

    assert "DAY 1" in data["updated_plan"]


def test_users():

    response = client.get(
        "/api/users"
    )


    assert response.status_code == 200


    data = response.json()


    assert any(

        user["user_id"] ==
        "TEST1001"

        for user in data

    )