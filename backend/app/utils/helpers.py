# backend/app/utils/helpers.py

import csv
import os

def load_place_data_from_csv(path: str):
    """
    CSV should have headers: id,name,tags,description,price,rating
    tags should be pipe-separated e.g. beach|seafood|relax
    """
    places = []
    if not os.path.exists(path):
        return places
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tags = [t.strip() for t in row.get("tags","").split("|") if t.strip()]
            places.append({
                "id": row.get("id"),
                "name": row.get("name"),
                "tags": tags,
                "description": row.get("description",""),
                "price": float(row["price"]) if row.get("price") else None,
                "rating": float(row["rating"]) if row.get("rating") else None
            })
    return places
