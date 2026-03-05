"""Pydantic models for the Watermelon game."""

from datetime import datetime
from pydantic import BaseModel, Field


class ScoreCreate(BaseModel):
    """Model for creating a new score entry."""

    player_name: str = Field(..., min_length=1, max_length=50)
    score: int = Field(..., ge=0)


class ScoreResponse(BaseModel):
    """Model for score response with all fields."""

    id: int
    player_name: str
    score: int
    created_at: str


class FruitConfig(BaseModel):
    """Configuration for a single fruit type."""

    name: str
    emoji: str
    radius: int
    color: str
    points: int


class GameConfig(BaseModel):
    """Game configuration including fruit list and board settings."""

    fruits: list[FruitConfig]
    board_width: int = 400
    board_height: int = 700
    gravity: float = 1.5
