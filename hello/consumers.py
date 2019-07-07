import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from threading import Thread
from simulation import environment



class send_data(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })
        await self.send({
            "type": "websocket.send",
            "text": json.dumps(["Hello world"])
        })
        env_playground = environment()
        while True:
            await asyncio.sleep(0.1)
            env_playground.update()
            data = env_playground.send_update()

            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(data)
            })


       

    async def websocket_receive(self,event):
        print("received", event)

    async def websocket_disconnect(self,event):
        print("disconnected", event)