from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import Ratings
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from rest_framework.response import Response

class HighlyRatedFoods(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        user = request.user
        user_id = user.id
        ratings_data = Ratings.objects.all()

        ratings_list = list(ratings_data.values('user_id', 'meal_id', 'rating'))

        ratings_df = pd.DataFrame(ratings_list)
        user_item_matrix = ratings_df.pivot(index='user_id', columns='meal_id', values='rating')

        user_item_matrix.fillna(0, inplace=True)
        user_similarity = cosine_similarity(user_item_matrix)
        user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)
        sim_scores = user_similarity_df[user_id]
        # Get similarity scores for the user
        sim_scores = sim_scores.values.reshape(-1, 1)
        # Multiply similarity scores by the user's ratings
        
        user_ratings = user_item_matrix.values
        weighted_ratings = user_ratings.T.dot(sim_scores).flatten()
        # Normalize the weighted ratings
        normalized_ratings = weighted_ratings / sim_scores.sum(axis=0)

        # Create a Series with the scores and sort by descending order
        recommendations = pd.Series(normalized_ratings, index=user_item_matrix.columns).sort_values(ascending=False)

        # Remove items the user has already rated
        rated_items = user_item_matrix.loc[user_id][user_item_matrix.loc[user_id] > 0].index
        recommendations = recommendations.drop(rated_items)
        return Response(recommendations,status = status.HTTP_200_OK)

    
    


