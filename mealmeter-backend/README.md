# 🍽️ MealMeter — Python Backend API

Flask REST API backend for the MealMeter Angular 19 frontend.

---

## 📋 Requirements

- Python 3.8 or higher
- pip

---

## 🚀 Setup & Run

### Step 1 — Install dependencies
```bash
cd mealmeter-backend
pip install -r requirements.txt
```

### Step 2 — (Optional) Edit .env
```
SECRET_KEY=mealmeter-super-secret-jwt-key-2024
JWT_EXPIRY_HOURS=24
PORT=5000
DEBUG=True
```

### Step 3 — Start the server
```bash
python app.py
```

Server starts at: **http://localhost:5000**

### Step 4 — Run tests (optional, while server is running)
```bash
python test_api.py
```

---

## 🔑 Login Credentials

| Role  | Email                    | Password   |
|-------|--------------------------|------------|
| Admin | admin@mealrating.com     | Admin@123  |
| User  | demo@mealrating.com      | Demo@123   |

---

## 📡 API Endpoints

All endpoints are prefixed with `/api`.

### Auth
| Method | Endpoint         | Auth     | Description                   |
|--------|-----------------|----------|-------------------------------|
| POST   | /auth/login      | None     | Login, get JWT token          |
| GET    | /auth/me         | Token    | Get current user              |
| POST   | /auth/logout     | None     | Logout (client-side)          |

**Login body:**
```json
{ "email": "admin@mealrating.com", "password": "Admin@123" }
```
**Login response:**
```json
{
  "success": true,
  "message": "Login successful!",
  "token": "<JWT>",
  "user": { "id": "1", "name": "Admin User", "email": "...", "role": "admin", "avatar": "A", "joinedAt": "..." }
}
```

---

### Meals
| Method | Endpoint                  | Auth     | Description                   |
|--------|--------------------------|----------|-------------------------------|
| GET    | /meals                   | None     | Get all meals (filterable)    |
| GET    | /meals/:id               | None     | Get meal by id                |
| POST   | /meals                   | Token    | Add new meal                  |
| POST   | /meals/:id/rating        | Token    | Submit a rating (1–10)        |
| DELETE | /meals/:id               | Admin    | Delete a meal                 |

**GET /meals query params:**
- `?search=biryani` — search name/restaurant/description
- `?category=Main+Course`
- `?performance=top` — `top` / `moderate` / `low`
- `?restaurant=Spice+Garden`
- `?sort=newest` — `newest` / `rating-high` / `rating-low` / `name` / `most-rated`

**Meal object returned:**
```json
{
  "id": "1",
  "name": "Chicken Biryani",
  "restaurant": "Spice Garden",
  "category": "Main Course",
  "image": "🍛",
  "description": "...",
  "ratings": [9, 8, 9, 10, 8, 9],
  "addedBy": "admin",
  "createdAt": "2024-01-15",
  "averageRating": 8.8,
  "performanceCategory": "top"
}
```

**POST /meals body:**
```json
{
  "name": "Chicken Karahi",
  "restaurant": "Desi Dhaba",
  "category": "Main Course",
  "image": "🍲",
  "description": "Rich tomato-based chicken curry",
  "ratings": [8],
  "addedBy": "Demo User",
  "createdAt": "2024-06-01"
}
```

**POST /meals/:id/rating body:**
```json
{ "rating": 9 }
```

---

### Stats
| Method | Endpoint   | Auth   | Description             |
|--------|-----------|--------|-------------------------|
| GET    | /stats    | Token  | Dashboard statistics    |

**Response:**
```json
{
  "success": true,
  "stats": { "total": 6, "top": 3, "moderate": 2, "low": 1, "avgOverall": 7.8 }
}
```

---

### Restaurants
| Method | Endpoint       | Auth   | Description          |
|--------|---------------|--------|----------------------|
| GET    | /restaurants  | None   | Get all restaurants  |
| POST   | /restaurants  | Token  | Add new restaurant   |

---

### Categories
| Method | Endpoint      | Auth | Description         |
|--------|--------------|------|---------------------|
| GET    | /categories  | None | Get all categories  |

---

### Users (Admin only)
| Method | Endpoint | Auth  | Description       |
|--------|---------|-------|-------------------|
| GET    | /users  | Admin | Get all users     |

---

### Utility
| Method | Endpoint  | Auth  | Description                      |
|--------|----------|-------|----------------------------------|
| GET    | /health  | None  | Health check                     |
| POST   | /reset   | Admin | Reset DB to seed data            |

---

## 🔐 Authentication

Use JWT Bearer token in headers:
```
Authorization: Bearer <token>
```

Tokens expire after **24 hours**.

---

## 📁 File Structure

```
mealmeter-backend/
├── app.py              ← Main Flask application (all routes)
├── database_helper.py  ← All DB read/write functions
├── auth_helper.py      ← JWT create/verify + decorators
├── database.json       ← Data store (mirrors frontend assets/data/data.json)
├── test_api.py         ← Full API test script
├── requirements.txt    ← Python dependencies
├── .env                ← Environment variables
└── README.md
```

---

## 🔄 Performance Categories

Matches Angular frontend logic exactly:

| Category | Average Rating | Label       |
|----------|---------------|-------------|
| top      | ≥ 8.0         | 🏆 Top Rated   |
| moderate | ≥ 6.0 & < 8   | 👍 Moderate    |
| low      | < 6.0         | 📉 Low Rated   |

---

## ⚙️ CORS

CORS is enabled for all origins (`*`) to allow the Angular dev server (`localhost:4200`) to communicate freely. Restrict to specific origins in production.
