# backend/app/core/nlp_engine.py

import re
from typing import Dict, List
from transformers import pipeline

class NLPEngine:
    """
    NLP module for extracting preferences, sentiment, and constraints
    from natural-language chat messages.
    """

    def __init__(self, use_transformer: bool = True):
        self.use_transformer = use_transformer
        if use_transformer:
            try:
                # Load lightweight DistilBERT sentiment model
                self.sentiment_analyzer = pipeline("sentiment-analysis")
            except Exception as e:
                print("⚠️ Transformer pipeline load failed:", e)
                self.use_transformer = False

    # ---------- core public method ----------
    def extract_preferences(self, message: str) -> Dict:
        message = message.lower()

        # --- extract tone ---
        tone = self._get_tone(message)

        # --- extract numeric constraints (e.g. budget/time) ---
        budget = self._extract_budget(message)

        # --- keyword-based preferences ---
        likes = self._extract_likes(message)
        dislikes = self._extract_dislikes(message)

        # --- build result ---
        result = {
            "likes": likes,
            "dislikes": dislikes,
            "budget_max": budget,
            "tone": tone
        }
        return result

    # ---------- helper methods ----------
    def _get_tone(self, text: str) -> str:
        if self.use_transformer:
            try:
                result = self.sentiment_analyzer(text[:512])[0]
                return result["label"].lower()
            except Exception:
                pass
        # fallback: rule-based sentiment
        if any(w in text for w in ["love", "like", "great", "awesome"]):
            return "positive"
        if any(w in text for w in ["hate", "bad", "terrible", "not good"]):
            return "negative"
        return "neutral"

    def _extract_budget(self, text: str) -> int:
        match = re.search(r"(\d{2,5})\s?(?:rs|inr|₹|rupees|bucks|k)?", text)
        if match:
            value = match.group(1)
            if "k" in text:  # e.g., 20k
                return int(value) * 1000
            return int(value)
        return None

    def _extract_likes(self, text: str) -> List[str]:
        # simple positive triggers
        patterns = ["love", "like", "enjoy", "prefer", "fond of"]
        likes = []
        for p in patterns:
            found = re.findall(p + r"\s+([a-zA-Z\s]+?)(?:,|\.|but|and|$)", text)
            for f in found:
                cleaned = f.strip()
                if cleaned:
                    likes.append(cleaned)
        return likes

    def _extract_dislikes(self, text: str) -> List[str]:
        patterns = ["hate", "dislike", "not like", "avoid", "don’t like", "dont like"]
        dislikes = []
        for p in patterns:
            found = re.findall(p + r"\s+([a-zA-Z\s]+?)(?:,|\.|but|and|$)", text)
            for f in found:
                cleaned = f.strip()
                if cleaned:
                    dislikes.append(cleaned)
        return dislikes
