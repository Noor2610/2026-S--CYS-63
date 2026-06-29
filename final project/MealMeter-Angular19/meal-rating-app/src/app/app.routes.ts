import { Routes } from '@angular/router';
import { authGuard, loginGuard } from './guards/auth.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  {
    path: 'login',
    loadComponent: () => import('./auth/login/login.component').then(m => m.LoginComponent),
    canActivate: [loginGuard]
  },
  {
    path: 'dashboard',
    loadComponent: () => import('./dashboard/dashboard.component').then(m => m.DashboardComponent),
    canActivate: [authGuard]
  },
  {
    path: 'meals',
    loadComponent: () => import('./meals/meals.component').then(m => m.MealsComponent),
    canActivate: [authGuard]
  },
  {
    path: 'meals/:id',
    loadComponent: () => import('./meals/meal-detail/meal-detail.component').then(m => m.MealDetailComponent),
    canActivate: [authGuard]
  },
  {
    path: 'add-meal',
    loadComponent: () => import('./meals/add-meal/add-meal.component').then(m => m.AddMealComponent),
    canActivate: [authGuard]
  },
  { path: '**', redirectTo: '/dashboard' }
];
