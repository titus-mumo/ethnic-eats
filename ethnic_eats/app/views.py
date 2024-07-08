#normal imports
from rest_framework import status, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from .serializers import GroupSerializer, CuisineGetSerializer, CuisinePostSerializer, MealPostSerializer, MealGetSerializer, LocationDetailPostSerializer, LocationDetailGetSerializer, CuisineBasedMenuPostSerializer, MealAndRatingSerializer, CuisineAndLocationDetailSerializer
from .models import Cuisine, MealModel, LocationDetail, Ratings
from django.http import JsonResponse
import json

#ML imports
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from django.db.models import Avg

from django.db.models import F, Func, FloatField

from django.db import models

import math


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

def greetings(request):
    return JsonResponse({"greetings": "Hello"})

#Cuisine View
class CuisineView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if User.objects.filter(id=user.id).exists():
            data = request.data
            name = data.get('name')
            description = data.get('description')
            location = data.get('location')
            address = data.get('address')
            contact = data.get('contact')
            website = data.get('website')
            time_open = data.get('time_open')
            time_close = data.get('time_close')
            cuisine_pic = data.get('cuisine_pic' )

            location_geometry = json.loads(data.get('location_geometry'))
            latitude = location_geometry['latitude']
            print(latitude)
            longitude = location_geometry['longitude']

            cuisine_data = dict()

            cuisine_data['name'] = name
            cuisine_data['description'] = description
            cuisine_data['location'] = location
            cuisine_data['address'] = address
            cuisine_data['contact'] = contact
            cuisine_data['website'] = website
            cuisine_data['time_open'] = time_open
            cuisine_data['time_close'] = time_close
            cuisine_data['cuisine_pic'] = cuisine_pic

            if Cuisine.objects.filter(name = name).exists():
                return JsonResponse({"error": "A cuisine with the same name already exists"}, status = status.HTTP_400_BAD_REQUEST, safe=False)
            
            cuisine_serializer = CuisinePostSerializer(data = cuisine_data)
            if cuisine_serializer.is_valid():
                cuisine = Cuisine.objects.create(user = user, name = name, description = description, location=location,  contact = contact, address = address, website = website, time_open = time_open, time_close = time_close, cuisine_pic = cuisine_pic)
                location = LocationDetail.objects.create(cuisine = cuisine, address=name, latitude= latitude, longitude=longitude)
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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        cuisine = Cuisine.objects.filter(cuisine_id = data.get('cuisine_id')).first()
        meal_name = data.get('meal_name')
        price = data.get('price')
        category = data.get('category')
        meal_pic = data.get('meal_pic')
        meal_data = {}
        meal_data['cuisine'] = cuisine.cuisine_id
        meal_data['meal_name'] = meal_name
        meal_data['price'] = price
        meal_data['category'] = category
        meal_data['meal_pic'] = meal_pic
        if MealModel.objects.filter(meal_name = meal_name, cuisine = cuisine).exists():
            return JsonResponse({"error": "Meal present on the menu already"}, status = status.HTTP_400_BAD_REQUEST, safe=False)
        serializer = MealPostSerializer(data = meal_data)
        if serializer.is_valid():
            meal =  MealModel.objects.create(cuisine = cuisine, meal_name = meal_name, price = price, category = category, meal_pic = meal_pic)
            serialized_response = MealGetSerializer(meal, many = False)
            return JsonResponse(serialized_response.data, status = status.HTTP_201_CREATED, safe=False)
        return JsonResponse({"error": serializer.errors }, status = status.HTTP_400_BAD_REQUEST, safe=False)
    
    def get(self, request):
        meals = MealModel.objects.annotate(average_rating = Avg('ratings__rating'))
        serialized_meals = MealAndRatingSerializer(meals, many=True)
        return JsonResponse(serialized_meals.data, status=status.HTTP_200_OK, safe=False)
    

#Location View Detail
class LocationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        location_detail = LocationDetail.objects.all()
        serialized_location_detail = LocationDetailGetSerializer(location_detail, many = True)
        return JsonResponse(serialized_location_detail.data, status = status.HTTP_200_OK, safe=False)
        
# Menus related to a specific Restaurants
class CuisineBasedMenuView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
            if not cuisine:
                return JsonResponse({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status = status.HTTP_404_NOT_FOUND)
        
        try:
            meals = MealModel.objects.filter(cuisine_id = cuisine).annotate(average_rating = Avg('ratings__rating'))
            serialized_meals = MealAndRatingSerializer(meals, many=True)
            return JsonResponse(serialized_meals.data, status=status.HTTP_200_OK, safe=False)
        except MealModel.DoesNotExist:
            return JsonResponse({"error" : "Meals specific for this restaurant not found"})
        
    def post(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
            if not cuisine:
                return JsonResponse({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status = status.HTTP_404_NOT_FOUND)
        data = request.data
        meal_serializer = CuisineBasedMenuPostSerializer(data = data, many = False)
        if meal_serializer.is_valid():
            try:
                meal_info = MealModel.objects.create(cuisine_id = cuisine, meal_name = data.get("meal_name"), price = data.get("price"), category = data.get("category"))
                serialized_data = MealGetSerializer(meal_info, many = False)
                return JsonResponse(serialized_data.data, status = status.HTTP_201_CREATED)
            except Exception as e:
                return JsonResponse({"error": "Integrity Error"}, status = status.HTTP_404_NOT_FOUND)
        return JsonResponse(meal_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    

class GetSpecificCuisineView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, cuisine_id):
        try:
            cuisine = Cuisine.objects.filter(cuisine_id=cuisine_id).first()
            if not cuisine:
                return JsonResponse({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Cuisine.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_data = CuisineGetSerializer(cuisine)
        return JsonResponse(serialized_data.data, status = status.HTTP_200_OK, safe = False)
        
class CuisineOwnerView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        cuisines = Cuisine.objects.filter(user = user)
        serialized_cuisines = CuisineGetSerializer(cuisines, many = True)
        return JsonResponse(data = serialized_cuisines.data, status = status.HTTP_200_OK, safe = False)


class SpecificMealView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, meal_id):
        data = request.data
        cuisine = Cuisine.objects.filter(cuisine_id = data.get('cuisine_id')).first()
        meal_name = data.get('meal_name')
        price = data.get('price')
        category = data.get('category')
        meal_pic = data.get('meal_pic')
        meal_data = {}
        meal_data['cuisine'] = cuisine.cuisine_id
        meal_data['meal_name'] = meal_name
        meal_data['price'] = price
        meal_data['category'] = category
        if meal_pic is not None:
            meal_data['meal_pic'] = meal_pic
        #print(meal_data)
        try:
            meal = MealModel.objects.get(meal_id = meal_id)
            serializer = MealPostSerializer(meal, data = meal_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status = status.HTTP_200_OK, safe=False)
            return JsonResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except MealModel.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status = status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, meal_id):
        try:
            meal = MealModel.objects.get(meal_id = meal_id)
            meal.delete()
            return JsonResponse({"message": "Meal deleted sucessfully"}, status = status.HTTP_200_OK, safe= False)
        except MealModel.DoesNotExist:
            return JsonResponse({"error": "Meal not found"}, status = status.HTTP_400_BAD_REQUEST, safe=False)

class CuisineAndLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        latitude = float(request.query_params.get('latitude'))
        longitude = float(request.query_params.get('longitude'))
        nearby_cuisines = get_nearby_cuisines(latitude, longitude)
        return JsonResponse(nearby_cuisines, status=status.HTTP_200_OK, safe=False)



class Distance(Func):
    function = 'ST_Distance_Sphere'
    template = '%(function)s(Point(%(longitude)s, %(latitude)s), Point(%(longitude2)s, %(latitude2)s))'
    output_field = FloatField()

def calculate_distance(latitude, longitude, latitude2, longitude2):
    radius = 6371  # Radius of the Earth in kilometers
    lat_diff = math.radians(latitude2 - latitude)
    lon_diff = math.radians(longitude2 - longitude)
    a = (math.sin(lat_diff / 2) ** 2 + math.cos(math.radians(latitude)) * 
         math.cos(math.radians(latitude2)) * math.sin(lon_diff / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance

def get_nearby_cuisines(latitude, longitude, radius_km=50):
    nearby_cuisines = []
    cuisines = Cuisine.objects.all()
    serialized_cuisines = CuisineAndLocationDetailSerializer(cuisines, many=True)
    for cuisine in serialized_cuisines.data:
        distance = calculate_distance(latitude, longitude, float(cuisine['location_detail']['latitude']), float(cuisine['location_detail']['longitude']))
        print(distance)
        if distance <= radius_km:
            nearby_cuisines.append(cuisine)
    return nearby_cuisines