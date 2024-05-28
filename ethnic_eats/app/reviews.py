from .models import Cuisine, Reviews
from rest_framework.views import APIView
from .serializers import UserReviewPostSerielizer,UserReviewSerielizer
from django.http import JsonResponse
from rest_framework import status, permissions
from rest_framework.response import Response
from nltk.sentiment import SentimentIntensityAnalyzer


#Reviews View
class UserReviewClass(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, cuisine_id):
        cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
        review_data = {
            'cuisine': cuisine.cuisine_id,
            'review': request.data.get('review'),
            'score' : classify_review(str(request.data.get('review')))
        }

        serializer = UserReviewPostSerielizer(data=review_data)
        
        if serializer.is_valid():
            saved_data = Reviews.objects.create(
                review=review_data['review'], cuisine = cuisine, score = review_data['score'])
            serializer = UserReviewSerielizer(saved_data, many=False)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED, safe = False)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, safe=False)

    def get(self, request, cuisine_id):
        cuisine = Cuisine.objects.filter(cuisine_id = cuisine_id).first()
        reviews = Reviews.objects.filter(cuisine = cuisine)
        serializer = UserReviewSerielizer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
review_model = SentimentIntensityAnalyzer()

def classify_review(review):
    print(review)
    sentiment_scores = review_model.polarity_scores(review)
    compound_score = sentiment_scores['compound']
    return compound_score
    
