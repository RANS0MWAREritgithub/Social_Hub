from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
import logging
from django.shortcuts import render
from .models import Post, Video, Picture
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@ensure_csrf_cookie
def set_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

@ensure_csrf_cookie
def index(request):
    return render(request, 'index.html')

logger = logging.getLogger(__name__)

from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        logger.info(f"CSRF Token: {request.META.get('CSRF_COOKIE')}")
        try:
            data = json.loads(request.body)
            user_model = get_user_model()
            user = user_model.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password']
            )
            user.save()
            return JsonResponse({'message': 'Registration successful'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not email or not password:
                return JsonResponse({'error': 'Please provide both email and password'}, status=400)

            user = authenticate(request, username=email, password=password)

            if user is not None:
                auth_login(request, user)
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def createPost(request):
    if request.method == 'POST':
        user = request.user
        content = request.data.get('content')
        post = Post.objects.create(user=user, content=content)
        
        # Handle video and image files
        for video in request.FILES.getlist('video_files'):
            Video.objects.create(post=post, video_file=video)
        
        for image in request.FILES.getlist('image_files'):
            Picture.objects.create(post=post, image_file=image)
        
        return Response({'message': 'Post created successfully'}, status=201)
    return Response({'error': 'Invalid request method'}, status=405)