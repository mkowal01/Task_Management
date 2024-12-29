from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),  # Import ścieżek z aplikacji users
    path('projects/', include('projects.urls')),  # Import ścieżek z aplikacji projects
    path('tasks/', include('tasks.urls')),  # Import ścieżek z aplikacji tasks
    path('notifications/', include('notifications.urls')),  # Import ścieżek z aplikacji notifications
    path('', lambda request: redirect('homepage'), name='root'),  # Przekierowanie na homepage
]
