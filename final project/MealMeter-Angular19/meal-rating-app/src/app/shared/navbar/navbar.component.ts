import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { ThemeService } from '../../services/theme.service';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  menuOpen = false;
  userMenuOpen = false;

  constructor(
    public auth: AuthService,
    public themeService: ThemeService
  ) {}

  toggleMenu(): void { this.menuOpen = !this.menuOpen; }
  toggleUserMenu(): void { this.userMenuOpen = !this.userMenuOpen; }
  toggleTheme(): void { this.themeService.toggleTheme(); }
  logout(): void { this.auth.logout(); this.userMenuOpen = false; }
  closeMenus(): void { this.menuOpen = false; this.userMenuOpen = false; }

  get userInitial(): string {
    return this.auth.currentUser?.name?.charAt(0)?.toUpperCase() || 'U';
  }
}
