# chat/consumers.py
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import unquote


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name_encoded = self.scope["url_route"]["kwargs"]["room_name_encoded"]
        self.room_name = unquote(self.room_name_encoded)
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room groupㄹ
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user_name = self.scope["user"].username  # 사용자 이름 가져오기

        # Send message to room group with user name
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": f"{user_name}: {message}"}
        )
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))