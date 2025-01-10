# app/views.py
from django.http import HttpResponse

def root_view(request):
    return HttpResponse("Welcome to the API!")
