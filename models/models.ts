export interface Meal {
  id: any;
  name: any;
  restaurant: any;
  category: any;
  image: any;
  description: any;
  ratings: any[];
  addedBy: any;
  createdAt: any;
  averageRating?: any;
  performanceCategory?: 'top' | 'moderate' | 'low';
}

export interface User {
  id: string;
  name: string;
  email: string;
  password: string;
  role: 'admin' | 'user';
  avatar: string;
  joinedAt: string;
}

export interface Restaurant {
  id: string;
  name: string;
}

export interface AppData {
  meals: Meal[];
  users: User[];
  restaurants: Restaurant[];
  categories: string[];
}

export interface AuthState {
  isLoggedIn: boolean;
  currentUser: User | null;
  token: string | null;
}

export interface RatingSubmission {
  mealId: string;
  rating: number;
  userId: string;
}
