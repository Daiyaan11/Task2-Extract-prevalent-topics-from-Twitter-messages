from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from collections import Counter
import string
import json

def preprocess(text, tokenizer, stopwords):
    text = text.lower()
    tokens = tokenizer.tokenize(text)
    return [t for t in tokens if t not in stopwords and not t.isdigit()]

def analyze_tokens(filepath):
    tokenizer = TweetTokenizer()
    punctuation = list(string.punctuation)
    stop_words = stopwords.words('english') + punctuation + ['rt', 'via', '...']

    token_counts = Counter()
    with open(filepath, 'r') as file:
        for line in file:
            tweet = json.loads(line)
            tokens = preprocess(tweet['text'], tokenizer, stop_words)
            token_counts.update(tokens)
    return token_counts.most_common(10)
