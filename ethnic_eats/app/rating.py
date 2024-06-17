from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Ratings, MealModel
import numpy as np
import pandas as pd
from django.db.models import Avg
from rest_framework.response import Response
from django.http import JsonResponse

from rest_framework.serializers import ModelSerializer

class RatingSerializer(ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['user_id', 'meal_id', 'rating']


class RatingView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        print(request.data)
        rating = request.data.get('rating')
        print(rating)
        meal_id = request.data.get('meal_id')
        print(meal_id)
        meal = MealModel.objects.get(meal_id=meal_id)
        print(meal)
        if not meal:
            return JsonResponse({"error": "Meal not found"}, status=status.HTTP_404_NOT_FOUND)
        
        Rating = {
            'user_id': user.id,
            'meal_id': meal.meal_id,
            'rating': rating
        }

        rating_serializer = RatingSerializer(data=Rating)

        if rating_serializer.is_valid():
            new_rating = Ratings.objects.create(user_id=user, meal_id=meal, rating=rating)
            return JsonResponse(rating_serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HighlyRatedFoods(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        meals_with_avg_rating = Ratings.objects.values('meal_id').annotate(avg_rating=Avg('rating'))

        # Filter meals with mean rating >= 3.5
        recommended_meals = meals_with_avg_rating.filter(avg_rating__gte=3.5)

        # Prepare a response dictionary
        recommended_meals_list = []
        for meal_data in recommended_meals:
            meal_id = meal_data['meal_id']
            avg_rating = meal_data['avg_rating']
            try:
                meal = MealModel.objects.get(meal_id=meal_id)
                recommended_meals_list.append({
                    'meal_id': meal_id,
                    'cuisine_id': meal.cuisine.cuisine_id,
                    'meal_name': meal.meal_name,
                    'avg_rating': avg_rating,
                    'price': meal.price,
                    'category':meal.category,
                    'meal_pic': str(meal.meal_pic),

                })
            except MealModel.DoesNotExist:
                continue

        return Response(recommended_meals_list, status=status.HTTP_200_OK)
    
    


