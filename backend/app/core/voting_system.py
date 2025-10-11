# backend/app/core/voting_system.py

from typing import List, Dict
import numpy as np

class VotingSystem:
    """
    Weighted AI Voting System for PACKVOTE.
    Combines group preferences, destination tags, price, and sentiment into one score.
    """

    def __init__(self):
        pass

    def weighted_vote(self, preferences: List[Dict], candidates: List[Dict]) -> List[Dict]:
        """
        Compute a weighted group ranking of all candidates.
        """
        results = []

        for c in candidates:
            candidate_score = 0
            user_count = 0

            for p in preferences:
                user_count += 1
                candidate_score += self._match_score(p["preferences"], c)

            avg_score = candidate_score / max(user_count, 1)
            results.append({
                "id": c.get("id"),
                "name": c.get("name"),
                "score": round(avg_score, 2)
            })

        # Sort descending by score
        ranked = sorted(results, key=lambda x: x["score"], reverse=True)
        return ranked


    def _match_score(self, pref: Dict, candidate: Dict) -> float:
        """
        Compute how well one candidate fits a single user's preferences.
        """
        score = 0

        likes = pref.get("likes", [])
        dislikes = pref.get("dislikes", [])
        budget_max = pref.get("budget_max")
        tone = pref.get("tone", "neutral")

        # Tag matching
        for tag in candidate.get("tags", []):
            if any(like in tag for like in likes):
                score += 1.0
            if any(dislike in tag for dislike in dislikes):
                score -= 1.0

        # Budget compatibility
        if budget_max and candidate.get("price"):
            price = candidate["price"]
            if price <= budget_max:
                score += 0.5
            else:
                score -= 0.5 * ((price - budget_max) / budget_max)

        # Rating boost
        score += (candidate.get("rating", 3.5) - 3.5) * 0.5

        # Tone influence
        if tone == "positive":
            score *= 1.1
        elif tone == "negative":
            score *= 0.9

        return score
