import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { map, tap } from 'rxjs/operators';
import { Meal, AppData, User, Restaurant } from '../models/models';

@Injectable({ providedIn: 'root' })
export class DataService {
  private apiUrl = 'http://127.0.0.1:5000/api';
  private appData: AppData | null = null;
  private mealsSubject = new BehaviorSubject<Meal[]>([]);
  meals$ = this.mealsSubject.asObservable();

  constructor(private http: HttpClient) {
  this.loadData();
}

private loadData(): void {

  this.http.get<any>(`${this.apiUrl}/meals`).subscribe({

    next: (response) => {

      this.appData = {
        meals: response.meals,
        users: [],
        restaurants: [],
        categories: []
      };

      this.http.get<any>(`${this.apiUrl}/categories`).subscribe({
        next: (catRes) => {
          this.appData!.categories = catRes.categories;
        }
      });

      this.http.get<any>(`${this.apiUrl}/restaurants`).subscribe({
        next: (restRes) => {
          this.appData!.restaurants = restRes.restaurants;
        }
      });

      this.processAndEmitMeals();

    },

    error: (err) => {
      console.error('Failed to load meals', err);
    }

  });

}
  private processAndEmitMeals(): void {
    if (!this.appData) return;
    const processed = this.appData.meals.map(m => this.processMeal(m));
    this.mealsSubject.next(processed);
  }

  processMeal(meal: Meal): Meal {
    const avg = meal.ratings.length
      ? meal.ratings.reduce((a:any, b:any) => a + b, 0) / meal.ratings.length
      : 0;
    const avgRounded = Math.round(avg * 10) / 10;
    let cat: 'top' | 'moderate' | 'low';
    if (avgRounded >= 8) cat = 'top';
    else if (avgRounded >= 6) cat = 'moderate';
    else cat = 'low';
    return { ...meal, averageRating: avgRounded, performanceCategory: cat };
  }

  getMeals(): Meal[] {
    return this.mealsSubject.value;
  }

  getMealById(id: string): Meal | undefined {
    return this.getMeals().find(m => m.id === id);
  }

  addRating(mealId: string, rating: number): void {

  const session = JSON.parse(localStorage.getItem('authSession') || '{}');
  const token = session.token;

  this.http.post<any>(
    `${this.apiUrl}/meals/${mealId}/rating`,
    { rating: rating },
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  ).subscribe({

    next: (response) => {

      const meal = response.meal;

      if (!this.appData) return;

      const index = this.appData.meals.findIndex(m => m.id === mealId);

      if (index !== -1) {
        this.appData.meals[index] = meal;
      }

      this.processAndEmitMeals();

    },

    error: (err) => {
      console.error('Rating failed', err);
    }

  });

}
  addMeal(meal: Omit<Meal, 'id' | 'averageRating' | 'performanceCategory'>): void {

  const session = JSON.parse(localStorage.getItem('authSession') || '{}');
  const token = session.token;

  this.http.post<any>(
    `${this.apiUrl}/meals`,
    meal,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  ).subscribe({

    next: (response) => {

      if (!this.appData) {
        this.appData = {
          meals: [],
          users: [],
          restaurants: [],
          categories: []
        };
      }

      this.appData.meals.push(response.meal);
      this.processAndEmitMeals();

    },

    error: (err) => {
      console.error('Failed to add meal', err);
    }

  });


}

deleteMeal(id: string): void {

  const session = JSON.parse(localStorage.getItem('authSession') || '{}');
  const token = session.token;

  this.http.delete<any>(
    `${this.apiUrl}/meals/${id}`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  ).subscribe({

    next: () => {

      if (!this.appData) return;

      this.appData.meals = this.appData.meals.filter(m => m.id !== id);

      this.processAndEmitMeals();

    },

    error: (err) => {
      console.error('Delete failed', err);
    }

  });

}

  getRestaurants(): Restaurant[] {
    return this.appData?.restaurants || [];
  }

  getCategories(): string[] {
    return this.appData?.categories || [];
  }

  getUsers(): User[] {
    return this.appData?.users || [];
  }

  getUserByEmail(email: string): User | undefined {
    return this.appData?.users.find(u => u.email === email);
  }

  getStats() {
    const meals = this.getMeals();
    return {
      total: meals.length,
      top: meals.filter(m => m.performanceCategory === 'top').length,
      moderate: meals.filter(m => m.performanceCategory === 'moderate').length,
      low: meals.filter(m => m.performanceCategory === 'low').length,
      avgOverall: meals.length
        ? Math.round((meals.reduce((s, m) => s + (m.averageRating || 0), 0) / meals.length) * 10) / 10
        : 0
    };
  }

  resetData(): void {
  localStorage.removeItem('mealRatingData');
  this.loadData();
}
}