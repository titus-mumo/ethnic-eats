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

import requests

# Your bearer token
BEARER_TOKEN = bearer_token

# The search query
query = 'justTitusk'

# The Twitter API v2 endpoint for recent search
      
url = f'https://api.twitter.com/2/users/me'

    

# The headers for the request
headers = {
    'Authorization': f'Bearer {BEARER_TOKEN}'
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check for errors
if response.status_code != 200:
    raise Exception(f"Request returned an error: {response.status_code} {response.text}")

# Print the response
tweets = response.json()
for tweet in tweets['data']:
    print(tweet['text'])




      
# import requests
# from requests_oauthlib import OAuth1
# import time
# import random
# import hashlib
# import hmac
# import base64

# # Your credentials
# CONSUMER_API_KEY = api_key
# CONSUMER_API_SECRET_KEY = api_secret
# ACCESS_TOKEN = access_token
# ACCESS_TOKEN_SECRET = access_token_secret

# # Generate OAuth nonce
# def generate_nonce(length=8):
#     return ''.join([str(random.randint(0, 9)) for i in range(length)])

# # Generate OAuth timestamp
# def generate_timestamp():
#     return str(int(time.time()))

# # Generate OAuth signature
# def generate_signature(method, url, params, consumer_secret, token_secret):
#     sorted_params = '&'.join(['{}={}'.format(k, v) for k, v in sorted(params.items())])
#     base_string = '&'.join([method.upper(), requests.utils.quote(url, safe=''), requests.utils.quote(sorted_params, safe='')])
    
#     signing_key = '&'.join([consumer_secret, token_secret])
    
#     hashed = hmac.new(signing_key.encode('utf-8'), base_string.encode('utf-8'), hashlib.sha1)
#     signature = base64.b64encode(hashed.digest()).decode('utf-8')
#     return signature

# # Prepare the parameters
# url = 'https://api.twitter.com/1.1/statuses/update.json'
# status = 'Hello world'
# method = 'POST'

# oauth_params = {
#     'oauth_consumer_key': CONSUMER_API_KEY,
#     'oauth_nonce': generate_nonce(),
#     'oauth_signature_method': 'HMAC-SHA1',
#     'oauth_timestamp': generate_timestamp(),
#     'oauth_token': ACCESS_TOKEN,
#     'oauth_version': '1.0',
#     'status': status,
# }

# # Generate OAuth signature
# oauth_params['oauth_signature'] = generate_signature(method, url, oauth_params, CONSUMER_API_SECRET_KEY, ACCESS_TOKEN_SECRET)

# # Create OAuth1 object
# auth = OAuth1(
#     CONSUMER_API_KEY,
#     client_secret=CONSUMER_API_SECRET_KEY,
#     resource_owner_key=ACCESS_TOKEN,
#     resource_owner_secret=ACCESS_TOKEN_SECRET,
#     signature_type='query'
# )

# # Make the POST request
# response = requests.post(url, params={'status': status}, auth=auth)

# # Print the response
# print(response.status_code)
# print(response.json())
 