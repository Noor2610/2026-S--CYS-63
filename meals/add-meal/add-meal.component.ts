import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { DataService } from '../../services/data.service';
import { AuthService } from '../../services/auth.service';
import { NavbarComponent } from '../../shared/navbar/navbar.component';

const MEAL_EMOJIS = ['🍛','🍜','🍲','🥩','🍖','🥗','🍱','🥘','🍢','🍣','🥟','🍮','🧆','🥪','🥞','🧇','🧋','🍙','🌮','🍕','🍩','🍨','🍪','🍟','🍔','🍤','🥮','🍹','🌭','🥙','🌯','🫕','🍚','🍝','🥧','🍰'];

@Component({
  selector: 'app-add-meal',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule, NavbarComponent],
  templateUrl: './add-meal.component.html',
  styleUrls: ['./add-meal.component.css']
})
export class AddMealComponent implements OnInit {
  mealEmojis = MEAL_EMOJIS;
  categories: string[] = [];
  restaurants: string[] = [];

  form = {
    name: '',
    restaurant: '',
    category: '',
    image: '🍛',
    description: '',
    initialRating: 0
  };

  newRestaurant = '';
  showNewRestaurant = false;
  submitting = false;
  success = false;
  errors: { [key: string]: string } = {};

  constructor(
    public dataService: DataService,
    public auth: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {

  setTimeout(() => {

    this.categories = this.dataService.getCategories();
    this.restaurants = this.dataService.getRestaurants().map(r => r.name);

    console.log("Categories:", this.categories);
    console.log("Restaurants:", this.restaurants);

  }, 1000);

}

  selectEmoji(e: string): void { this.form.image = e; }

  validate(): boolean {
    this.errors = {};
    if (!this.form.name.trim()) this.errors['name'] = 'Meal name is required.';
    if (!this.form.restaurant && !this.newRestaurant.trim()) this.errors['restaurant'] = 'Restaurant is required.';
    if (!this.form.category) this.errors['category'] = 'Category is required.';
    if (!this.form.description.trim()) this.errors['description'] = 'Description is required.';
    return Object.keys(this.errors).length === 0;
  }

  onSubmit(): void {
    if (!this.validate()) return;
    this.submitting = true;

    const restaurant = this.showNewRestaurant ? this.newRestaurant.trim() : this.form.restaurant;

    setTimeout(() => {
      this.dataService.addMeal({
        name: this.form.name.trim(),
        restaurant,
        category: this.form.category,
        image: this.form.image,
        description: this.form.description.trim(),
        ratings: this.form.initialRating > 0 ? [this.form.initialRating] : [],
        addedBy: this.auth.currentUser?.name || 'Unknown',
        createdAt: new Date().toISOString().split('T')[0]
      });
      this.submitting = false;
      this.success = true;
      setTimeout(() => this.router.navigate(['/meals']), 1500);
    }, 800);
  }
}
