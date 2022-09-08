import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

ROOM_GROUP_NAME = 'test'


class SubmitConsumer(WebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            ROOM_GROUP_NAME,
            self.channel_name
        )
        self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            ROOM_GROUP_NAME,
            self.channel_name
        )
        pass

    async def receive(self, text_data):
        print(text_data)

        await self.channel_layer.group_send(
            ROOM_GROUP_NAME,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=event['message'])
