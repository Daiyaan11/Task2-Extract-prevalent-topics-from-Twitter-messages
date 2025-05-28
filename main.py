# src/main.py
import os
import argparse
from datetime import datetime
from src.auth import authenticate_v2
from src.collect import collect_tweets_by_topic

limit = int(os.getenv("TWEET_LIMIT", 100)) 
def main():
    parser = argparse.ArgumentParser(description="Fetch tweets by topic.")
    parser.add_argument("--limit", type=int, default=100, help="Max tweets to collect (default: 100)")
    args = parser.parse_args()

    client = authenticate_v2()
    topic = "#eskom OR #citypower OR #joburgwater"
    filename = f"output/johannesburg_tweets_{datetime.now().strftime('%Y%m%d')}.csv"
    collect_tweets_by_topic(client, topic, filename=filename, limit=args.limit)

if __name__ == "__main__":
    main()