from django.shortcuts import render

def login(request):
    return render(request, 'volt_ai_app/index.html')
