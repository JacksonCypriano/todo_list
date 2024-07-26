import pytest
from httpx import AsyncClient
from app.main import app
from app.database import Base, engine
from app import models
from redis import Redis

# Configurar o banco de dados para testes
@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def redis_client():
    return Redis(host='redis', port=6379, db=0)

@pytest.mark.asyncio
async def test_create_task(async_client, setup_database, redis_client):
    response = await async_client.post("/tasks/", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

@pytest.mark.asyncio
async def test_read_task(async_client, setup_database, redis_client):
    response = await async_client.get("/tasks/1")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_update_task(async_client, setup_database, redis_client):
    response = await async_client.put("/tasks/1", json={"title": "Updated Task", "description": "Updated Description", "completed": True})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_task(async_client, setup_database, redis_client):
    response = await async_client.delete("/tasks/1")
    assert response.status_code == 200