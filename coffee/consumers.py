from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from datetime import datetime
import asyncio


class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "notification"
        self.room_group_name = "notification_group"

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.send(text_data=json.dumps({
            'status': "connected"
        }))

    # sends a message when it receives something
    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({'status': 'receive'}))

    def disconnect(self, *args, **kwargs):
        print("disconnected")

    def send_notification(self, text_data):
        notification_data = (json.loads(text_data.get('value')))

        self.send(text_data=json.dumps({
            'status': "notification",
            'value': notification_data
        }))


class TimeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.get_time()

    async def get_time(self):
        while True:
            now = datetime.now()
            time = now.strftime("%I:%M %p")
            await self.send(json.dumps({'time': time}))
            await asyncio.sleep(1)

    def disconnect(self, close_code):
        self.disconnect()


class TrackConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "track"
        self.room_group_name = "track_group"

        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.send(text_data=json.dumps({
            'status': "connected"
        }))

    def send_track(self, text_data):
        trackOrder = (json.loads(text_data.get('value')))

        self.send(text_data=json.dumps({
            "status": "track_order",
            "value": trackOrder
        }))
