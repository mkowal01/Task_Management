from django.shortcuts import render
from .models import Notification
from django.contrib.auth.decorators import login_required


@login_required
def list_notifications(request):
    # Pobierz powiadomienia dla zalogowanego użytkownika
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notification_list.html', {'notifications': notifications})
