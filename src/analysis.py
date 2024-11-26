import json
from collections import Counter

def analyze_hashtags(filepath):
    with open(filepath, 'r') as file:
        hashtags = Counter()
        for line in file:
            tweet = json.loads(line)
            entities = tweet.get('entities', {})
            h = entities.get('hashtags', [])
            hashtags_tweet = [tag['text'].lower() for tag in h]
            hashtags.update(hashtags_tweet)
    return hashtags.most_common(10)

def analyze_mentions(filepath):
    with open(filepath, 'r') as file:
        mentions = Counter()
        for line in file:
            tweet = json.loads(line)
            entities = tweet.get('entities', {})
            m = entities.get('user_mentions', [])
            mentions_in_tweet = [mention['screen_name'].lower() for mention in m]
            mentions.update(mentions_in_tweet)
    return mentions.most_common(5)
