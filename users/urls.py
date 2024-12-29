from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Strona główna
    path('register/', views.register, name='register'),  # Rejestracja
    path('login/', views.login_view, name='login'),  # Logowanie
    path('logout/', views.logout_view, name='logout'),  # Wylogowanie
]
