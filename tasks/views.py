from django.shortcuts import render, get_object_or_404, redirect
from .models import Task
from projects.models import Project
from django.contrib.auth.decorators import login_required


@login_required
def list_tasks(request, project_id):
    # Pobierz projekt, upewniając się, że użytkownik jest członkiem projektu
    project = get_object_or_404(Project, id=project_id, members=request.user)
    tasks = project.tasks.all()
    return render(request, 'task_list.html', {'project': project, 'tasks': tasks})


@login_required
def task_detail(request, project_id, task_id):
    # Pobierz szczegóły zadania
    project = get_object_or_404(Project, id=project_id, members=request.user)
    task = get_object_or_404(Task, id=task_id, project=project)
    return render(request, 'task_detail.html', {'task': task})


@login_required
def create_task(request, project_id):
    # Pobranie projektu, do którego przypisane będzie zadanie
    project = get_object_or_404(Project, id=project_id, members=request.user)

    if request.method == "POST":
        # Pobierz dane z formularza
        name = request.POST.get('name')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')

        # Walidacja
        if not name or not description or not deadline:
            return render(request, 'task_create.html', {
                'project': project,
                'error': "Wszystkie pola są wymagane!"
            })

        # Tworzenie nowego zadania
        Task.objects.create(
            name=name,
            description=description,
            deadline=deadline,
            project=project
        )

        # Przekierowanie do listy zadań po utworzeniu
        return redirect('list_tasks', project_id=project.id)

    # Renderowanie formularza w przypadku GET
    return render(request, 'task_create.html', {'project': project})
