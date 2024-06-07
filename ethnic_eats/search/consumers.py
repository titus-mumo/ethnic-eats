# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from app.models import Cuisine

class CuisineConsumer(AsyncWebsocketConsumer):
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
            return list(Cuisine.objects.filter(name__icontains=search_query).values_list('name', flat=True))
        else:
            return list(Cuisine.objects.values_list('name', flat=True))
