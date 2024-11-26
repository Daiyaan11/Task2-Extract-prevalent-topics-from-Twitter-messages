import tweepy
import csv
import json

def collect_tweets_by_topic(api, topic, filename, limit=20):
    tweets = tweepy.Cursor(api.search_tweets, q=topic, lang='en').items(limit)
    data = [[tweet.id_str, tweet.created_at, tweet.retweet_count, tweet.text] for tweet in tweets]

    with open(f'data/raw/{filename}.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Id", "Created_at", "Retweet_count", "Text"])
        writer.writerows(data)

def save_user_timeline(api, screen_name, filename, pages=2):
    with open(f'data/raw/{filename}.jsonl', 'w') as file:
        for page in tweepy.Cursor(api.user_timeline, screen_name=screen_name, count=200).pages(pages):
            for status in page:
                file.write(json.dumps(status._json) + '\n')
