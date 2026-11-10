import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message, Room

MAX_MESSAGE_LENGTH = 1000


class ChatConsumer(AsyncWebsocketConsumer):
    """One instance of this class runs per open browser WebSocket."""

    async def connect(self):
        # AuthMiddlewareStack (see config/asgi.py) puts the logged-in user here.
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()  # anonymous users may not chat
            return

        # The room name comes from the URL: ws/chat/<room_name>/
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.group_name = f"chat_{self.room_name}"

        # Join the room's group so we receive everyone's messages.
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # group_name is only set if connect() got far enough to join a group.
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        """Called when the browser sends us a message."""
        try:
            data = json.loads(text_data or "")
        except json.JSONDecodeError:
            return  # ignore garbage

        content = str(data.get("message", "")).strip()
        if not content or len(content) > MAX_MESSAGE_LENGTH:
            return  # ignore empty or oversized messages

        message = await self.save_message(content)

        # Broadcast to everyone in the room (including the sender).
        # "type": "chat.message" makes Channels call self.chat_message() on each consumer.
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "username": self.user.username,
                "content": message.content,
                "timestamp": message.created_at.isoformat(),
            },
        )

    async def chat_message(self, event):
        """Called once per consumer in the group for every group_send above."""
        await self.send(
            text_data=json.dumps(
                {
                    "username": event["username"],
                    "content": event["content"],
                    "timestamp": event["timestamp"],
                }
            )
        )

    @database_sync_to_async
    def save_message(self, content):
        # The Django ORM is synchronous, so it runs in a worker thread.
        room, _created = Room.objects.get_or_create(name=self.room_name)
        return Message.objects.create(room=room, user=self.user, content=content)
