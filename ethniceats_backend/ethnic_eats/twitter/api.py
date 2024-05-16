from requests_oauthlib import OAuth1
import requests
from collections import Counter
from dotenv import load_dotenv
import os
import tweepy

load_dotenv()

bearer_token = os.getenv('bearer_token')
access_token = os.getenv('access_token')
access_token_secret = os.getenv('access_token_secret')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
api_key = os.getenv('api_key')
api_secret = os.getenv('api_secret')

# Define Twitter API endpoint
twitter_api_url = 'https://api.twitter.com/1.1/search/tweets.json'

# List of ethnic cuisines to track
ethnic_cuisines = ['Chinese', 'Mexican', 'Indian', 'Italian', 'Japanese', 'Thai']

# Counter to store trending cuisines
trending_cuisines = Counter()

try:
    # Create OAuth1 session
    auth = OAuth1(client_id, client_secret, access_token, access_token_secret)

    # Fetch tweets mentioning ethnic cuisines
    for cuisine in ethnic_cuisines:
        # Make request to Twitter API
        response = requests.get(twitter_api_url, auth=auth, params={'q': cuisine, 'count': 100})

        # Check if request was successful
        if response.status_code == 200:
            # Extract tweets from response
            tweets = response.json().get('statuses', [])

            # Count mentions of cuisine
            trending_cuisines[cuisine] += len(tweets)
        else:
            print(f"Error fetching tweets for {cuisine}: {response.text}")

    # Identify trending cuisines
    trending_cuisines = trending_cuisines.most_common()
    
    # Print the results
    print("Trending Ethnic Cuisines:")
    for cuisine, count in trending_cuisines:
        print(f"{cuisine}: {count} mentions")

except Exception as e:
    print(f"An error occurred: {e}")