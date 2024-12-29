from django.shortcuts import render, get_object_or_404, redirect
# from django.http import HttpResponseForbidden
from .models import Task, Step


def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    task_id = request.GET.get('task_id')
    selected_task = None

    if task_id:
        selected_task = get_object_or_404(Task, id=task_id, user=request.user)

    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'selected_task': selected_task,
    })


def create_task(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST.get('description', '')
        Task.objects.create(name=name, description=description, user=request.user)
        return redirect('dashboard')
    return render(request, 'create_task.html')


def add_step(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        Step.objects.create(task=task, name=name)
        return redirect('dashboard')
    return render(request, 'add_step.html', {'task': task})


def update_step(request, step_id):
    step = get_object_or_404(Step, id=step_id, task__user=request.user)
    if request.method == 'POST':
        step.is_completed = 'is_completed' in request.POST
        step.save()
        # Automatyczna aktualizacja postępu zadania
        task = step.task
        total_steps = task.steps.count()
        completed_steps = task.steps.filter(is_completed=True).count()
        task.progress = (completed_steps / total_steps) * 100 if total_steps > 0 else 0
        task.save()
    return redirect('dashboard')
