import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';
@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  username: string = '';
  email: string = '';
  password: string = '';

  constructor(private authService: AuthService) {}

  onSubmit() {
    this.authService.register(this.username, this.email, this.password).subscribe(
      (response) => {
        console.log('Registration successful:', response);
        
      },
      (error) => {
        console.error('Registration failed:', error);
        
      }
    );
  }
}
