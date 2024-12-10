"""
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Relief Network!")

from django.shortcuts import render

def home(request):
    return render(request, 'templates\home.html')
"""