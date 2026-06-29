"""
test_api.py
-----------
Manual API test script for MealMeter backend.
Run AFTER starting the server with: python app.py

Usage:
    python test_api.py
"""

import sys
import json
import urllib.request
import urllib.error

BASE_URL = "http://localhost:5000/api"

# Mutable state shared across tests
state = {
    "admin_token": None,
    "user_token": None,
    "created_meal_id": None,
}

results = []
PASS = "✅"
FAIL = "❌"


def _request(method, path, body=None, token=None):
    """Make an HTTP request and return (status_code, response_dict)."""
    url = BASE_URL + path
    data = json.dumps(body).encode("utf-8") if body else None
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body_text = e.read().decode("utf-8")
            return e.code, json.loads(body_text)
        except Exception:
            return e.code, {"error": str(e)}
    except urllib.error.URLError:
        print(f"\n  ❌  Cannot connect to {url}")
        print("     Make sure the server is running: python app.py")
        sys.exit(1)


def check(label, status, response, expected_status, expected_key=None):
    """Assert status code and optional key presence. Print result."""
    ok = (status == expected_status)
    if ok and expected_key and expected_key not in response:
        ok = False
    results.append(ok)
    mark = PASS if ok else FAIL
    detail = "" if ok else f"  → got HTTP {status}, body: {json.dumps(response)[:120]}"
    print(f"  {mark}  {label}{detail}")
    return response


# ─────────────────────────────────────────────────────────────────────────────
print("\n" + "=" * 62)
print("  MealMeter API Test Suite")
print("=" * 62)

# ── 1. HEALTH CHECK ───────────────────────────────────────────────────────────
print("\n[1] Health Check")
s, r = _request("GET", "/health")
check("GET /api/health → 200", s, r, 200, "status")

# ── 2. AUTH ───────────────────────────────────────────────────────────────────
print("\n[2] Authentication")

s, r = _request("POST", "/auth/login", {"email": "admin@mealrating.com", "password": "Admin@123"})
check("POST /api/auth/login (admin correct) → 200", s, r, 200, "token")
if s == 200 and "token" in r:
    state["admin_token"] = r["token"]

s, r = _request("POST", "/auth/login", {"email": "demo@mealrating.com", "password": "Demo@123"})
check("POST /api/auth/login (user correct) → 200", s, r, 200, "token")
if s == 200 and "token" in r:
    state["user_token"] = r["token"]

s, r = _request("POST", "/auth/login", {"email": "admin@mealrating.com", "password": "wrongpass"})
check("POST /api/auth/login (wrong password) → 401", s, r, 401)

s, r = _request("POST", "/auth/login", {"email": "nobody@x.com", "password": "pass"})
check("POST /api/auth/login (unknown email) → 401", s, r, 401)

s, r = _request("POST", "/auth/login", {})
check("POST /api/auth/login (empty body) → 400", s, r, 400)

s, r = _request("GET", "/auth/me", token=state["admin_token"])
check("GET /api/auth/me (valid token) → 200", s, r, 200, "user")

s, r = _request("GET", "/auth/me")
check("GET /api/auth/me (no token) → 401", s, r, 401)

s, r = _request("POST", "/auth/logout")
check("POST /api/auth/logout → 200", s, r, 200)

# ── 3. MEALS ─────────────────────────────────────────────────────────────────
print("\n[3] Meals")

s, r = _request("GET", "/meals")
check("GET /api/meals → 200", s, r, 200, "meals")
meal_list = r.get("meals", [])
if meal_list:
    first_meal = meal_list[0]
    for field in ["id", "name", "averageRating", "performanceCategory", "ratings"]:
        ok = field in first_meal
        results.append(ok)
        print(f"  {'✅' if ok else '❌'}  Meal has field '{field}'")

s, r = _request("GET", "/meals?sort=rating-high")
check("GET /api/meals?sort=rating-high → 200", s, r, 200, "meals")

s, r = _request("GET", "/meals?category=Main+Course")
check("GET /api/meals?category=Main Course → 200", s, r, 200, "meals")
for m in r.get("meals", []):
    if m.get("category") != "Main Course":
        results.append(False)
        print(f"  {FAIL}  Category filter returned wrong item: {m.get('category')}")
        break

s, r = _request("GET", "/meals?performance=top")
check("GET /api/meals?performance=top → 200", s, r, 200, "meals")

s, r = _request("GET", "/meals?search=biryani")
check("GET /api/meals?search=biryani → 200", s, r, 200, "meals")

s, r = _request("GET", "/meals?sort=newest")
check("GET /api/meals?sort=newest → 200", s, r, 200, "meals")

s, r = _request("GET", "/meals/1")
check("GET /api/meals/1 → 200", s, r, 200, "meal")

s, r = _request("GET", "/meals/999999")
check("GET /api/meals/999999 (not found) → 404", s, r, 404)

# Add meal
new_meal_body = {
    "name": "Test Haleem",
    "restaurant": "Test Kitchen",
    "category": "Main Course",
    "image": "🍲",
    "description": "Slow-cooked lentils and meat test dish",
    "ratings": [8, 9],
    "addedBy": "Admin User",
    "createdAt": "2024-06-01",
}
s, r = _request("POST", "/meals", new_meal_body, token=state["admin_token"])
check("POST /api/meals (valid, admin token) → 201", s, r, 201, "meal")
if s == 201 and "meal" in r:
    state["created_meal_id"] = r["meal"]["id"]

s, r = _request("POST", "/meals", new_meal_body)
check("POST /api/meals (no token) → 401", s, r, 401)

s, r = _request("POST", "/meals", {"name": "", "restaurant": "", "category": ""}, token=state["user_token"])
check("POST /api/meals (missing required fields) → 422", s, r, 422)

# Add rating
s, r = _request("POST", "/meals/1/rating", {"rating": 9}, token=state["user_token"])
check("POST /api/meals/1/rating (valid, rating=9) → 200", s, r, 200, "meal")

s, r = _request("POST", "/meals/1/rating", {"rating": 15}, token=state["user_token"])
check("POST /api/meals/1/rating (rating=15, out of range) → 400", s, r, 400)

s, r = _request("POST", "/meals/1/rating", {"rating": 0}, token=state["user_token"])
check("POST /api/meals/1/rating (rating=0, out of range) → 400", s, r, 400)

s, r = _request("POST", "/meals/1/rating", {}, token=state["user_token"])
check("POST /api/meals/1/rating (missing rating) → 400", s, r, 400)

s, r = _request("POST", "/meals/1/rating", {"rating": 8})
check("POST /api/meals/1/rating (no token) → 401", s, r, 401)

# Delete meal
meal_id = state["created_meal_id"]
if meal_id:
    s, r = _request("DELETE", f"/meals/{meal_id}", token=state["user_token"])
    check(f"DELETE /api/meals/{meal_id} (user, not admin) → 403", s, r, 403)

    s, r = _request("DELETE", f"/meals/{meal_id}", token=state["admin_token"])
    check(f"DELETE /api/meals/{meal_id} (admin) → 200", s, r, 200)

    s, r = _request("DELETE", f"/meals/{meal_id}", token=state["admin_token"])
    check(f"DELETE /api/meals/{meal_id} (already deleted) → 404", s, r, 404)

s, r = _request("DELETE", "/meals/1")
check("DELETE /api/meals/1 (no token) → 401", s, r, 401)

# ── 4. STATS ─────────────────────────────────────────────────────────────────
print("\n[4] Stats")

s, r = _request("GET", "/stats", token=state["admin_token"])
check("GET /api/stats (admin token) → 200", s, r, 200, "stats")
stats = r.get("stats", {})
for key in ["total", "top", "moderate", "low", "avgOverall"]:
    ok = key in stats
    results.append(ok)
    print(f"  {'✅' if ok else '❌'}  Stats has key '{key}'")

s, r = _request("GET", "/stats")
check("GET /api/stats (no token) → 401", s, r, 401)

# ── 5. RESTAURANTS ───────────────────────────────────────────────────────────
print("\n[5] Restaurants")

s, r = _request("GET", "/restaurants")
check("GET /api/restaurants → 200", s, r, 200, "restaurants")

s, r = _request("POST", "/restaurants", {"name": "New Test Restaurant"}, token=state["user_token"])
check("POST /api/restaurants (valid token) → 201", s, r, 201, "restaurant")

s, r = _request("POST", "/restaurants", {"name": "New Test Restaurant"}, token=state["user_token"])
check("POST /api/restaurants (duplicate) → 201 idempotent", s, r, 201)

s, r = _request("POST", "/restaurants", {"name": ""}, token=state["user_token"])
check("POST /api/restaurants (empty name) → 400", s, r, 400)

s, r = _request("POST", "/restaurants", {"name": "X"})
check("POST /api/restaurants (no token) → 401", s, r, 401)

# ── 6. CATEGORIES ────────────────────────────────────────────────────────────
print("\n[6] Categories")

s, r = _request("GET", "/categories")
check("GET /api/categories → 200", s, r, 200, "categories")
ok = isinstance(r.get("categories"), list) and len(r.get("categories", [])) > 0
results.append(ok)
print(f"  {'✅' if ok else '❌'}  Categories list is non-empty")

# ── 7. USERS ─────────────────────────────────────────────────────────────────
print("\n[7] Users")

s, r = _request("GET", "/users", token=state["admin_token"])
check("GET /api/users (admin) → 200", s, r, 200, "users")
password_leaked = any("password" in u for u in r.get("users", []))
results.append(not password_leaked)
print(f"  {'✅' if not password_leaked else '❌'}  No password fields in /api/users response")

s, r = _request("GET", "/users", token=state["user_token"])
check("GET /api/users (non-admin) → 403", s, r, 403)

s, r = _request("GET", "/users")
check("GET /api/users (no token) → 401", s, r, 401)

# ── 8. RESET ─────────────────────────────────────────────────────────────────
print("\n[8] Database Reset")

s, r = _request("POST", "/reset", token=state["user_token"])
check("POST /api/reset (non-admin) → 403", s, r, 403)

s, r = _request("POST", "/reset", token=state["admin_token"])
check("POST /api/reset (admin) → 200", s, r, 200)

# ── 9. ERROR HANDLERS ────────────────────────────────────────────────────────
print("\n[9] Error Handlers")

s, r = _request("GET", "/nonexistent-endpoint")
check("GET /api/nonexistent-endpoint → 404", s, r, 404)

# ── SUMMARY ──────────────────────────────────────────────────────────────────
passed = sum(1 for x in results if x)
total = len(results)
failed = total - passed
print("\n" + "=" * 62)
print(f"  Results: {passed}/{total} passed  |  {failed} failed")
print("=" * 62)

if failed == 0:
    print("  🎉  All tests passed!\n")
    sys.exit(0)
else:
    print(f"  ⚠️   {failed} test(s) failed. Check output above.\n")
    sys.exit(1)
