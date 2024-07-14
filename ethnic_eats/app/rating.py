from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Ratings, MealModelIntense
import numpy as np
import pandas as pd
from django.db.models import Avg
from rest_framework.response import Response
from django.http import JsonResponse
from .meal_view import MealIntenseAndRatingSerializer

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
        meal = MealModelIntense.objects.get(meal_id=meal_id)
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
        diatery_preference = str(request.query_params.get('diateryPreference'))
        meals = MealModelIntense.objects.annotate(average_rating=Avg('ratings__rating'))

        if 'Vegetarian' in diatery_preference:
            vegetarian_ingredients = [
                "chicken", "turkey", "duck", "goose", "beef", "lamb", "veal", "pork", "bacon", "seafood", "hamburger",
                "rabbit", "venison", "offal", "sausage", "hot dog", "salami", "pepperoni",
                "gelatin", "rennet", "pepsin", "L-cysteine",
                "fish", "shrimp", "lobster", "crab", "mussels", "clams", "oysters", "scallops", "calamari", "sushi", 'tilapia'
            ]
            for ingredient in vegetarian_ingredients:
                meals = meals.exclude(meal_name__icontains=ingredient).exclude(ingredients__icontains=ingredient)

        if 'Vegan' in diatery_preference:
            vegan_avoid_foods = [
                'beef', 'hamburger', 'lamb', 'pork', 'veal', 'horse', 'organ meat', 'meat', 'chicken', 'turkey',
                'goose', 'duck', 'quail', 'fish', 'anchovies', 'shrimp', 'tilapia', 'sushi', 'squid',
                'scallops', 'calamari', 'mussels', 'crab', 'lobster', 'fish sauce', 
                'milk', 'yogurt', 'cheese', 'butter', 'cream', 'ice cream', 'eggs', 'egg', 'honey', 'bee pollen',
                'royal jolley', 'carmine', 'cochineal', 'gelatin', 'isinglass', 'castoreum', 'omega-3', 'shellac',
                'whey', 'casein', 'lactose', 'l-cystein', 'chips', 'cookies', 'candy'
            ]
            for ingredient in vegan_avoid_foods:
                meals = meals.exclude(meal_name__icontains=ingredient).exclude(ingredients__icontains=ingredient)

        if 'Gluten-Free' in diatery_preference:
            gluten_ingredients = [
                "wheat bran", "wheat flour", "spelt", "durum", "kamut", "semolina",
                "barley", "rye", "tricale", "malt", "brewer's yeast", "bread", "pasta",
                "cereals", "rice","maize", "quinoa", "cake", "muffin", "bread crumbs", "pasteries", "candy", "cracker",
                "flavoured chips", "pretzels", "soy sauce", "teriyaki sauce", "hoisin sauce", 
                "marinades", "salad dressings", "beer", "pizza", "couscous", "broth"
            ]
            for ingredient in gluten_ingredients:
                meals = meals.exclude(meal_name__icontains=ingredient).exclude(ingredients__icontains=ingredient)

        if 'Nut-Free' in diatery_preference:
            nuts = [
                'nut', 'nuts', "acorns", "almonds", "andean walnuts", "argan nuts", "baru nuts", "beech nuts",
                "betel nuts", "bitter almond", "black walnuts", "brazil nuts", "breadnut", "bunya nut", "butternuts",
                "canarium nut", "candle nuts", "cashews", "chestnuts", "chilean hazelnut", "chinese chestnut", 
                "coconuts", "dika nuts", "english walnuts", "filberts (hazelnuts)", "ginkgo nuts", "hickory nuts", 
                "jackfruit seeds", "kola nuts", "kurrajong nuts", "lotus nuts", "macadamia nuts", "malabar chestnut", 
                "mongongo nuts", "monkey puzzle nut", "oysternut", "peanuts", "pecans", "pine nuts", "pistachios", 
                "canistel nut", "cupuacu nut", "pekan nut", "sheanut", "ugli fruit seeds", "walnuts"
            ]
            for nut in nuts:
                meals = meals.exclude(meal_name__icontains=nut).exclude(ingredients__icontains=nut)

        # Filter meals with mean rating >= 3.5
        meals = meals.filter(average_rating__gte=3.5)
        serialized_meals = MealIntenseAndRatingSerializer(meals, many=True)
        return JsonResponse(serialized_meals.data, status=status.HTTP_200_OK, safe=False)
    
    


