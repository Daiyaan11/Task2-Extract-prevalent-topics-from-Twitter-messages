from src.auth import authenticate_v2
from src.collect import collect_tweets_by_topic

def main():
    client = authenticate_v2()
    topic = "#eskom OR #citypower OR #joburgwater OR #servicedelivery OR #waterupdates OR #loadshedding OR #roadmaintenance OR #joburgissues"
    collect_tweets_by_topic(client, topic, filename="output/johannesburg_tweets.csv", limit=100)

if __name__ == "__main__":
    main()
