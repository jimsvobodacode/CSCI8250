from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, "index.html", {"message": "csci 8250 - trip planner"})
    # return HttpResponse("csci 8250 - trip planner")



def about(request):
    return render(request, "about.html")

