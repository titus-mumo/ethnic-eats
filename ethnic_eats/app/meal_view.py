from rest_framework import status, permissions, serializers
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import MealModelIntense, Cuisine, Ratings
from django.db.models import Avg

class MealIntenseAndRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()
    class Meta:
        model = MealModelIntense
        fields = ['meal_id', 'cuisine', 'meal_name', 'price', 'category', 'meal_pic', 'ingredients', 'average_rating']

class MealModelIntenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealModelIntense
        fields = '__all__'

import os
import pandas as pd
from rapidfuzz import process
from concurrent.futures import ThreadPoolExecutor

# Absolute path to the CSV file
file_path = os.path.join(os.getcwd(), 'ethnic_eats', 'app', 'ingredients_dataset.csv')

if not os.path.isfile(file_path):
    print(f"File not found: {file_path}")
else:
    df = pd.read_csv(file_path)
    meal_names = df['Name'].tolist()
    print(f"Successfully loaded {len(meal_names)} meal names.")

def find_best_match(meal_name, meal_names):
    return process.extractOne(meal_name, meal_names)


def get_meal_ingredients(meal_name):
    with ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(find_best_match, meal_name, meal_names)
        best_match = future.result()

    if best_match and best_match[1] > 80:
        meal = df.loc[df['Name'] == best_match[0]].iloc[0]
        ingredients = meal['RecipeIngredientParts']
        print(meal['Name'])
        return ingredients
    else:
        return None
# print(get_meal_ingredients('Ground nuts'))
class MealIntenseView(APIView):
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
        meal_data['ingredients'] = str(get_meal_ingredients(meal_name))
        print(meal_data['ingredients'])
        if MealModelIntense.objects.filter(meal_name = meal_name, cuisine = cuisine).exists():
            return JsonResponse({"error": "Meal present on the menu already"}, status = status.HTTP_400_BAD_REQUEST, safe=False)
        serializer = MealModelIntenseSerializer(data = meal_data)
        if serializer.is_valid():
            meal =  MealModelIntense.objects.create(cuisine = cuisine, meal_name = meal_name, price = price, category = category, meal_pic = meal_pic, ingredients = meal_data['ingredients'])
            serialized_response = MealModelIntenseSerializer(meal, many = False)
            return JsonResponse(serialized_response.data, status = status.HTTP_201_CREATED, safe=False)
        return JsonResponse({"error": serializer.errors }, status = status.HTTP_400_BAD_REQUEST, safe=False)
    
    def get(self, request):
        diatery_preference = str(request.query_params.get('diateryPreference'))
        meals = MealModelIntense.objects.annotate(average_rating = Avg('ratings__rating'))
        if 'Vegetarian' in diatery_preference:
            print('vegetarian')
            vegetarian_ingredients = [
                "chicken", "turkey", "duck", "goose", "beef", "lamb", "veal", "pork", "bacon", "seafood", "hamburger",
                "rabbit", "venison", "offal", "sausage", "hot dog", "salami", "pepperoni",
                "gelatin", "rennet", "pepsin", "L-cysteine",
                "fish", "shrimp", "lobster", "crab", "mussels", "clams", "oysters", "scallops", "calamari", "sushi", 'tilapia'
            ]
            for ingredient in vegetarian_ingredients:
                meals = meals.exclude(meal_name__icontains=ingredient).exclude(ingredients__icontains=ingredient)
        if 'Vegan' in diatery_preference:
            print('vegan')
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
            print("Gluten-Free")
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
                'nut',
                "nuts",
                "acorns",
                "almonds",
                "andean walnuts",
                "argan nuts",
                "baru nuts",
                "beech nuts",
                "betel nuts",
                "bitter almond",
                "black walnuts",
                "brazil nuts",
                "breadnut",
                "bunya nut",
                "butternuts",
                "canarium nut",
                "candle nuts",
                "cashews",
                "chestnuts",
                "chilean hazelnut",
                "chinese chestnut",
                "coconuts",
                "dika nuts",
                "english walnuts",
                "filberts (hazelnuts)",
                "ginkgo nuts",
                "hickory nuts",
                "jackfruit seeds",
                "kola nuts",
                "kurrajong nuts",
                "lotus nuts",
                "macadamia nuts",
                "malabar chestnut",
                "mongongo nuts",
                "monkey puzzle nut",
                "oysternut",
                "peanuts",
                "pecans",
                "pine nuts",
                "pistachios",
                "canistel nut", 
                "cupuacu nut", 
                "pekan nut",
                "sheanut",
                "ugli fruit seeds",
                "walnuts"
                ]
            print('Nut-Free')
            for nut in nuts:
                meals = meals.exclude(meal_name__icontains=nut).exclude(ingredients__icontains=nut)
        serialized_meals = MealIntenseAndRatingSerializer(meals, many=True)
        return JsonResponse(serialized_meals.data, status=status.HTTP_200_OK, safe=False)


