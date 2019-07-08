import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class send_data(WebsocketConsumer):
    def connect(self):
        self.group_name = "connected_users"
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from group
    def receive_data(self, data):
        # Send message to WebSocket
        self.send(text_data=json.dumps(data))
