"""
database.py
-----------
Handles reading and writing to database.json.
All data is stored in a single JSON file, matching the
structure used by the Angular frontend's assets/data/data.json.
"""

import json
import os
import math
import time

DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")


def _read_db():
    """Read and return the full database as a dict."""
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_db(data):
    """Write the full database dict back to the JSON file."""
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
#  MEAL HELPERS
# ─────────────────────────────────────────────

def _compute_meal_stats(meal):
    """
    Add averageRating and performanceCategory to a meal dict.
    Logic mirrors the Angular DataService.processMeal() method:
      top      → avg >= 8.0
      moderate → avg >= 6.0
      low      → avg <  6.0
    """
    ratings = meal.get("ratings", [])
    if ratings:
        avg = sum(ratings) / len(ratings)
        avg_rounded = round(avg * 10) / 10
    else:
        avg_rounded = 0.0

    if avg_rounded >= 8:
        category = "top"
    elif avg_rounded >= 6:
        category = "moderate"
    else:
        category = "low"

    return {
        **meal,
        "averageRating": avg_rounded,
        "performanceCategory": category,
    }


def get_all_meals():
    """Return all meals with computed averageRating and performanceCategory."""
    db = _read_db()
    return [_compute_meal_stats(m) for m in db.get("meals", [])]


def get_meal_by_id(meal_id):
    """Return a single meal by id, or None if not found."""
    db = _read_db()
    for meal in db.get("meals", []):
        if meal["id"] == str(meal_id):
            return _compute_meal_stats(meal)
    return None


def add_meal(name, restaurant, category, image, description, ratings, added_by, created_at):
    """
    Insert a new meal into the database.
    Returns the newly created meal (with computed stats).
    """
    db = _read_db()
    new_id = str(int(time.time() * 1000))  # millisecond timestamp as string id
    new_meal = {
        "id": new_id,
        "name": name,
        "restaurant": restaurant,
        "category": category,
        "image": image,
        "description": description,
        "ratings": ratings if isinstance(ratings, list) else [],
        "addedBy": added_by,
        "createdAt": created_at,
    }
    db["meals"].append(new_meal)
    _write_db(db)
    return _compute_meal_stats(new_meal)


def add_rating_to_meal(meal_id, rating):
    """
    Append a rating to a meal's ratings list.
    Returns the updated meal with stats, or None if meal not found.
    """
    db = _read_db()
    for meal in db["meals"]:
        if meal["id"] == str(meal_id):
            meal["ratings"].append(rating)
            _write_db(db)
            return _compute_meal_stats(meal)
    return None


def delete_meal(meal_id):
    """
    Delete a meal by id.
    Returns True if deleted, False if not found.
    """
    db = _read_db()
    original_count = len(db["meals"])
    db["meals"] = [m for m in db["meals"] if m["id"] != str(meal_id)]
    if len(db["meals"]) == original_count:
        return False
    _write_db(db)
    return True


def get_stats():
    """
    Return dashboard statistics matching the Angular DataService.getStats() method.
    """
    meals = get_all_meals()
    total = len(meals)
    top = sum(1 for m in meals if m["performanceCategory"] == "top")
    moderate = sum(1 for m in meals if m["performanceCategory"] == "moderate")
    low = sum(1 for m in meals if m["performanceCategory"] == "low")

    if total > 0:
        avg_overall = round(
            (sum(m["averageRating"] for m in meals) / total) * 10
        ) / 10
    else:
        avg_overall = 0.0

    return {
        "total": total,
        "top": top,
        "moderate": moderate,
        "low": low,
        "avgOverall": avg_overall,
    }


# ─────────────────────────────────────────────
#  USER HELPERS
# ─────────────────────────────────────────────

def get_user_by_email(email):
    """Return a user dict by email (case-insensitive), or None."""
    db = _read_db()
    email_lower = email.strip().lower()
    for user in db.get("users", []):
        if user["email"].lower() == email_lower:
            return user
    return None


def get_user_by_id(user_id):
    """Return a user dict by id, or None."""
    db = _read_db()
    for user in db.get("users", []):
        if user["id"] == str(user_id):
            return user
    return None


def get_all_users():
    """Return all users (passwords included — strip before sending to client)."""
    db = _read_db()
    return db.get("users", [])


# ─────────────────────────────────────────────
#  RESTAURANT & CATEGORY HELPERS
# ─────────────────────────────────────────────

def get_restaurants():
    """Return list of restaurant objects: [{id, name}, ...]."""
    db = _read_db()
    return db.get("restaurants", [])


def add_restaurant(name):
    """
    Add a new restaurant if it doesn't already exist.
    Returns the restaurant object.
    """
    db = _read_db()
    # Check if already exists (case-insensitive)
    for r in db["restaurants"]:
        if r["name"].lower() == name.strip().lower():
            return r
    new_id = str(len(db["restaurants"]) + 1)
    new_restaurant = {"id": new_id, "name": name.strip()}
    db["restaurants"].append(new_restaurant)
    _write_db(db)
    return new_restaurant


def get_categories():
    """Return list of category strings."""
    db = _read_db()
    return db.get("categories", [])


def reset_database():
    """
    Reset the database to the original seed data.
    Returns the fresh database dict.
    """
    seed = {
        "meals": [
            {
                "id": "1",
                "name": "Chicken Biryani",
                "restaurant": "Spice Garden",
                "category": "Main Course",
                "image": "🍛",
                "description": "Aromatic basmati rice cooked with tender chicken and spices",
                "ratings": [9, 8, 9, 10, 8, 9],
                "addedBy": "admin",
                "createdAt": "2024-01-15",
            },
            {
                "id": "2",
                "name": "Seekh Kebab",
                "restaurant": "BBQ Tonight",
                "category": "Starter",
                "image": "🥩",
                "description": "Minced meat skewers grilled to perfection with aromatic herbs",
                "ratings": [7, 8, 6, 7, 8],
                "addedBy": "admin",
                "createdAt": "2024-01-20",
            },
            {
                "id": "3",
                "name": "Karahi Gosht",
                "restaurant": "Desi Dhaba",
                "category": "Main Course",
                "image": "🍲",
                "description": "Tender mutton cooked in a wok with tomatoes and green chilies",
                "ratings": [9, 9, 10, 9, 8, 10],
                "addedBy": "admin",
                "createdAt": "2024-02-01",
            },
            {
                "id": "4",
                "name": "Gulab Jamun",
                "restaurant": "Sweet Treats",
                "category": "Dessert",
                "image": "🍮",
                "description": "Soft milk-solid dumplings soaked in rose-flavored syrup",
                "ratings": [10, 9, 10, 10],
                "addedBy": "admin",
                "createdAt": "2024-02-10",
            },
            {
                "id": "5",
                "name": "Nihari",
                "restaurant": "Old City Kitchen",
                "category": "Main Course",
                "image": "🍜",
                "description": "Slow-cooked beef stew with warming spices, a Lahori breakfast classic",
                "ratings": [8, 7, 8, 6, 7],
                "addedBy": "admin",
                "createdAt": "2024-02-15",
            },
            {
                "id": "6",
                "name": "Samosa",
                "restaurant": "Street Bites",
                "category": "Snack",
                "image": "🥟",
                "description": "Crispy pastry filled with spiced potatoes and served with chutney",
                "ratings": [5, 6, 5, 4, 6],
                "addedBy": "admin",
                "createdAt": "2024-03-01",
            },
        ],
        "users": [
            {
                "id": "1",
                "name": "Admin User",
                "email": "admin@mealrating.com",
                "password": "Admin@123",
                "role": "admin",
                "avatar": "A",
                "joinedAt": "2024-01-01",
            },
            {
                "id": "2",
                "name": "Demo User",
                "email": "demo@mealrating.com",
                "password": "Demo@123",
                "role": "user",
                "avatar": "D",
                "joinedAt": "2024-01-10",
            },
        ],
        "restaurants": [
            {"id": "1", "name": "Spice Garden"},
            {"id": "2", "name": "BBQ Tonight"},
            {"id": "3", "name": "Desi Dhaba"},
            {"id": "4", "name": "Sweet Treats"},
            {"id": "5", "name": "Old City Kitchen"},
            {"id": "6", "name": "Street Bites"},
        ],
        "categories": ["Starter", "Main Course", "Dessert", "Snack", "Beverage", "Bread"],
    }
    _write_db(seed)
    return seed
