from django.contrib import admin
from django.urls import path, include
from .views import set_csrf_token, createPost

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('index/', views.index, name='index'),
    path('set-csrf-token/', set_csrf_token),
    path('createPost/', views.createPost, name='createPost'),
]
