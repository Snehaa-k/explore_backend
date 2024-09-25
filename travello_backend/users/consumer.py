import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from urllib.parse import urlparse, parse_qs
import json
from .models import ChatMessages,Usermodels
from asgiref.sync import sync_to_async

class TravelChat(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope.get('query_string', b'').decode('utf-8')
        query_params = parse_qs(query_string)

        if query_params.get('receiver_id', [None])[0] == "null":
            self.room_group_name = None
        else:
            try:
                user_id = int(query_params.get('user_id', [None])[0])
                receiver_id = int(query_params.get('receiver_id', [None])[0])

                if user_id > receiver_id:
                    self.room_name = f'{user_id}_{receiver_id}'
                else:
                    self.room_name = f'{receiver_id}_{user_id}'

                self.room_group_name = 'chat_%s' % self.room_name

                await self.channel_layer.group_add(
                    self.room_group_name,
                    self.channel_name
                )
                await self.accept()

                # Send a JSON message indicating successful connection
                await self.send(text_data=json.dumps({
                    'type': 'connection',
                    'room_group_name': self.room_group_name
                }))
            except (TypeError, IndexError):
                await self.close(code=4000)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        userId = text_data_json['sender_id']
        receiver_id = text_data_json['receiver_id']
        
        await self.save_message(userId, receiver_id, message, self.room_group_name)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': userId,
                'receiver': receiver_id
            }
        )

    async def chat_message(self, event):
        content = event['message']
        sender = event['sender']
        receiver = event['receiver']
        
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'content': content,
            'sender': sender,
            'receiver': receiver
        }))


    @database_sync_to_async
    def save_message(self, sender, receiver, message,thread):
        
        try:
            sender = Usermodels.objects.get(id=sender)
            print(sender)
        except Usermodels.DoesNotExist:
            print(f"Sender with ID {sender} does not exist")
          
        try:
            receiver = Usermodels.objects.get(id=receiver)
        except Usermodels.DoesNotExist:
            print(f"Receiver with ID {receiver} does not exist")
            return
        ChatMessages.objects.create(sender = sender.id,receiver = receiver.id,content = message,thread_name= thread) 


  