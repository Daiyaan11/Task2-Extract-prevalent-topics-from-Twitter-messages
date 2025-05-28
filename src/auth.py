import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

def authenticate_v2():
    """Authenticate with Twitter API v2"""
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")
    if not BEARER_TOKEN:
        raise ValueError("Missing BEARER_TOKEN in .env")
    
    return tweepy.Client(bearer_token=BEARER_TOKEN)

def authenticate_v1():
    """Authenticate with Twitter API v1.1 (if needed)"""
    return tweepy.OAuth1UserHandler(
        consumer_key=os.getenv("API_KEY"),
        consumer_secret=os.getenv("API_SECRET"),
        access_token=os.getenv("ACCESS_TOKEN"),
        access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
    )