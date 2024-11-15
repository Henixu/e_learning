import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor() { }

  // Set user data in localStorage
  setUser(userData: any) {
    localStorage.setItem('user', JSON.stringify(userData)); // Store as string
  }

  // Get user data from localStorage
  getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null; // Parse and return user data or null if not available
  }

  // Remove user data from localStorage (e.g., on logout)
  removeUser() {
    localStorage.removeItem('user');
  }
}
