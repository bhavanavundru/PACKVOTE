from fastapi import APIRouter

router = APIRouter(prefix="/api/recommend", tags=["Recommendations"])

@router.get("/")
def recommend_places():
    # Will later connect with recommender.py
    sample_places = [
        {"name": "Goa Beach", "tags": ["beach", "relax"], "rating": 4.6},
        {"name": "Manali Hills", "tags": ["mountains", "snow"], "rating": 4.8},
        {"name": "Jaipur", "tags": ["heritage", "culture"], "rating": 4.5}
    ]
    return {"recommendations": sample_places}
