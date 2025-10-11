# backend/app/routes/plan.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
from app.core.nlp_engine import NLPEngine
from app.core.recommender import Recommender
from app.core.voting_system import VotingSystem
from app.utils.helpers import load_place_data_from_csv
import os, pathlib

router = APIRouter(prefix="/api/plan", tags=["Planner"])

# Initialize models
nlp_engine = NLPEngine()
voting_system = VotingSystem()

# Load places dataset
ROOT_DIR = pathlib.Path(__file__).resolve().parents[3]
DATA_CSV = os.path.join(ROOT_DIR, "datasets", "place_data.csv")
_places = load_place_data_from_csv(DATA_CSV)
recommender = Recommender(place_data=_places)

# Request models
class ChatInput(BaseModel):
    user_id: str
    message: str

class GroupPlanRequest(BaseModel):
    messages: List[ChatInput]
    top_k: int = 5


@router.post("/")
def generate_group_plan(req: GroupPlanRequest):
    """
    Full AI pipeline:
    1. NLP extract preferences from group chat
    2. Recommender suggests destinations
    3. VotingSystem ranks them for group satisfaction
    """
    print("🧠 Running AI pipeline for group plan...")

    # Step 1 → NLP extraction for each user
    group_preferences = []
    for msg in req.messages:
        prefs = nlp_engine.extract_preferences(msg.message)
        group_preferences.append({"user_id": msg.user_id, "preferences": prefs})

    # Step 2 → Generate candidate destinations
    all_likes = " ".join([",".join(p["preferences"].get("likes", [])) for p in group_preferences])
    recommendations = recommender.recommend(query=all_likes, group_preferences=group_preferences, top_k=req.top_k)

    # Step 3 → Weighted voting
    ranked = voting_system.weighted_vote(group_preferences, recommendations)

    return {
        "group_preferences": group_preferences,
        "recommended_places": recommendations,
        "final_ranking": ranked
    }
