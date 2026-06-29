import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { Meal } from '../models/models';
import { AuthService } from '../services/auth.service';
import { DataService } from '../services/data.service';
import { NavbarComponent } from '../shared/navbar/navbar.component';

@Component({
  selector: 'app-meals',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent],
  templateUrl: './meals.component.html',
  styleUrls: ['./meals.component.css']
})
export class MealsComponent implements OnInit {
  allMeals: Meal[] = [];
  filteredMeals: Meal[] = [];
  categories: any = [];
  restaurants: any = [];

  searchTerm = '';
  filterCategory = '';
  filterPerformance = '';
  filterRestaurant = '';
  sortBy = 'newest';
  viewMode: 'grid' | 'list' = 'grid';

  constructor(public dataService: DataService, public auth: AuthService) {}

  ngOnInit(): void {
    this.dataService.meals$.subscribe((meals:any) => {
      this.allMeals = meals;
      console.log('all meals',this.allMeals);
      
      this.categories = [...new Set(meals.map((m:any) => m.category))];
      this.restaurants = [...new Set(meals.map((m:any) => m.restaurant))];
      this.applyFilters();
    });
  }

  applyFilters(): void {
    let result = [...this.allMeals];

    if (this.searchTerm) {
      const q = this.searchTerm.toLowerCase();
      result = result.filter(m =>
        m.name.toLowerCase().includes(q) ||
        m.restaurant.toLowerCase().includes(q) ||
        m.description.toLowerCase().includes(q)
      );
    }
    if (this.filterCategory) result = result.filter(m => m.category === this.filterCategory);
    if (this.filterPerformance) result = result.filter(m => m.performanceCategory === this.filterPerformance);
    if (this.filterRestaurant) result = result.filter(m => m.restaurant === this.filterRestaurant);

    switch (this.sortBy) {
      case 'rating-high': result.sort((a, b) => (b.averageRating || 0) - (a.averageRating || 0)); break;
      case 'rating-low': result.sort((a, b) => (a.averageRating || 0) - (b.averageRating || 0)); break;
      case 'name': result.sort((a, b) => a.name.localeCompare(b.name)); break;
      case 'newest': result.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()); break;
      case 'most-rated': result.sort((a, b) => b.ratings.length - a.ratings.length); break;
    }

    this.filteredMeals = result;
  }

  clearFilters(): void {
    this.searchTerm = '';
    this.filterCategory = '';
    this.filterPerformance = '';
    this.filterRestaurant = '';
    this.sortBy = 'newest';
    this.applyFilters();
  }

  deleteMeal(id: string, event: Event): void {
    event.stopPropagation();
    if (confirm('Delete this meal?')) {
      this.dataService.deleteMeal(id);
    }
  }

  getCategoryClass(cat?: string): string {
    if (cat === 'top') return 'badge-top';
    if (cat === 'moderate') return 'badge-moderate';
    return 'badge-low';
  }

  getCategoryLabel(cat?: string): string {
    if (cat === 'top') return '🏆 Top';
    if (cat === 'moderate') return '👍 Moderate';
    return '📉 Low';
  }

  get hasActiveFilters(): boolean {
    return !!(this.searchTerm || this.filterCategory || this.filterPerformance || this.filterRestaurant);
  }
}
