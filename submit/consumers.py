import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

GROUP_NAME = 'submit_{}'


class SubmitConsumer(AsyncWebsocketConsumer):
    registers = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        for register in self.registers:
            await self.channel_layer.group_discard(
                GROUP_NAME.format(register),
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if 'register' not in data:
            await self.disconnect(0)
            return
        register = data['register']
        # submit = Submit.objects.get(id=int(data['submit_id']))
        # if submit.result not in [ResultType.PREPARE, ResultType.ONGOING]:
        #     await self.send_status({
        #         'result': submit.result
        #     })
        self.registers.append(register)
        await self.channel_layer.group_add(
            GROUP_NAME.format(register),
            self.channel_name
        )
        await self.send('registered to ' + str(register))

    async def send_status(self, event):
        await self.send(text_data=event['message'])
        if bool(event['close']):
            # await self.disconnect(1000)
            print(event['close'])


async def update_status(submit_id: int, data: dict, close: bool):
    await get_channel_layer().group_send(
        GROUP_NAME.format(submit_id),
        {
            'type': 'send_status',
            'message': json.dumps(data),
            'close': str(close)
        }
    )
