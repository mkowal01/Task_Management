from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_task, name='create_task'),
    path('<int:task_id>/add_step/', views.add_step, name='add_step'),
]
