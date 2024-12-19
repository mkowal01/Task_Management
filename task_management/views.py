from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')  # Szablon w globalnym folderze templates
