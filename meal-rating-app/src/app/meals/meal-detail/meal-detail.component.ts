import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { DataService } from '../../services/data.service';
import { AuthService } from '../../services/auth.service';
import { NavbarComponent } from '../../shared/navbar/navbar.component';
import { Meal } from '../../models/models';

@Component({
  selector: 'app-meal-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, NavbarComponent],
  templateUrl: './meal-detail.component.html',
  styleUrls: ['./meal-detail.component.css']
})
export class MealDetailComponent implements OnInit {
  meal: Meal | undefined;
  selectedRating = 0;
  hoverRating = 0;
  ratingSubmitted = false;
  submitSuccess = false;
  ratingNumbers = [1,2,3,4,5,6,7,8,9,10];
  
  // Add these computed properties
  highestRating: number | string = 'N/A';
  lowestRating: number | string = 'N/A';
  averageRating: number = 0;
  totalVotes: number = 0;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    public dataService: DataService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.dataService.meals$.subscribe(meals => {
        this.meal = meals.find(m => m.id === id);
        if (!this.meal) {
          this.router.navigate(['/meals']);
        } else {
          // Update computed properties when meal is loaded
          this.updateRatingStats();
        }
      });
    }
  }

  // Add this method to update stats whenever ratings change
  private updateRatingStats(): void {
    if (!this.meal) return;
    
    this.totalVotes = this.meal.ratings.length;
    
    if (this.totalVotes > 0) {
      this.highestRating = Math.max(...this.meal.ratings);
      this.lowestRating = Math.min(...this.meal.ratings);
      this.averageRating = this.meal.averageRating || 0;
    } else {
      this.highestRating = 'N/A';
      this.lowestRating = 'N/A';
      this.averageRating = 0;
    }
  }

  submitRating(): void {
    if (!this.selectedRating || !this.meal) return;
    this.dataService.addRating(this.meal.id, this.selectedRating);
    this.submitSuccess = true;
    this.ratingSubmitted = true;
    
    // Update stats after rating is submitted
    this.updateRatingStats();
    
    setTimeout(() => { 
      this.submitSuccess = false; 
    }, 3000);
  }

  resetRating(): void {
    this.selectedRating = 0;
    this.ratingSubmitted = false;
  }

  deleteMeal(): void {
    if (!this.meal) return;
    if (confirm('Delete this meal permanently?')) {
      this.dataService.deleteMeal(this.meal.id);
      this.router.navigate(['/meals']);
    }
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

  getRatingBarWidth(value: number): number {
    if (!this.meal || this.meal.ratings.length === 0) return 0;
    const count = this.meal.ratings.filter(r => Math.round(r) === value).length;
    return (count / this.meal.ratings.length) * 100;
  }

  getRatingCount(value: number): number {
    if (!this.meal) return 0;
    return this.meal.ratings.filter(r => Math.round(r) === value).length;
  }

  getRatingColor(rating: number): string {
    if (rating >= 8) return '#f59e0b';
    if (rating >= 6) return '#3b82f6';
    return '#ef4444';
  }
}