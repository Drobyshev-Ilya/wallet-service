import os
import sys
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import asyncio
import platform

# Add the project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from app.database import Base, get_db

# Use environment variable to determine if we're testing locally
is_local = os.environ.get('LOCAL_TEST') == '1'
host = 'localhost' if is_local else 'db'

DATABASE_URL = f"postgresql+asyncpg://postgres:12345678@{host}:5432/test_wallet_db"

@pytest.fixture(scope="session")
def event_loop_policy():
    """Create an instance of the default event loop policy for the test session."""
    if platform.system() == 'Windows':
        return asyncio.WindowsSelectorEventLoopPolicy()
    return asyncio.get_event_loop_policy()

@pytest.fixture(autouse=True)
async def setup_database():
    """Create a fresh test database for each test."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield async_session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture
async def client(setup_database):
    """Create a test client with a fresh database session."""
    async def override_get_db():
        async with setup_database() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_create_wallet(client):
    response = await client.post("/api/v1/wallets")
    assert response.status_code == 200
    assert "id" in response.json()
    assert "balance" in response.json()
    assert response.json()["balance"] == "0.00"

@pytest.mark.asyncio
async def test_get_wallet_balance(client):
    # First create a wallet
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]
    
    # Then get its balance
    response = await client.get(f"/api/v1/wallets/{wallet_id}")
    assert response.status_code == 200
    assert response.json()["id"] == wallet_id
    assert response.json()["balance"] == "0.00"

@pytest.mark.asyncio
async def test_wallet_operations(client):
    # Create wallet
    create_response = await client.post("/api/v1/wallets")
    wallet_id = create_response.json()["id"]
    
    # Deposit
    deposit_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "DEPOSIT", "amount": "100.50"}
    )
    assert deposit_response.status_code == 200
    assert deposit_response.json()["balance"] == "100.50"
    
    # Withdraw
    withdraw_response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={"operation_type": "WITHDRAW", "amount": "50.25"}
    )
    assert withdraw_response.status_code == 200
    assert withdraw_response.json()["balance"] == "50.25"

@pytest.mark.asyncio
async def test_wallet_not_found(client):
    response = await client.get("/api/v1/wallets/nonexistent")
    assert response.status_code == 404