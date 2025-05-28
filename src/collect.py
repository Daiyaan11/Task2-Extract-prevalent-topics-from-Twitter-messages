import tweepy
import json
import csv
import os
from pathlib import Path
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=retry_if_exception_type(tweepy.errors.TooManyRequests),
)
def safe_tweet_search(client, query_params):
    """Wrapper with automatic retry for rate limits"""
    try:
        response = client.search_recent_tweets(**query_params)
        if response.data:
            logger.info(f"Fetched {len(response.data)} tweets")
        return response
    except tweepy.errors.TweepyException as e:
        logger.warning(f"Twitter API error: {e}")
        raise

def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    return output_dir

def save_tweets_to_file(tweets, filename_prefix):
    """Save tweets to both JSON and CSV with timestamp"""
    output_dir = ensure_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Define file paths
    json_path = output_dir / f"{filename_prefix}_{timestamp}.json"
    csv_path = output_dir / f"{filename_prefix}_{timestamp}.csv"
    
    try:
        # Save as JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump([tweet.data for tweet in tweets], f, indent=4)
        
        # Save as CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "id", "author_id", "created_at", "text", 
                "retweets", "likes", "replies", "quotes"
            ])
            for tweet in tweets:
                metrics = tweet.data.get('public_metrics', {})
                writer.writerow([
                    tweet.data['id'],
                    tweet.data['author_id'],
                    tweet.data['created_at'],
                    tweet.data['text'],
                    metrics.get('retweet_count', 0),
                    metrics.get('like_count', 0),
                    metrics.get('reply_count', 0),
                    metrics.get('quote_count', 0)
                ])
        
        logger.info(f"Successfully saved:\n- {json_path}\n- {csv_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to save files: {e}")
        return False

def collect_tweets_by_topic(client, topic, filename_prefix, limit=100):
    """
    Collect tweets by topic with enhanced error handling
    Args:
        client: Authenticated Twitter client
        topic: Search query (e.g., "#eskom OR #loadshedding")
        filename_prefix: Base name for output files
        limit: Max tweets to collect (default: 100)
    """
    query_params = {
        "query": topic,
        "tweet_fields": "id,text,author_id,created_at,public_metrics",
        "max_results": min(100, limit)  # Twitter's max per request
    }

    try:
        tweets = []
        for tweet in tweepy.Paginator(
            safe_tweet_search,
            client,
            query_params
        ).flatten(limit=limit):
            tweets.append(tweet)
            if len(tweets) >= limit:
                break
        
        if tweets:
            save_tweets_to_file(tweets, filename_prefix)
            return True
        else:
            logger.warning("No tweets found matching your criteria")
            return False
            
    except tweepy.errors.TweepyException as e:
        logger.error(f"Twitter API failure: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return False