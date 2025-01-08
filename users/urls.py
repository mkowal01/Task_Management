from django.urls import path
from . import views
from .views import under_construction

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Strona główna
    path('register/', views.register, name='register'),  # Rejestracja
    path('login/', views.login_view, name='login'),  # Logowanie
    path('logout/', views.logout_view, name='logout'),  # Wylogowanie
    path('features/', under_construction, name='features'),  # Strona w budowie dla "Features"
    path('pricing/', under_construction, name='pricing'),  # Strona w budowie dla "Pricing"
]
