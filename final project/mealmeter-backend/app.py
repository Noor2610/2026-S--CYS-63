"""
app.py
------
MealMeter Backend API
Flask REST API matching the Angular 19 frontend.

Base URL : http://localhost:5000/api

AUTH ROUTES
  POST   /api/auth/login          - Login, returns JWT token + user info
  GET    /api/auth/me             - Get current logged-in user (token required)
  POST   /api/auth/logout         - Logout (client-side token removal)

MEAL ROUTES
  GET    /api/meals               - Get all meals (with averageRating + performanceCategory)
  GET    /api/meals/<id>          - Get single meal by id
  POST   /api/meals               - Add new meal (token required)
  POST   /api/meals/<id>/rating   - Add rating to a meal (token required)
  DELETE /api/meals/<id>          - Delete a meal (admin only)

STATS ROUTE
  GET    /api/stats               - Dashboard statistics (token required)

RESTAURANTS ROUTES
  GET    /api/restaurants         - Get all restaurants
  POST   /api/restaurants         - Add new restaurant (token required)

CATEGORIES ROUTE
  GET    /api/categories          - Get all categories

USERS ROUTE
  GET    /api/users               - Get all users (admin only)

UTILITY
  GET    /api/health              - Health check
  POST   /api/reset               - Reset database to seed data (admin only)
"""

import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

import database_helper as db
from auth_helper import create_token, token_required, admin_required

# ─────────────────────────────────────────────
#  APP SETUP
# ─────────────────────────────────────────────

load_dotenv()

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


# ─────────────────────────────────────────────
#  CORS — manual headers (works without flask-cors)
# ─────────────────────────────────────────────

@app.after_request
def add_cors_headers(response):
    """
    Add CORS headers to every response.
    Allows the Angular dev server (localhost:4200) to call this API.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.route("/api/<path:path>", methods=["OPTIONS"])
def options_handler(path):
    """Handle all CORS preflight OPTIONS requests."""
    resp = jsonify({"ok": True})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return resp, 200


# ─────────────────────────────────────────────
#  UTILITY FUNCTIONS
# ─────────────────────────────────────────────

def _safe_user(user):
    """Return user dict without the password field."""
    if user is None:
        return None
    return {k: v for k, v in user.items() if k != "password"}


def _error(message, status_code=400):
    """Return a JSON error response."""
    return jsonify({"error": message}), status_code


# ─────────────────────────────────────────────
#  HEALTH CHECK
# ─────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "ok", "message": "MealMeter API is running"}), 200


# ─────────────────────────────────────────────
#  AUTH ROUTES
# ─────────────────────────────────────────────

@app.route("/api/auth/login", methods=["POST"])
def login():
    """
    POST /api/auth/login
    Body: { "email": "...", "password": "..." }
    Returns: { "token": "...", "user": {...}, "message": "..." }

    Matches Angular AuthService.login() exactly:
    - Find user by email (case-insensitive)
    - Compare plain-text password (as stored in database.json)
    - Return JWT token valid for 24 hours
    """
    body = request.get_json(silent=True)
    if not body:
        return _error("Request body must be JSON.")

    email = (body.get("email") or "").strip().lower()
    password = (body.get("password") or "")

    if not email:
        return _error("Email is required.")
    if not password:
        return _error("Password is required.")

    user = db.get_user_by_email(email)

    if user is None:
        return _error("No account found with this email.", 401)

    if user["password"] != password:
        return _error("Incorrect password.", 401)

    token = create_token(user["id"], user["role"])

    return jsonify({
        "success": True,
        "message": "Login successful!",
        "token": token,
        "user": _safe_user(user),
    }), 200


@app.route("/api/auth/me", methods=["GET"])
@token_required
def get_current_user(current_user_id, current_user_role):
    """
    GET /api/auth/me
    Header: Authorization: Bearer <token>
    Returns: { "user": {...} }
    """
    user = db.get_user_by_id(current_user_id)
    if user is None:
        return _error("User not found.", 404)
    return jsonify({"success": True, "user": _safe_user(user)}), 200


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    """
    POST /api/auth/logout
    Token is stateless (JWT), so logout is handled client-side.
    This endpoint exists for API completeness.
    """
    return jsonify({"success": True, "message": "Logged out successfully."}), 200


# ─────────────────────────────────────────────
#  MEAL ROUTES
# ─────────────────────────────────────────────

@app.route("/api/meals", methods=["GET"])
def get_meals():
    """
    GET /api/meals
    Optional query params:
      ?search=<str>           - filter by name/restaurant/description
      ?category=<str>         - filter by category
      ?performance=<str>      - top | moderate | low
      ?restaurant=<str>       - filter by restaurant name
      ?sort=<str>             - newest | rating-high | rating-low | name | most-rated
    Returns: { "meals": [...], "count": <int> }
    """
    meals = db.get_all_meals()

    search = (request.args.get("search") or "").strip().lower()
    category = (request.args.get("category") or "").strip()
    performance = (request.args.get("performance") or "").strip().lower()
    restaurant = (request.args.get("restaurant") or "").strip()
    sort_by = (request.args.get("sort") or "newest").strip()

    if search:
        meals = [
            m for m in meals
            if search in m["name"].lower()
            or search in m["restaurant"].lower()
            or search in m["description"].lower()
        ]

    if category:
        meals = [m for m in meals if m["category"] == category]

    if performance and performance in ("top", "moderate", "low"):
        meals = [m for m in meals if m["performanceCategory"] == performance]

    if restaurant:
        meals = [m for m in meals if m["restaurant"] == restaurant]

    if sort_by == "rating-high":
        meals.sort(key=lambda m: m["averageRating"], reverse=True)
    elif sort_by == "rating-low":
        meals.sort(key=lambda m: m["averageRating"])
    elif sort_by == "name":
        meals.sort(key=lambda m: m["name"].lower())
    elif sort_by == "most-rated":
        meals.sort(key=lambda m: len(m["ratings"]), reverse=True)
    else:
        meals.sort(key=lambda m: m["createdAt"], reverse=True)

    return jsonify({"success": True, "meals": meals, "count": len(meals)}), 200


@app.route("/api/meals/<string:meal_id>", methods=["GET"])
def get_meal(meal_id):
    """
    GET /api/meals/<id>
    Returns: { "meal": {...} }
    """
    meal = db.get_meal_by_id(meal_id)
    if meal is None:
        return _error(f"Meal with id '{meal_id}' not found.", 404)
    return jsonify({"success": True, "meal": meal}), 200


@app.route("/api/meals", methods=["POST"])
@token_required
def create_meal(current_user_id, current_user_role):
    """
    POST /api/meals
    Header: Authorization: Bearer <token>
    Body: {
      "name": "...",
      "restaurant": "...",
      "category": "...",
      "image": "...",
      "description": "...",
      "ratings": [...],
      "addedBy": "...",
      "createdAt": "YYYY-MM-DD"
    }
    Returns: { "meal": {...} }
    """
    body = request.get_json(silent=True)
    if not body:
        return _error("Request body must be JSON.")

    name        = (body.get("name") or "").strip()
    restaurant  = (body.get("restaurant") or "").strip()
    category    = (body.get("category") or "").strip()
    image       = (body.get("image") or "🍽️").strip()
    description = (body.get("description") or "").strip()
    ratings_raw = body.get("ratings", [])
    added_by    = (body.get("addedBy") or "Unknown").strip()
    created_at  = (body.get("createdAt") or "").strip()

    errors = {}
    if not name:
        errors["name"] = "Meal name is required."
    if not restaurant:
        errors["restaurant"] = "Restaurant is required."
    if not category:
        errors["category"] = "Category is required."
    if not description:
        errors["description"] = "Description is required."

    if not created_at:
        from datetime import date
        created_at = date.today().isoformat()

    if not isinstance(ratings_raw, list):
        errors["ratings"] = "Ratings must be a list."
    else:
        for r in ratings_raw:
            if not isinstance(r, (int, float)) or not (1 <= r <= 10):
                errors["ratings"] = "Each rating must be a number between 1 and 10."
                break

    if errors:
        return jsonify({"error": "Validation failed.", "details": errors}), 422

    # Auto-add restaurant if it's new
    existing_names = [r["name"].lower() for r in db.get_restaurants()]
    if restaurant.lower() not in existing_names:
        db.add_restaurant(restaurant)

    new_meal = db.add_meal(
        name=name,
        restaurant=restaurant,
        category=category,
        image=image,
        description=description,
        ratings=ratings_raw,
        added_by=added_by,
        created_at=created_at,
    )

    return jsonify({"success": True, "message": "Meal added successfully.", "meal": new_meal}), 201


@app.route("/api/meals/<string:meal_id>/rating", methods=["POST"])
@token_required
def add_rating(meal_id, current_user_id, current_user_role):
    """
    POST /api/meals/<id>/rating
    Header: Authorization: Bearer <token>
    Body: { "rating": <number 1-10> }
    Returns: { "meal": {...} }
    """
    body = request.get_json(silent=True)
    if not body:
        return _error("Request body must be JSON.")

    rating = body.get("rating")

    if rating is None:
        return _error("Rating is required.")
    if not isinstance(rating, (int, float)):
        return _error("Rating must be a number.")
    if not (1 <= rating <= 10):
        return _error("Rating must be between 1 and 10.")

    updated_meal = db.add_rating_to_meal(meal_id, rating)
    if updated_meal is None:
        return _error(f"Meal with id '{meal_id}' not found.", 404)

    return jsonify({
        "success": True,
        "message": "Rating submitted successfully.",
        "meal": updated_meal,
    }), 200


@app.route("/api/meals/<string:meal_id>", methods=["DELETE"])
@admin_required
def delete_meal(meal_id, current_user_id, current_user_role):
    """
    DELETE /api/meals/<id>
    Header: Authorization: Bearer <token>  (admin required)
    Returns: { "message": "..." }
    """
    deleted = db.delete_meal(meal_id)
    if not deleted:
        return _error(f"Meal with id '{meal_id}' not found.", 404)
    return jsonify({"success": True, "message": "Meal deleted successfully."}), 200


# ─────────────────────────────────────────────
#  STATS ROUTE
# ─────────────────────────────────────────────

@app.route("/api/stats", methods=["GET"])
@token_required
def get_stats(current_user_id, current_user_role):
    """
    GET /api/stats
    Header: Authorization: Bearer <token>
    Returns dashboard statistics matching Angular DataService.getStats().
    """
    stats = db.get_stats()
    return jsonify({"success": True, "stats": stats}), 200


# ─────────────────────────────────────────────
#  RESTAURANT ROUTES
# ─────────────────────────────────────────────

@app.route("/api/restaurants", methods=["GET"])
def get_restaurants():
    """GET /api/restaurants → { "restaurants": [{id, name}] }"""
    restaurants = db.get_restaurants()
    return jsonify({"success": True, "restaurants": restaurants}), 200


@app.route("/api/restaurants", methods=["POST"])
@token_required
def add_restaurant(current_user_id, current_user_role):
    """POST /api/restaurants — Body: { "name": "..." }"""
    body = request.get_json(silent=True)
    if not body:
        return _error("Request body must be JSON.")

    name = (body.get("name") or "").strip()
    if not name:
        return _error("Restaurant name is required.")

    restaurant = db.add_restaurant(name)
    return jsonify({"success": True, "restaurant": restaurant}), 201


# ─────────────────────────────────────────────
#  CATEGORIES ROUTE
# ─────────────────────────────────────────────

@app.route("/api/categories", methods=["GET"])
def get_categories():
    """GET /api/categories → { "categories": ["Starter", ...] }"""
    categories = db.get_categories()
    return jsonify({"success": True, "categories": categories}), 200


# ─────────────────────────────────────────────
#  USERS ROUTE (admin only)
# ─────────────────────────────────────────────

@app.route("/api/users", methods=["GET"])
@admin_required
def get_users(current_user_id, current_user_role):
    """GET /api/users (admin only) — returns users without passwords."""
    users = db.get_all_users()
    return jsonify({"success": True, "users": [_safe_user(u) for u in users]}), 200


# ─────────────────────────────────────────────
#  DATABASE RESET (admin only)
# ─────────────────────────────────────────────

@app.route("/api/reset", methods=["POST"])
@admin_required
def reset_database_route(current_user_id, current_user_role):
    """POST /api/reset (admin only) — resets database.json to seed data."""
    db.reset_database()
    return jsonify({"success": True, "message": "Database reset to seed data."}), 200


# ─────────────────────────────────────────────
#  ERROR HANDLERS
# ─────────────────────────────────────────────

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "The requested endpoint does not exist."}), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "HTTP method not allowed on this endpoint."}), 405


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error.", "detail": str(e)}), 500


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"
    print(f"\n🍽️  MealMeter API starting on http://localhost:{port}/api")
    print(f"   Debug mode : {debug}")
    print(f"   Database   : database.json\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
