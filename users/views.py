from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


def homepage(request):
    return render(request, 'homepage.html')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Używamy Twojego formularza
        if form.is_valid():
            user = form.save()
            login(request, user)  # Logowanie użytkownika po rejestracji
            return redirect('dashboard')  # Przekierowanie na dashboard
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Przekierowanie na dashboard
            return redirect('dashboard')  # 'dashboard' to nazwa widoku lub URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('homepage')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


def under_construction(request):
    return render(request, 'under_construction.html')
