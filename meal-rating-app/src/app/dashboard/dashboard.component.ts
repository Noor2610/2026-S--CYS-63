import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Meal } from '../models/models';
import { AuthService } from '../services/auth.service';
import { DataService } from '../services/data.service';
import { NavbarComponent } from '../shared/navbar/navbar.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, NavbarComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  stats = { total: 0, top: 0, moderate: 0, low: 0, avgOverall: 0 };
  topMeals: Meal[] = [];
  recentMeals: Meal[] = [];
  allMeals: Meal[] = [];

  constructor(public dataService: DataService, public auth: AuthService) {}

  ngOnInit(): void {
    this.dataService.meals$.subscribe((meals:any) => {
      this.allMeals = meals;
      this.stats = this.dataService.getStats();
      this.topMeals = [...meals]
        .filter(m => m.performanceCategory === 'top')
        .sort((a, b) => (b.averageRating || 0) - (a.averageRating || 0))
        .slice(0, 3);
      this.recentMeals = [...meals]
        .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime())
        .slice(0, 6);
    });
  }

  getCategoryClass(cat?: string): string {
    if (cat === 'top') return 'badge-top';
    if (cat === 'moderate') return 'badge-moderate';
    return 'badge-low';
  }

  getCategoryLabel(cat?: string): string {
    if (cat === 'top') return '🏆 Top Rated';
    if (cat === 'moderate') return '👍 Moderate';
    return '📉 Low Rated';
  }

  getStars(rating: number): string {
    return '★'.repeat(Math.round(rating / 2)) + '☆'.repeat(5 - Math.round(rating / 2));
  }
}
