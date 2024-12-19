from django.urls import path
from . import views  # Import widoków z aplikacji users

urlpatterns = [
    # Przykładowy widok (trzeba dodać widok w `users/views.py`)
    path('example/', views.example_view, name='example_view'),
]
