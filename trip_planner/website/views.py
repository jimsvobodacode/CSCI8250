from django.http import HttpResponse
from django.shortcuts import render

from website.forms import IndexForm
from website.agentic_ai import AgenticAI

def index(request):
    if request.method == "POST":
        form = IndexForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            ai = AgenticAI()
            ai.Process(prompt)
    else:
        form = IndexForm()
    return render(request, "index.html", {"form": form})


def about(request):
    return render(request, "about.html")


from django.shortcuts import redirect
def redirect_404(request, exception):
    return redirect("/")   # name of your home URL

