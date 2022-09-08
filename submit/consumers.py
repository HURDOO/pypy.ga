from channels.generic.websocket import AsyncWebsocketConsumer

ROOM_GROUP_NAME = 'test'


class SubmitConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            ROOM_GROUP_NAME,
            self.channel_name
        )
        await self.accept()

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
