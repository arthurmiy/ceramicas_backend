from fastapi.testclient import TestClient
from sqlalchemy import StaticPool,create_engine
from sqlalchemy.orm import sessionmaker
from api.main import app, Base, get_db
import pytest

client = TestClient(app)

DATABASE_URL2 = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL2, 
    connect_args={
        "check_same_thread": False,
        },
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()

app.dependency_overrides[get_db] = override_get_db


def setup() -> None:
    print("Setting up)")
    # Create the tables in the test database
    Base.metadata.create_all(bind=engine)

setup()


def teardown() -> None:
    # Drop the tables in the test database
    Base.metadata.drop_all(bind=engine)



def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_create_item():
    response = client.post(
        "/items",json={"name": "Foo", "description": "A very nice Item"}
    )
    assert response.status_code == 200
    data=response.json()
    assert data["name"] == "Foo"
    assert data["description"] == "A very nice Item"
    assert "id" in data

def test_update_item():
    item_id = 1
    response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated Item", "description": "This is an updated item"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["description"] == "This is an updated item"
    assert data["id"] == item_id


def test_delete_item():
    item_id = 1
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == item_id
    # Try to get the deleted item
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404, response.text