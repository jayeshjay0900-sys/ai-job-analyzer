from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "AI Job Description Analyzer" in response.text


def test_short_job_description():

    response = client.post(
        "/analyze",
        json={
            "job_description": "Python developer"
        }
    )

    assert response.status_code == 422


def test_model():

    response = client.get(
        "/model"
    )

    assert response.status_code == 200

    data = response.json()

    assert "provider" in data
    assert "model" in data