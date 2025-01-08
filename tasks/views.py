from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Task, Step


def dashboard(request):
    # Pobieranie zadań użytkownika
    tasks = Task.objects.filter(user=request.user)

    # Obliczanie postępu dla każdego zadania
    for task in tasks:
        task.progress = task.calculate_progress()  # Dynamiczne obliczanie postępu

    # Pobieranie wybranego zadania (jeśli użytkownik kliknął szczegóły)
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
        total_steps = int(request.POST.get('total_steps', 0))  # Pobierz liczbę kroków z formularza
        task = Task.objects.create(name=name, description=description, user=request.user)

        # Tworzenie domyślnych kroków dla zadania
        for i in range(1, total_steps + 1):
            Step.objects.create(task=task, name=f"Step {i}", description=f"Description for Step {i}")

        return redirect('dashboard')
    return render(request, 'create_task.html')


def add_step(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')  # Pobieranie opisu kroku
        Step.objects.create(task=task, name=name, description=description)  # Tworzenie nowego kroku
        return redirect('task_detail', task_id=task.id)  # Przekierowanie z powrotem na szczegóły zadania
    return render(request, 'add_step.html', {'task': task})


def update_step(request, step_id):
    step = get_object_or_404(Step, id=step_id, task__user=request.user)
    if request.method == 'POST':
        step.is_completed = 'is_completed' in request.POST
        step.save()

        # Oblicz dynamiczny postęp zadania
        task = step.task
        task.progress = task.calculate_progress()
        task.save()

        # Zwróć wynik jako JSON (do obsługi AJAX lub dynamicznego odświeżania)
        return JsonResponse({'task_id': task.id, 'progress': task.progress})
    return redirect('dashboard')


def task_progress(request):
    tasks = Task.objects.filter(user=request.user)
    progress_data = [
        {"id": task.id, "progress": task.calculate_progress()}
        for task in tasks
    ]
    return JsonResponse(progress_data, safe=False)


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    steps = task.steps.all()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'edit_step':
            step_id = request.POST.get('step_id')
            step = get_object_or_404(Step, id=step_id, task=task)
            step.description = request.POST.get('description', step.description)
            step.is_completed = 'is_completed' in request.POST
            step.save()
            task.calculate_progress()
            return redirect('task_detail', task_id=task.id)

        elif action == 'add_step':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            Step.objects.create(task=task, name=name, description=description)
            task.calculate_progress()
            return redirect('task_detail', task_id=task.id)

    return render(request, 'task_detail.html', {'task': task, 'steps': steps})


def delete_step(request, step_id):
    step = get_object_or_404(Step, id=step_id, task__user=request.user)
    task = step.task
    step.delete()
    task.calculate_progress()
    return redirect('task_detail', task_id=task.id)


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()  # Usuwa zadanie i automatycznie powiązane kroki (kaskadowe usuwanie)
        return redirect('dashboard')  # Przekierowanie na dashboard
