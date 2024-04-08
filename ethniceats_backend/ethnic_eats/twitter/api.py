from requests_oauthlib import OAuth1
import tweepy
from collections import Counter
import requests

consumer_key = ''
bearer_token = 'AAAAAAAAAAAAAAAAAAAAANaHtAEAAAAAR4aphPf0I5R1%2BNCC2iwkeEfxZHs%3DYq7qxn9ozngo37NMO2zFsRs8DxO2ADQbWKXWdX9W1fBRHuB7Dt'
access_token = '1746594715451961344-mrxxsknmZicFAWWgMkmG4RzlNebdpF'
access_token_secret = 'MSWTVMy59Jz2W70YtmHSqfgBYtj2ajYAydgDYLzA41r5P'
client_id = 'UEQ1LUtKYlptLUlWd2FTdTVubjA6MTpjaQ'
client_secret = 'aFydSzhI64llpKa4Olacai5ZxwY0G5d8qL79gvc6Uc3ESzPTHB'
api_key = 'hALGDFf3fTvZbCquI7toqmULz'
api_secret = 'svTO0edrgEJkNTypf5VvXuN4WB8wwMl9kEb3cFZYoMdLxjGoZJ'
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
