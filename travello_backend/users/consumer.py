import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage,Usermodels
from asgiref.sync import sync_to_async

class TravelChat(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        sender_id = data.get('sender_id') 
        receiver_id = data.get('receiver_id')  
        # Save message to database
        await self.save_message(sender_id, receiver_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
                
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        try:
            sender = Usermodels.objects.get(id=sender_id)
        except Usermodels.DoesNotExist:
            print(f"Sender with ID {sender_id} does not exist")
          
        try:
            receiver = Usermodels.objects.get(id=receiver_id)
        except Usermodels.DoesNotExist:
            print(f"Receiver with ID {receiver_id} does not exist")
            return
        ChatMessage.objects.create(sender=sender, receiver=receiver, message=message)

  