import json
import time

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

GROUP_NAME = 'submit_{}'


class SubmitConsumer(AsyncWebsocketConsumer):
    registers = []

    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        for register in self.registers:
            await self.remove(register)
        await self.close(code)

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

    async def send_status(self, event):
        await self.send(text_data=event['message'])
        if 'close' in event:
            await self.remove(event['close'])
            pass

    async def remove(self, submit_id: int):
        await self.channel_layer.group_discard(
            GROUP_NAME.format(submit_id),
            self.channel_name
        )


async def update_status(submit_id: int, data: dict, close: bool):
    send_data = {
        'type': 'send_status',
        'message': json.dumps(data),
    }
    if close:
        send_data['close'] = submit_id

    await get_channel_layer().group_send(
        GROUP_NAME.format(submit_id),
        send_data
    )
