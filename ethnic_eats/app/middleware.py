import pandas as pd
import os

# Define a global variable to hold the DataFrame
df = None

def load_dataframe():
    global df
    df = pd.read_csv('app/food_dataset.csv', compression='gzip')
    print("DataFrame loaded successfully.")

class LoadDataFrameMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        load_dataframe()  # Load the DataFrame when the middleware is instantiated

    def __call__(self, request):
        response = self.get_response(request)
        return response