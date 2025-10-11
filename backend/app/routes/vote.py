from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.core.voting_system import VotingSystem

router = APIRouter(prefix="/api/vote", tags=["Voting"])

voting_system = VotingSystem()

# Pydantic schemas
class Preference(BaseModel):
    user_id: str
    preferences: Dict

class Candidate(BaseModel):
    id: str
    name: str
    tags: List[str]
    price: float
    rating: float

class VoteRequest(BaseModel):
    preferences: List[Preference]
    candidates: List[Candidate]


@router.post("/weighted")
def group_vote(data: VoteRequest):
    prefs = [p.dict() for p in data.preferences]
    candidates = [c.dict() for c in data.candidates]

    ranking = voting_system.weighted_vote(prefs, candidates)
    return {"ranking": ranking}
