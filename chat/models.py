from django.conf import settings
from django.db import models


class Room(models.Model):
    """A chat room, identified by a URL-safe name such as "general"."""

    name = models.SlugField(unique=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Message(models.Model):
    """One chat message posted by a user in a room."""

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]  # oldest first, like a chat log

    def __str__(self):
        return f"{self.user}: {self.content[:40]}"
