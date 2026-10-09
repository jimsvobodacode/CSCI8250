import uuid
from django.shortcuts import render
from django.views.decorators.http import require_POST

from website.forms import IndexForm
from website.agentic_ai import AgenticAI

def index(request):
    form = IndexForm()
    return render(request, "index.html", {"form": form, "profile": None})


@require_POST
def aisession(request):
    form = IndexForm(request.POST)
    profile = None
    if form.is_valid():
        ai = AgenticAI()
        ai.Process(get_conversation_id(request), form.cleaned_data["prompt"])
        profile = ai.Profile
    return render(request, "results.html", {"form": form, "profile": profile})

@require_POST
def new_session(request):
    request.session.pop("agent_conversation_id", None)
    get_conversation_id(request)
    return redirect("/")


def get_conversation_id(request):
    conversation_id = request.session.get("agent_conversation_id")
    if not conversation_id:
        conversation_id = str(uuid.uuid4())
        request.session["agent_conversation_id"] = conversation_id
    return conversation_id


def about(request):
    return render(request, "about.html")


from django.shortcuts import redirect
def redirect_404(request, exception):
    return redirect("/")   # name of your home URL


# def process(request):
    # if request.method == "POST":
    #     pass
    # else:
    #     form = IndexForm()
    # return render(request, "index.html", {"form": form, "profile": None})



