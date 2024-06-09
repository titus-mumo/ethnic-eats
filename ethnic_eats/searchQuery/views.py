from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.http import JsonResponse
from app.models import Cuisine
from app.serializers import CuisineGetSerializer

# Create your views here.

class SearchQuery(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, searchTerm):
        searchTerm = str(searchTerm).strip()
        if not searchTerm:
            return JsonResponse({"error": "Search term is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        cuisines = Cuisine.objects.filter(name__icontains=searchTerm)
        if cuisines.exists():
            serializer = CuisineGetSerializer(cuisines, many=True)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe = False)
        else:
            return JsonResponse({"message": "No matching cuisines found"}, status = status.HTTP_404_NOT_FOUND)