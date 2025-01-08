from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/add_step/', views.add_step, name='add_step'),
    path('update-step/<int:step_id>/', views.update_step, name='update_step'),
    path('tasks/progress/', views.task_progress, name='task_progress'),
    path('tasks/<int:task_id>/detail/', views.task_detail, name='task_detail'),
    path('tasks/step/<int:step_id>/delete/', views.delete_step, name='delete_step'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
]
