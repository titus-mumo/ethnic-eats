from rest_framework import status, permissions
from rest_framework.views import APIView
from django.http import JsonResponse
import json
import re

from dotenv import load_dotenv

import google.generativeai as genai
from pathlib import Path
import hashlib
from datetime import datetime

import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(model_name="gemini-1.5-flash-latest", generation_config=generation_config,)

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
