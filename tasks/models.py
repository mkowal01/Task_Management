from django.db import models
from django.conf import settings


class Task(models.Model):
    name = models.CharField(max_length=255)  # Nazwa zadania
    description = models.TextField(blank=True, null=True)  # Opis zadania (opcjonalny)
    deadline = models.DateField(null=True, blank=True)  # Termin realizacji
    status = models.CharField(
        max_length=20,
        choices=[
            ('to_do', 'To Do'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
        ],
        default='to_do',
    )  # Status zadania
    progress = models.IntegerField(default=0)  # Postęp w procentach (0-100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Wskazanie na model użytkownika
        on_delete=models.CASCADE,  # Usunięcie użytkownika powoduje usunięcie jego zadań
        related_name='tasks'  # Dodanie odwrotnego dostępu z poziomu użytkownika
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Data utworzenia
    updated_at = models.DateTimeField(auto_now=True)  # Data ostatniej aktualizacji

    def __str__(self):
        return f"{self.name} ({self.status})"
