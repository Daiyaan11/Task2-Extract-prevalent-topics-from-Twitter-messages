import re
import json
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import string

# Pre-initialize for performance
TOKENIZER = TweetTokenizer()
STOPWORDS = set(stopwords.words('english') + list(string.punctuation) + ['rt', 'via', '...'])
URL_PATTERN = re.compile(r"http\S+|@\w+")

def clean_text(text):
    """Remove URLs, mentions, and non-ASCII chars."""
    text = URL_PATTERN.sub("", text)
    return text.encode('ascii', 'ignore').decode('ascii').strip()

def preprocess(text, tokenizer=TOKENIZER, stopwords=STOPWORDS):
    """Normalize and tokenize text."""
    text = clean_text(text.lower())
    return [t for t in tokenizer.tokenize(text) if t not in stopwords and t.isalpha()]

def analyze_tokens(filepath):
    """Count tokens with robust error handling."""
    token_counts = Counter()
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                try:
                    tweet = json.loads(line)
                    tokens = preprocess(tweet.get('text', ''))
                    token_counts.update(tokens)
                except (json.JSONDecodeError, KeyError):
                    continue
    except IOError as e:
        raise SystemExit(f"Error reading {filepath}: {e}")
    return token_counts.most_common(10)