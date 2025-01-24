import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

def authenticate_v2():
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    if not BEARER_TOKEN:
        raise ValueError("BEARER_TOKEN is missing. Please check your .env file.")
    return tweepy.Client(bearer_token=BEARER_TOKEN)
