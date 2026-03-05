"""Async SQLite database operations for the Watermelon game."""

import aiosqlite
import os
from datetime import datetime, timezone

DB_PATH = os.getenv("WATERMELON_DB_PATH", "watermelon_scores.db")


async def init_db() -> None:
    """Initialize the database and create tables if they don't exist."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.commit()


async def save_score(player_name: str, score: int) -> dict:
    """Save a score to the database and return the created record."""
    created_at = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO scores (player_name, score, created_at) VALUES (?, ?, ?)",
            (player_name, score, created_at),
        )
        await db.commit()
        return {
            "id": cursor.lastrowid,
            "player_name": player_name,
            "score": score,
            "created_at": created_at,
        }


async def get_leaderboard(limit: int = 10) -> list[dict]:
    """Get the top scores from the leaderboard, sorted by score descending."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, player_name, score, created_at FROM scores ORDER BY score DESC LIMIT ?",
            (limit,),
        )
        rows = await cursor.fetchall()
        return [
            {
                "id": row["id"],
                "player_name": row["player_name"],
                "score": row["score"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]
