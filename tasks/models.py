from django.db import models
from django.conf import settings


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('to_do', 'To Do'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='to_do',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    def calculate_progress(self):
        steps = self.steps.all()
        total_steps = steps.count()
        if total_steps == 0:
            self.progress = 0
        else:
            completed_steps = steps.filter(is_completed=True).count()
            self.progress = (completed_steps / total_steps) * 100
            self.progress = round((completed_steps / total_steps) * 100, 2)  # Zaokrąglenie do 2 miejsc po przecinku
        self.save()
        return self.progress


class Step(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='steps')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Pole opisu kroku
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {'Completed' if self.is_completed else 'Pending'}"
