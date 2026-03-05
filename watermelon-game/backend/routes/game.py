"""Game configuration API routes."""

from fastapi import APIRouter
from backend.models import GameConfig, FruitConfig

router = APIRouter(prefix="/api/game", tags=["game"])

FRUITS = [
    FruitConfig(name="Cherry", emoji="\U0001f352", radius=15, color="#e74c3c", points=1),
    FruitConfig(name="Strawberry", emoji="\U0001f353", radius=20, color="#e91e63", points=3),
    FruitConfig(name="Grape", emoji="\U0001f347", radius=25, color="#9b59b6", points=6),
    FruitConfig(name="Orange", emoji="\U0001f34a", radius=32, color="#f39c12", points=10),
    FruitConfig(name="Peach", emoji="\U0001f351", radius=40, color="#fd79a8", points=15),
    FruitConfig(name="Apple", emoji="\U0001f34e", radius=47, color="#e74c3c", points=21),
    FruitConfig(name="Pear", emoji="\U0001f350", radius=55, color="#a8e06c", points=28),
    FruitConfig(name="Pineapple", emoji="\U0001f34d", radius=65, color="#fdcb6e", points=36),
    FruitConfig(name="Melon", emoji="\U0001f348", radius=75, color="#00b894", points=45),
    FruitConfig(name="Watermelon", emoji="\U0001f349", radius=90, color="#27ae60", points=55),
]


@router.get("/config", response_model=GameConfig)
async def get_game_config() -> GameConfig:
    """Return the game configuration including fruit list and board settings."""
    return GameConfig(
        fruits=FRUITS,
        board_width=400,
        board_height=700,
        gravity=1.5,
    )
