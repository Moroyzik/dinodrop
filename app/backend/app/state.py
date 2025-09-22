import json
import os
from typing import Any, Dict


DEFAULT_SEEDS = {
    "cases": [
        {
            "id": 1,
            "slug": "classic_case",
            "title": "Classic Case",
            "is_active": True,
            "min_price_minor": 9900,
            "image_url": "https://cdn/cases/classic.png",
        }
    ],
    "case_items": [
        {
            "id": 1,
            "case_id": 1,
            "item_name": "Field-tested AK",
            "steam_classid": "123",
            "rarity": "common",
            "base_price_minor": 12000,
            "weight_base": 6500,
            "weight_dyn": 6500,
            "is_active": True,
        },
        {
            "id": 2,
            "case_id": 1,
            "item_name": "AWP Redline",
            "steam_classid": "124",
            "rarity": "rare",
            "base_price_minor": 45000,
            "weight_base": 280,
            "weight_dyn": 280,
            "is_active": True,
        },
        {
            "id": 3,
            "case_id": 1,
            "item_name": "M9 Bayonet",
            "steam_classid": "125",
            "rarity": "legendary",
            "base_price_minor": 1500000,
            "weight_base": 5,
            "weight_dyn": 5,
            "is_active": True,
        },
    ],
}


def load_seeds_from_file(path: str | None = None) -> Dict[str, Any]:
    path = path or os.getenv("SEEDS_PATH", "/app/app/seeds/seed.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SEEDS

