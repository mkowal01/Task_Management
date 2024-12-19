from django.shortcuts import render, get_object_or_404, redirect
from .models import Project
from django.contrib.auth.decorators import login_required


@login_required
def list_projects(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'project_list.html', {'projects': projects})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, members=request.user)
    return render(request, 'project_detail.html', {'project': project})


@login_required
def create_project(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        project = Project.objects.create(name=name, description=description, owner=request.user)
        project.members.add(request.user)
        return redirect('list_projects')
    return render(request, 'project_create.html')
