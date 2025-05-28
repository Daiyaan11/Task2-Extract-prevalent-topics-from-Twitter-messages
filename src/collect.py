import tweepy
import csv
import os
from tenacity import retry, stop_after_attempt, wait_exponential
from tweepy.errors import TweepyException

def collect_tweets_by_topic(client, topic, filename, limit=100):
    # Configure query
    query_params = {
        "query": topic,
        "tweet_fields": "id,text,author_id,created_at,public_metrics",
        "max_results": min(100, limit)  # Twitter's max per request
    }

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    csv_path = os.path.join("output", filename)
    json_path = os.path.join("output", filename.replace(".csv", ".json"))

    # Fetch tweets with retries
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_tweets():
        tweets = []
        for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            **query_params
        ).flatten(limit=limit):
            tweets.append(tweet)
        return tweets

    try:
        tweets_data = fetch_tweets()
        
        # Save to JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([tweet.data for tweet in tweets_data], f, indent=4)

        # Save to CSV
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Author", "Created At", "Text", "Retweets", "Likes"])
            for tweet in tweets_data:
                metrics = tweet.data.get("public_metrics", {})
                writer.writerow([
                    tweet.data["id"],
                    tweet.data["author_id"],
                    tweet.data["created_at"],
                    tweet.data["text"],
                    metrics.get("retweet_count", 0),
                    metrics.get("like_count", 0)
                ])

        print(f"Saved {len(tweets_data)} tweets to {csv_path}")

    except TweepyException as e:
        print(f"Twitter API failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")