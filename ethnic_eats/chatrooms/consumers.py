import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage
from app.models import Cuisine


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        print(f"Connecting to room: {self.room_name}")
        print(f"Group name: {self.room_group_name}")

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f"Disconnecting from room: {self.room_name}")
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        print(f"Received message: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']

        # Save message to database
        room = await database_sync_to_async(ChatRoom.objects.get)(room=self.room_name)
        await database_sync_to_async(ChatMessage.objects.create)(room=room, message=message, user=user)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    async def chat_message(self, event):
        print(f"Sending message to WebSocket: {event['message']}")
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))




class SearchCuisineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        search_query = data.get('search_query', '')

        # Filter cuisines based on the search query
        filtered_cuisines = await self.filter_cuisines(search_query)

        # Send filtered cuisines back to the client
        await self.send(text_data=json.dumps({'cuisines': filtered_cuisines}))

    @database_sync_to_async
    def filter_cuisines(self, search_query):
        # Use Django ORM to filter cuisines based on the search query
        if search_query:
            return list(Cuisine.objects.filter(name__icontains=search_query).values_list('cuisine_id', 'name'))
        else:
            return list(Cuisine.objects.values_list('cuisine_id', 'name'))
