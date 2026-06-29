import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  email = '';
  password = '';
  showPassword = false;
  loading = false;
  errorMessage = '';

  constructor(
    private auth: AuthService,
    private router: Router,
    public themeService: ThemeService
  ) {}

  onLogin(): void {
  if (!this.email || !this.password) {
    this.errorMessage = 'Please fill in all fields.';
    return;
  }

  this.loading = true;
  this.errorMessage = '';

  setTimeout(() => {
    this.auth.login(this.email, this.password).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage =
          err.error?.message || 'Invalid email or password.';
      }
    });
  }, 800);
}

  fillDemo(): void {
    this.email = 'demo@mealrating.com';
    this.password = 'Demo@123';
  }

  toggleTheme(): void {
    this.themeService.toggleTheme();
  }
}
