from src.auth import authenticate
from src.collect import collect_tweets_by_topic, save_user_timeline
from src.analysis import analyze_hashtags, analyze_mentions
from src.preprocess import analyze_tokens

def main():
    api = authenticate()

    # Collect tweets
    collect_tweets_by_topic(api, "#eskom OR #citypower", "eskom_tweets", limit=100)
    save_user_timeline(api, "CityofJoburg", "city_joburg_timeline")

    # Analyze hashtags
    hashtags = analyze_hashtags("data/raw/city_joburg_timeline.jsonl")
    print("Top 10 Hashtags:", hashtags)

    # Analyze mentions
    mentions = analyze_mentions("data/raw/city_joburg_timeline.jsonl")
    print("Top 5 Mentions:", mentions)

    # Token analysis
    tokens = analyze_tokens("data/raw/city_joburg_timeline.jsonl")
    print("Top 10 Tokens:", tokens)

if __name__ == "__main__":
    main()
