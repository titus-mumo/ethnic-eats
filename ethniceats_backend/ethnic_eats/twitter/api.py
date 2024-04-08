from requests_oauthlib import OAuth1
import tweepy
from collections import Counter
import requests
from dotenv import load_dotenv
import os

load_dotenv()

bearer_token = os.getenv('bearer_token')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')
# Define Twitter API endpoints
twitter_api_url = 'https://api.twitter.com/1.1/search/tweets.json'

# List of ethnic cuisines to track
ethnic_cuisines = ['Chinese', 'Mexican',
                   'Indian', 'Italian', 'Japanese', 'Thai']

# Fetch tweets mentioning ethnic cuisines
trending_cuisines = Counter()
try:
    for cuisine in ethnic_cuisines:
        # Define OAuth1 session
        auth = OAuth1(api_key, api_secret, access_token, access_token_secret)

        # Make request to Twitter API
        response = requests.get(twitter_api_url, auth=auth, params={
                                'q': cuisine, 'count': 100})

        # Extract tweets from response
        tweets = response.json().get('statuses', [])

        # Count mentions of cuisine
        for tweet in tweets:
            trending_cuisines[cuisine] += 1

    # Identify trending cuisines
    trending_cuisines = trending_cuisines.most_common()
except Exception as e:
    print(e)

# Print the results
print("Trending Ethnic Cuisines:")

print(trending_cuisines)
# for cuisine, count in trending_cuisines:
#     print(f"{cuisine}: {count} mentions")
