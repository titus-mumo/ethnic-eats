from rest_framework import status, permissions
from rest_framework.views import APIView
from django.http import JsonResponse
import json
import re

import google.generativeai as genai
from pathlib import Path
import hashlib
from datetime import datetime

GEMINI_API_KEY = 'AIzaSyBswPaYh2wO7dQddLCuow6QWqee6cH2A_o'
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config=generation_config,)



# class TrendingRestaurants(APIView):
#     #permission_classes = [permissions.IsAuthenticated]

#     def get(self, request = {}):
#         response = model.generate_content("Examples of trending restaurants in the UK (output a list containing dicts of the restaurants and description ,like in programing). Note that i don't want the type, I want the specific restaurant name. Do not add any other content.")
#         # Define pattern to extract restaurant names and descriptions
#         pattern = re.compile(r'\{\s*"restaurant":\s*"([^"]+)",\s*"description":\s*"([^"]+)"\s*\}')

#         # Find all matches in the response text
#         matches = pattern.findall(response.text)

#         # Create a list of dictionaries with the extracted data
#         restaurants = [{'restaurant': match[0], 'description': match[1]} for match in matches]

#         # Convert the list to JSON format
#         json_response = json.dumps(restaurants, indent=2)

#         # Clean up JSON response by removing unnecessary characters
#         cleaned_response = json_response.replace("\\", "").replace("\n", "")

#         # Return the cleaned response
#         return JsonResponse(cleaned_response, status=status.HTTP_200_OK, safe=False)

def update_foods() -> None:
        response = model.generate_content("Give a list of trending foods in the UK. Don't explain. Don't add any other information, at all.")
        data = response.text.replace("-", "").replace("*", "")
        json_data = json.dumps(data)
        with open('foods.json', 'w') as f:
          json.dump(json_data, f, indent=2)

        print(f"JSON file updated at {datetime.now().isoformat()}")

class TrendingFoods(APIView):
    
    def get(self, request):
        with open('foods.json', 'r') as f:
          json_file = json.load(f)
          food_list = json_file.strip().strip('\"').split('\\n')
        return JsonResponse(food_list, status = status.HTTP_200_OK, safe=False)
