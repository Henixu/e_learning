import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'] // Ensure this is plural
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService) {}

  // Call login method on form submission
  onSubmit() {
    this.authService.login(this.email, this.password).subscribe(
      (response) => {
        console.log('Login successful:', response);
        // You can redirect or handle successful login here
      },
      (error) => {
        console.error('Login failed:', error);
        // Handle error, e.g., show an error message
      }
    );
  }
}
