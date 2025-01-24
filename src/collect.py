import tweepy
import json
import csv
import os
import time

def collect_tweets_by_topic(client, topic, filename, limit=100):
    query_params = {
        "query": topic,
        "tweet_fields": "id,text,author_id,created_at,public_metrics",
        "max_results": 10
    }

    output_folder = "output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    json_path = os.path.join(output_folder, f"{filename}.json")
    csv_path = os.path.join(output_folder, f"{filename}.csv")

    tweets_data = []

    try:
        for _ in range(limit // query_params["max_results"]):  
            response = client.search_recent_tweets(**query_params)
            if "data" not in response:
                print("No more tweets found.")
                break

            tweets_data.extend(response["data"])
            print("Pausing for rate limit...")
            time.sleep(20)
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump(tweets_data, json_file, indent=4, ensure_ascii=False)
        with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Tweet ID", "Author ID", "Created At", "Text", "Retweets", "Likes", "Replies", "Quotes"])
            for tweet in tweets_data:
                metrics = tweet["public_metrics"]
                writer.writerow([
                    tweet["id"],
                    tweet["author_id"],
                    tweet["created_at"],
                    tweet["text"],
                    metrics["retweet_count"],
                    metrics["like_count"],
                    metrics["reply_count"],
                    metrics["quote_count"],
                ])

        print(f"Tweets saved to {json_path} and {csv_path}.")

    except tweepy.errors.TooManyRequests:
        print("Rate limit exceeded. Please try again later.")
    except Exception as e:
        print(f"An error occurred: {e}")

