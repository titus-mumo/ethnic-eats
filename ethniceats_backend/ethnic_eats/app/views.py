from .serializers import UserLoginSerielizer
from django.contrib.auth import authenticate, login
from rest_framework import status
from urllib import request
from django.shortcuts import render
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.views import APIView

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from .serializers import GroupSerializer, CuisineGetSerializer, CuisinePostSerializer, UserReviewSerielizer, UserPostPostSerielizer, UserPostGetSerializer, UserReviewPostSerielizer, MealPostSerializer, MealGetSerializer, LocationDetailPostSerializer, LocationDetailGetSerializer, CuisineBasedMenuPostSerializer
from .models import Cuisine, UserPost, Reviews, MealModel, LocationDetail
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.tokens import RefreshToken


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]



# Post View
class UserPostView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        post_description = request.data.get('post_description')
        post = {}
        post['user'] = user.id
        post['post_description'] = post_description
        post_serializer = UserPostPostSerielizer(data = post)
        if post_serializer.is_valid():
            print("Data is serialized")
            post = UserPost.objects.create(
                post_description=post['post_description'], post_owner=user)
            serializer = UserPostGetSerializer(post, many=False)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        
    def get(self, requet):
        posts = UserPost.objects.all()
        serializer = UserPostGetSerializer(posts, many = True)
        return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe=False)

#Reviews View
class UserReviewClass(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def post(self, request, cuisine_id):
        cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
        review_data = {
            'cuisine': cuisine.cuisine_id,
            'review': request.data.get('review'),
            'name': request.data.get('name')
        }
        serializer = UserReviewPostSerielizer(data=review_data)
        if serializer.is_valid():
            saved_data = Reviews.objects.create(
                review=review_data['review'], cuisine = cuisine)
            serializer = UserReviewSerielizer(saved_data, many=False)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def get(self, request, cuisine_id):
        cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
        reviews = Reviews.objects.filter(cuisine = cuisine)
        serializer = UserReviewSerielizer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#Cuisine View
class CuisineView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if User.objects.filter(id=user.id).exists():
            data = request.data
            print('data')
            name = data.get('name')
            description = data.get('description')
            address = data.get('address')
            contact = data.get('contact')
            website = data.get('website')
            time_open = data.get('time_open')
            # cuisine_data = {}
            # cuisine_data['name'] = name
            # cuisine_data['description'] = description
            # cuisine_data['address'] = address
            # cuisine_data['contact'] = contact
            # cuisine_data['website'] = website
            # cuisine_data['time_open'] = time_open
            cuisine_serializer = CuisinePostSerializer(data = data)
            if cuisine_serializer.is_valid():
                cuisine = Cuisine.objects.create(user = user, name = name, description = description, contact = contact, address = address, website = website, time_open = time_open)
                serialized_cuisine = CuisineGetSerializer(cuisine, many=False)
                return JsonResponse(serialized_cuisine.data, status = status.HTTP_201_CREATED, safe = False)
            return JsonResponse(cuisine_serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)
        return JsonResponse({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        user = request.user
        cuisines = Cuisine.objects.all()
        serialized_cuisines = CuisineGetSerializer(cuisines, many = True)
        return JsonResponse(serialized_cuisines.data, status = status.HTTP_200_OK, safe = False)


#Meals View

class MealView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        cuisine = Cuisine.objects.filter(name = data.get('cuisine_name')).first()
        cuisine = cuisine.cuisine_id
        meal_name = data.get('meal_name')
        price = data.get('price')
        category = data.get('category')
        meal_data = {}
        meal_data['cuisine'] = cuisine
        meal_data['meal_name'] = meal_name
        meal_data['price'] = price
        meal_data['category'] = category
        serializer = MealPostSerializer(data = meal_data)
        if serializer.is_valid():
            meal =  MealModel.objects.create(cuisine = cuisine, meal_name = meal_name, price = price, category = category)
            serialized_response = MealGetSerializer(meal, many = False)
            return JsonResponse(serialized_response.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        meals = MealModel.objects.all()
        serialized_meals = MealGetSerializer(meals, many=True)
        return JsonResponse(serialized_meals.data, status=status.HTTP_200_OK, safe=False)

#Location View Detail
class LocationDetailView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        address = data.get('address')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        location_detail = {}
        location_detail['address'] = address
        location_detail['latitude'] = latitude
        location_detail['longitude'] = longitude
        serializer = LocationDetailPostSerializer(data = location_detail, many = False)
        if serializer.is_valid():
            location_detail = LocationDetail.objects.create(address = address, latitude = latitude, longitude = longitude)
            serialized_location_detail = LocationDetailGetSerializer(location_detail, many = False)
            return JsonResponse(serialized_location_detail.data, status = status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        location_detail = LocationDetail.objects.all()
        serialized_location_detail = LocationDetailGetSerializer(location_detail, many = True)
        return JsonResponse(serialized_location_detail.data, status = status.HTTP_200_OK, safe=False)
        
# Menus related to a specific Restaurants
class CuisineBasedMenuView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
            if not cuisine:
                return JsonResponse({"massage": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status = status.HTTP_404_NOT_FOUND)
        
        try:
            meals = MealModel.objects.filter(cuisine_id = cuisine)
            serializer = MealGetSerializer(meals, many = True)
            return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe = False)
        except MealModel.DoesNotExist:
            return JsonResponse({"message" : "Meals specific for this restaurant not found"})
        
    def post(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
            if not cuisine:
                return JsonResponse({"massage": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status = status.HTTP_404_NOT_FOUND)
        data = request.data
        meal_serializer = CuisineBasedMenuPostSerializer(data = data, many = False)
        if meal_serializer.is_valid():
            try:
                meal_info = MealModel.objects.create(cuisine_id = cuisine, meal_name = data.get("meal_name"), price = data.get("price"), category = data.get("category"))
                serialized_data = MealGetSerializer(meal_info, many = False)
                return JsonResponse(serialized_data.data, status = status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"message": "Integrity Error"}, status = status.HTTP_404_NOT_FOUND)
        return JsonResponse(meal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class GetSpecificCuisineView(APIView):
    def get(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id=cuisine_id).first()
            if not cuisine:
                return JsonResponse({"massage": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_data = CuisineGetSerializer(cuisine)
        return JsonResponse(serialized_data.data, status = status.HTTP_200_OK, safe = False)
        
         
