from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.utils.text import slugify

from .models import Room


@login_required
def index(request):
    """List all rooms and handle the "create or join a room" form."""
    error = None
    if request.method == "POST":
        # Turn whatever the user typed into a URL-safe name: "My Room!" -> "my-room"
        room_name = slugify(request.POST.get("room_name", ""))
        if room_name:
            return redirect("chat:room", room_name=room_name)
        error = "Please enter a room name using letters or numbers."

    rooms = Room.objects.all()
    return render(request, "chat/index.html", {"rooms": rooms, "error": error})


@login_required
def room(request, room_name):
    """Show one room with its recent history. The live part runs over WebSocket."""
    # Keep URLs canonical so they always match the WebSocket route ([\w-]+).
    slug = slugify(room_name)
    if not slug:
        return redirect("chat:index")
    if slug != room_name:
        return redirect("chat:room", room_name=slug)

    room_obj, _created = Room.objects.get_or_create(name=slug)

    # Grab the 50 newest messages, then flip them so they read oldest -> newest.
    recent = room_obj.messages.select_related("user").order_by("-created_at")[:50]
    messages = list(reversed(recent))

    return render(
        request,
        "chat/room.html",
        {"room_name": slug, "chat_messages": messages},
    )


def signup(request):
    """Register a new account with Django's built-in form, then log the user in."""
    if request.user.is_authenticated:
        return redirect("chat:index")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("chat:index")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
