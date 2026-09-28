from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("csci 8250 - trip planner")
