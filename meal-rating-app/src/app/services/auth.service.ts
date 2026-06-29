import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { User, AuthState } from '../models/models';
import { DataService } from './data.service';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private apiUrl = 'http://127.0.0.1:5000/api/auth';
  private authStateSubject = new BehaviorSubject<AuthState>({
    isLoggedIn: false,
    currentUser: null,
    token: null
  });

  authState$ = this.authStateSubject.asObservable();

  constructor(
  private http: HttpClient,
  private dataService: DataService,
  private router: Router
)  {
    this.restoreSession();
  }

  private restoreSession(): void {
    const saved = localStorage.getItem('authSession');
    if (saved) {
      const session = JSON.parse(saved);
      if (session.expiry > Date.now()) {
        this.authStateSubject.next({
          isLoggedIn: true,
          currentUser: session.user,
          token: session.token
        });
      } else {
        localStorage.removeItem('authSession');
      }
    }
  }

  login(email: string, password: string) {
  return this.http.post<any>(`${this.apiUrl}/login`, {
    email: email.toLowerCase().trim(),
    password
  }).pipe(
    tap(response => {
      const state: AuthState = {
        isLoggedIn: true,
        currentUser: response.user,
        token: response.token
      };

      this.authStateSubject.next(state);

      const session = {
        user: response.user,
        token: response.token,
        expiry: Date.now() + 24 * 60 * 60 * 1000
      };

      localStorage.setItem('authSession', JSON.stringify(session));
    })
  );
}

  logout(): void {
    localStorage.removeItem('authSession');
    this.authStateSubject.next({ isLoggedIn: false, currentUser: null, token: null });
    this.router.navigate(['/login']);
  }

  get isLoggedIn(): boolean {
    return this.authStateSubject.value.isLoggedIn;
  }

  get currentUser(): any {
    return this.authStateSubject.value.currentUser;
  }

  get isAdmin(): boolean {
    return this.currentUser?.role === 'admin';
  }
  get token(): string | null {
  return this.authStateSubject.value.token;
}
}
