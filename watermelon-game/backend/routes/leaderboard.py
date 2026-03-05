"""Leaderboard API routes."""

from fastapi import APIRouter
from backend.models import ScoreCreate, ScoreResponse
from backend.database import save_score, get_leaderboard

router = APIRouter(prefix="/api", tags=["leaderboard"])


@router.post("/scores", response_model=ScoreResponse)
async def create_score(score_data: ScoreCreate) -> ScoreResponse:
    """Save a new score to the leaderboard."""
    result = await save_score(score_data.player_name, score_data.score)
    return ScoreResponse(**result)


@router.get("/scores", response_model=list[ScoreResponse])
async def get_scores() -> list[ScoreResponse]:
    """Get the top 10 scores from the leaderboard."""
    results = await get_leaderboard(limit=10)
    return [ScoreResponse(**r) for r in results]
