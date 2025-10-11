# backend/app/core/recommender.py

import os
from typing import List, Dict, Optional
import numpy as np

# Try sentence-transformers for better semantic matching; fallback to sklearn TF-IDF
try:
    from sentence_transformers import SentenceTransformer, util
    _HAS_ST = True
except Exception:
    _HAS_ST = False

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    def __init__(self, place_data: Optional[List[Dict]] = None):
        """
        place_data: list of place dicts, each with keys:
          - id, name, tags (list), description (str), price (float), rating (float)
        """
        self.places = place_data or []
        self._use_embeddings = False
        self._vectorizer = None
        self._corpus_vectors = None

        if _HAS_ST:
            try:
                # small model; change to a larger one if you have resources
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                self._use_embeddings = True
            except Exception:
                self._use_embeddings = False

        if not self._use_embeddings:
            # Build a TF-IDF vectorizer on place descriptions + tags
            texts = [self._place_text(p) for p in self.places]
            self._vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
            if texts:
                self._corpus_vectors = self._vectorizer.fit_transform(texts)

    def _place_text(self, p: Dict) -> str:
        tags = " ".join(p.get("tags", []))
        desc = p.get("description", "")
        return f"{p.get('name','')} {tags} {desc}"

    def add_place(self, place: Dict):
        self.places.append(place)
        # Rebuild corpus vectors lazily on next recommend call
        self._corpus_vectors = None

    def _ensure_corpus_vectors(self):
        if self._use_embeddings and not hasattr(self, "_corpus_embeddings"):
            texts = [self._place_text(p) for p in self.places]
            if texts:
                self._corpus_embeddings = self.model.encode(texts, convert_to_tensor=True)
        if not self._use_embeddings and self._corpus_vectors is None:
            texts = [self._place_text(p) for p in self.places]
            if texts:
                self._corpus_vectors = self._vectorizer.fit_transform(texts)

    def recommend(self, query: str = None, group_preferences: List[Dict] = None, top_k: int = 10) -> List[Dict]:
        """
        Returns top_k recommended places scored by:
         - semantic similarity between query and place descriptions
         - tag match against aggregated group preferences
         - budget compatibility and rating
        """
        if not self.places:
            return []

        self._ensure_corpus_vectors()

        # Semantic similarity scores
        sem_scores = np.zeros(len(self.places))
        if query:
            if self._use_embeddings:
                q_emb = self.model.encode(query, convert_to_tensor=True)
                sims = util.cos_sim(q_emb, self._corpus_embeddings).cpu().numpy()[0]
                sem_scores = np.array(sims)
            else:
                q_vec = self._vectorizer.transform([query])
                sims = cosine_similarity(q_vec, self._corpus_vectors)[0]
                sem_scores = np.array(sims)

        # Aggregate group preference tags (simple frequency)
        tag_weight = {}
        if group_preferences:
            for p in group_preferences:
                prefs = p.get("preferences", {})
                for tag in prefs.get("likes", []):
                    tag_weight[tag] = tag_weight.get(tag, 0) + 1
                for tag in prefs.get("dislikes", []):
                    tag_weight[tag] = tag_weight.get(tag, 0) - 1

        # compute final scores
        final_scores = []
        for idx, place in enumerate(self.places):
            score = 0.0
            # semantic
            score += 1.5 * float(sem_scores[idx]) if query else 0.0

            # tag matching (count positive likes, penalize dislikes)
            tags = place.get("tags", [])
            tag_score = 0.0
            for t in tags:
                tag_score += tag_weight.get(t, 0)
            # normalize by number of users if group present
            if group_preferences:
                user_count = max(len(group_preferences), 1)
                tag_score = tag_score / user_count
            score += 0.8 * tag_score

            # budget compatibility (if any user has a strict budget, penalize place over budget)
            budget_penalty = 0.0
            if group_preferences:
                avg_budget = None
                budgets = [p.get("preferences", {}).get("budget_max") for p in group_preferences]
                budgets = [b for b in budgets if b]
                if budgets:
                    avg_budget = sum(budgets) / len(budgets)
                if avg_budget and place.get("price"):
                    price = place["price"]
                    if price > avg_budget:
                        budget_penalty = -0.5 * ((price - avg_budget) / avg_budget)
                    else:
                        budget_penalty = 0.2
            score += budget_penalty

            # rating contribution (normalized around 3.5)
            rating = place.get("rating", 3.5)
            score += 0.3 * (rating - 3.5)

            final_scores.append((place, float(score)))

        # sort and return top_k
        ranked = sorted(final_scores, key=lambda x: x[1], reverse=True)[:top_k]
        results = []
        for place, sc in ranked:
            p = place.copy()
            p["score"] = round(sc, 4)
            results.append(p)
        return results
