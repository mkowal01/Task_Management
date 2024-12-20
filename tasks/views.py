from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def dashboard(request):
    # Pobranie tasków użytkownika
    tasks = Task.objects.filter(user=request.user)

    # Obliczanie procentu ukończenia każdego taska
    for task in tasks:
        task.completion_percentage = int((task.completed_steps / task.total_steps) * 100) if task.total_steps > 0 else 0

    return render(request, 'dashboard.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        total_steps = int(request.POST.get('total_steps', 0))

        # Tworzenie nowego taska
        Task.objects.create(
            user=request.user,
            name=name,
            description=description,
            total_steps=total_steps,
            completed_steps=0  # Domyślnie task zaczyna się od 0
        )
        return redirect('dashboard')

    return render(request, 'create_task.html')
