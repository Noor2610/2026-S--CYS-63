# 🍽️ MealMeter – Universal Meal Rating System

A professional Angular 19 application for rating and evaluating meals across food establishments.

## 🚀 Features

- **Authentication** – Login with session management (24-hour sessions)
- **Dark / Light Mode** – Toggle with persistent preference
- **Dashboard** – Stats overview, top performers, performance charts
- **All Meals** – Search, filter by category/restaurant/performance, grid & list views
- **Meal Detail** – Rate meals 1–10, view rating distribution, admin delete
- **Add Meal** – Full form with emoji picker, restaurant selector, initial rating
- **Data in Assets** – All data stored in `src/assets/data/data.json`, synced to `localStorage`

## 🔑 Login Credentials

| Role  | Email                    | Password   |
|-------|--------------------------|------------|
| Admin | admin@mealrating.com     | Admin@123  |
| User  | demo@mealrating.com      | Demo@123   |

## 🛠️ Setup & Run

### Prerequisites
- Node.js 18+ 
- npm 9+
- Angular CLI 19

### Install Angular CLI
```bash
npm install -g @angular/cli@19
```

### Install & Run
```bash
cd meal-rating-app
npm install
ng serve
```

Open: **http://localhost:4200**

### Build for Production
```bash
ng build --configuration production
```
Output in `dist/meal-rating-app/`

## 📁 Project Structure

```
src/
├── app/
│   ├── auth/login/          # Login page
│   ├── dashboard/           # Dashboard with stats
│   ├── meals/
│   │   ├── meals.component  # Meals list with filters
│   │   ├── meal-detail/     # Meal detail + rating
│   │   └── add-meal/        # Add new meal form
│   ├── shared/navbar/       # Navigation bar
│   ├── services/
│   │   ├── auth.service.ts  # Authentication
│   │   ├── data.service.ts  # Data management
│   │   └── theme.service.ts # Dark/light mode
│   ├── guards/auth.guard.ts # Route protection
│   └── models/models.ts     # TypeScript interfaces
├── assets/data/data.json    # All application data
├── styles.css               # Global styles + CSS variables
└── index.html
```

## 🎨 Design

- **Color**: Saffron/amber accent (#f07500) – food-industry inspired
- **Font**: Inter (Google Fonts)
- **Approach**: CSS custom properties for seamless theme switching
- **Responsive**: Mobile-first, works on all screen sizes

## 📊 Meal Categories

Meals are auto-classified based on average rating:
- 🏆 **Top Rated** – Average ≥ 8.0
- 👍 **Moderate** – Average 6.0–7.9  
- 📉 **Low Rated** – Average < 6.0

## 🔧 Customization

Edit `src/assets/data/data.json` to add initial meals, users, or restaurants.  
To reset app data to defaults: clear `localStorage` key `mealRatingData`.
