# backend/app/routes/recommend.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.core.recommender import Recommender
from app.utils.helpers import load_place_data_from_csv
import os
import pathlib

router = APIRouter(prefix="/api/recommend", tags=["Recommendations"])

# # Initialize recommender with dataset (lazy load once)
# DATA_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "datasets", "place_data.csv")
# _places = load_place_data_from_csv(DATA_CSV)

# print(f"Loaded {_places and len(_places) or 0} places from CSV: {DATA_CSV}")

# Get absolute path to the root of the project
ROOT_DIR = pathlib.Path(__file__).resolve().parents[3]
DATA_CSV = os.path.join(ROOT_DIR, "datasets", "place_data.csv")

_places = load_place_data_from_csv(DATA_CSV)
print(f"📊 Loaded {len(_places)} places from: {DATA_CSV}")

recommender = Recommender(place_data=_places)


class PreferenceIn(BaseModel):
    user_id: str
    preferences: Dict

class RecommendRequest(BaseModel):
    query: Optional[str] = None
    group_preferences: Optional[List[PreferenceIn]] = None
    top_k: Optional[int] = 8


@router.post("/")
def recommend(req: RecommendRequest):
    """
    POST body example:
    {
      "query": "beach and seafood",
      "group_preferences": [
         {"user_id": "dev", "preferences": {"likes":["beach"], "budget_max":20000}}
      ],
      "top_k": 5
    }
    """
    gp = req.group_preferences or []
    # convert pydantic models to dicts (we expect "preferences" field present)
    gp_dicts = [p.dict() for p in gp]
    results = recommender.recommend(query=req.query, group_preferences=gp_dicts, top_k=req.top_k)
    return {"recommendations": results}
