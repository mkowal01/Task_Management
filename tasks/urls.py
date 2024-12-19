from django.urls import path
from . import views

urlpatterns = [
    path('<int:project_id>/', views.list_tasks, name='list_tasks'),
    path('<int:project_id>/<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:project_id>/create/', views.create_task, name='create_task'),
]
