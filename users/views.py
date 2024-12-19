from django.http import JsonResponse

def example_view(request):
    return JsonResponse({'message': 'Example view from users app'})
