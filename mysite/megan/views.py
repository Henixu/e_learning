from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from .models import Recommendation, UserProgress 

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            # Parsing JSON data from the frontend
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Check required fields
        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        # Retrieve the user model
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        # Verify the password
        if user.check_password(password):
            login(request, user)

            # Fetch user-specific recommendations and progress by user ID
            recommendations = list(Recommendation.objects.filter(utilisateur_id=user.id).values()) or []
            progress = list(UserProgress.objects.filter(utilisateur_id=user.id).values()) or []

            # Fetch courses assigned to the user with progress details
            courses = []
            for progress_item in progress:
                course = progress_item['cours']  # Assuming 'cours' is a ForeignKey to Course
                course_details = {
                    'course_id': course.id,
                    'course_title': course.titre,
                    'course_description': course.description,
                    'progress': progress_item['progression'],
                    'status': progress_item['statut']
                }
                courses.append(course_details)

            # Prepare response data for the Angular frontend
            response_data = {
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'recommendations': recommendations,
                'progress': progress,
                'courses': courses  # Adding the list of courses to the response data
            }
            return JsonResponse(response_data, status=200)
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
# @csrf_exempt
# def login_view(request):
#     if request.method == 'POST':
#         try:
#             # Parsing JSON data from the frontend
#             data = json.loads(request.body)
#             email = data.get('email')
#             password = data.get('password')
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON format'}, status=400)

#         # Check required fields
#         if not email or not password:
#             return JsonResponse({'error': 'Email and password are required'}, status=400)

#         # Retrieve the user model
#         User = get_user_model()
#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'Invalid email or password'}, status=401)

#         # Verify the password
#         if user.check_password(password):
#             login(request, user)

#             # Fetch user-specific recommendations and progress by user ID
#             recommendations = list(Recommendation.objects.filter(utilisateur_id=user.id).values()) or []
#             progress = list(UserProgress.objects.filter(utilisateur_id=user.id).values()) or []

#             # Prepare response data for the Angular frontend
#             response_data = {
#                 'message': 'Login successful',
#                 'user_id': user.id,
#                 'username': user.username,
#                 'email': user.email,
#                 'recommendations': recommendations,
#                 'progress': progress
#             }
#             return JsonResponse(response_data, status=200)
#         else:
#             return JsonResponse({'error': 'Invalid email or password'}, status=401)

#     return JsonResponse({'error': 'Invalid request method'}, status=405)
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
