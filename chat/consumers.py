import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from users.models import Profile
from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope["user"]

        if user.is_authenticated:
            try:
                profile = await self.get_profile(user)
                username = f"{profile.firstname} {profile.lastname}"
            except Profile.DoesNotExist:
                username = user.username
        else:
            username = "Guest"

        await self.channel_layer.group_add("chat", self.channel_name)
        await self.accept()

        await self.channel_layer.group_send(
            "chat",
            {
                "type": "chat_message",
                "message": f"{username} joined the chat",
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("chat", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "").strip()

        user = self.scope["user"]
        if user.is_authenticated:
            try:
                profile = await self.get_profile(user)
                sender = f"{profile.firstname} {profile.lastname}"
                await self.save_message(profile, message)
            except Profile.DoesNotExist:
                sender = user.username
        else:
            sender = "Guest"

        if message:
            await self.channel_layer.group_send(
                "chat",
                {
                    "type": "chat_message",
                    "message": f"{sender}: {message}",
                }
            )

    async def chat_message(self, event):
        """Обязательный метод: отправляет сообщение клиенту"""
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))

    @database_sync_to_async
    def get_profile(self, user):
        return Profile.objects.get(user=user)

    @database_sync_to_async
    def save_message(self, profile, content):
        return Message.objects.create(sender=profile, content=content)
