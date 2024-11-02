from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import get_user_model
@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        # Find the user by email
        User = get_user_model()  # Get the User model
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        # Authenticate user
        if user.check_password(password):  # Check if the password is correct
            login(request, user)
            return JsonResponse({'message': 'Login successful', 'user_id': user.id}, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        # Parse the JSON data
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Check if all fields are provided
        if not username or not password:
            return JsonResponse({'error': 'Username and password are required'}, status=400)

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=409)

        try:
            # Create a new user
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return JsonResponse({'message': 'User registered successfully', 'user_id': user.id}, status=201)
        except IntegrityError:
            return JsonResponse({'error': 'Failed to create user'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
