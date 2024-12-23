import json

from django.shortcuts import get_object_or_404
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import (Message, ChatGroup)


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.group_name = None
        self.user = None

    async def connect(self):
        # we take the group name from the url that is sent to this consumer
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.user = self.scope['user']
        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        if text_data:
            data = json.loads(text_data)
            gp_name = await ChatGroup.objects.aget(unique_code=self.group_name)
            # here we create the message that user has been sent to the group
            await Message.objects.acreate(sender=self.user, chat_group=gp_name, message=data['message'])

            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'data': {
                        'message': data['message'],
                        'sender': self.user.username.capitalize()
                    }
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event['data']))
