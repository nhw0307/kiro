"""Tests for the leaderboard API endpoints."""

import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app
from backend.database import init_db

import os
import aiosqlite

TEST_DB_PATH = "test_watermelon_scores.db"


@pytest.fixture(autouse=True)
async def setup_test_db(monkeypatch):
    """Set up a fresh test database for each test."""
    monkeypatch.setenv("WATERMELON_DB_PATH", TEST_DB_PATH)
    # Patch the module-level DB_PATH in database module
    import backend.database as db_module
    monkeypatch.setattr(db_module, "DB_PATH", TEST_DB_PATH)

    await init_db()
    yield
    # Cleanup
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


@pytest.fixture
async def client():
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_post_score_success(client):
    """Test that posting a valid score returns 200 with the created score."""
    response = await client.post(
        "/api/scores",
        json={"player_name": "TestPlayer", "score": 1500},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["player_name"] == "TestPlayer"
    assert data["score"] == 1500
    assert "id" in data
    assert "created_at" in data


@pytest.mark.asyncio
async def test_post_score_missing_fields(client):
    """Test that posting with missing fields returns 422."""
    response = await client.post(
        "/api/scores",
        json={"player_name": "TestPlayer"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_scores_empty(client):
    """Test that GET /api/scores returns empty list when no scores exist."""
    response = await client.get("/api/scores")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_get_scores_returns_sorted_by_score_descending(client):
    """Test that leaderboard returns scores sorted highest first."""
    # Insert multiple scores
    scores = [
        {"player_name": "Alice", "score": 500},
        {"player_name": "Bob", "score": 2000},
        {"player_name": "Charlie", "score": 1000},
        {"player_name": "Diana", "score": 3000},
        {"player_name": "Eve", "score": 750},
    ]
    for s in scores:
        await client.post("/api/scores", json=s)

    response = await client.get("/api/scores")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 5
    # Verify descending order
    assert data[0]["player_name"] == "Diana"
    assert data[0]["score"] == 3000
    assert data[1]["player_name"] == "Bob"
    assert data[1]["score"] == 2000
    assert data[2]["player_name"] == "Charlie"
    assert data[2]["score"] == 1000
    assert data[3]["player_name"] == "Eve"
    assert data[3]["score"] == 750
    assert data[4]["player_name"] == "Alice"
    assert data[4]["score"] == 500


@pytest.mark.asyncio
async def test_get_scores_limited_to_10(client):
    """Test that leaderboard returns at most 10 results."""
    for i in range(15):
        await client.post(
            "/api/scores",
            json={"player_name": f"Player{i}", "score": i * 100},
        )

    response = await client.get("/api/scores")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 10
    # The top 10 should be players 14 down to 5 (highest scores)
    assert data[0]["score"] == 1400
    assert data[9]["score"] == 500


@pytest.mark.asyncio
async def test_get_game_config(client):
    """Test that game config endpoint returns valid configuration."""
    response = await client.get("/api/game/config")
    assert response.status_code == 200
    data = response.json()

    assert "fruits" in data
    assert "board_width" in data
    assert "board_height" in data
    assert "gravity" in data
    assert len(data["fruits"]) == 10
    # First fruit should be Cherry
    assert data["fruits"][0]["name"] == "Cherry"
    assert data["fruits"][0]["emoji"] == "\U0001f352"
    # Last fruit should be Watermelon
    assert data["fruits"][9]["name"] == "Watermelon"
    assert data["fruits"][9]["emoji"] == "\U0001f349"
