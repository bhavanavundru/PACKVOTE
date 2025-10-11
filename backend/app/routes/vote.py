from fastapi import APIRouter
from typing import List, Dict
from pydantic import BaseModel

router = APIRouter(prefix="/api/vote", tags=["Voting"])

class Preference(BaseModel):
    user_id: str
    preferences: Dict

class Candidate(BaseModel):
    id: str
    tags: List[str]
    price: float

@router.post("/weighted")
def weighted_vote(prefs: List[Preference], candidates: List[Candidate]):
    def match_score(pref, candidate):
        score = 0
        for tag in candidate.tags:
            if tag in pref.get("likes", []): score += 1
            if tag in pref.get("dislikes", []): score -= 1
        if "budget_max" in pref and candidate.price > pref["budget_max"]:
            score -= (candidate.price - pref["budget_max"]) / pref["budget_max"]
        return score

    results = {}
    for c in candidates:
        total = sum(match_score(p.preferences, c) for p in prefs)
        results[c.id] = total

    ranked = sorted(results.items(), key=lambda x: x[1], reverse=True)
    return {"ranking": ranked}
