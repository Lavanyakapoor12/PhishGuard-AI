
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from backend.main import app, get_db
from backend.database import Base, engine


# Connect to the separate test database.
test_database_url = engine.url.set(
    database="phishguard_test_db"
)

test_engine = create_engine(test_database_url)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


# Set up and clean the test database.
@pytest.fixture(scope="session", autouse=True)
def setup_test_database():

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():

        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield

    app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=test_engine)

    test_engine.dispose()


@pytest.fixture
def client():

    with TestClient(app) as test_client:
        yield test_client


# NORMAL API TESTS

def test_home_endpoint(client):

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["status"] == "Backend is running"


def test_predict_valid_url(client):

    response = client.post(
        "/predict",
        json={"url": "https://www.google.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["prediction"] in ["Phishing", "Legitimate"]

    assert 0 <= data["phishing_probability"] <= 100

    assert data["id"] is not None


def test_predict_invalid_url(client):

    response = client.post(
        "/predict",
        json={"url": "not-a-valid-url"}
    )

    assert response.status_code == 422


def test_history_endpoint(client):

    response = client.get("/history")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_stats_endpoint(client):

    response = client.get("/stats")

    assert response.status_code == 200

    data = response.json()

    assert "total_scans" in data

    assert "phishing_detected" in data

    assert "legitimate_urls" in data

    assert "phishing_rate" in data


# SECURITY TESTS

def test_empty_url(client):

    response = client.post(
        "/predict",
        json={"url": ""}
    )

    assert response.status_code == 422


def test_missing_url(client):

    response = client.post(
        "/predict",
        json={}
    )

    assert response.status_code == 422


def test_javascript_url(client):

    response = client.post(
        "/predict",
        json={"url": "javascript:alert(1)"}
    )

    assert response.status_code == 422


def test_file_url(client):

    response = client.post(
        "/predict",
        json={"url": "file:///etc/passwd"}
    )

    assert response.status_code == 422


# URL LENGTH SECURITY TEST

def test_url_exceeding_maximum_length(client):

    long_url = "https://example.com/" + ("a" * 2048)

    response = client.post(
        "/predict",
        json={"url": long_url}
    )

    assert response.status_code == 422
