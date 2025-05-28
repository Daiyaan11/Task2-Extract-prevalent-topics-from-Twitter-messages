import json
import logging
from collections import Counter

logging.basicConfig(level=logging.INFO)

def analyze_entities(filepath):
    """Extract hashtags and mentions in a single file pass."""
    hashtags = Counter()
    mentions = Counter()
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                try:
                    tweet = json.loads(line)
                    entities = tweet.get('entities', {})
                    
                    # Process hashtags
                    for tag in entities.get('hashtags', []):
                        if isinstance(tag, dict) and 'text' in tag:
                            hashtags[tag['text'].lower()] += 1
                    
                    # Process mentions
                    for mention in entities.get('user_mentions', []):
                        if isinstance(mention, dict) and 'screen_name' in mention:
                            mentions[mention['screen_name'].lower()] += 1
                
                except json.JSONDecodeError:
                    logging.warning(f"Skipping malformed line #{line_num}")
    
    except FileNotFoundError:
        raise SystemExit(f"Error: File {filepath} not found")
    
    return {
        'hashtags': hashtags.most_common(10),
        'mentions': mentions.most_common(5)
    }
def save_results(results, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    with open(f"{output_dir}/analysis.json", 'w') as f:
        json.dump(results, f)

def full_analysis(filepath):
    tokens = analyze_tokens(filepath)  # From preprocess.py
    entities = analyze_entities(filepath)
    return {**entities, 'top_tokens': tokens}
    
# Example usage:
# results = analyze_entities('output/tweets.json')
# print("Top hashtags:", results['hashtags'])
# print("Top mentions:", results['mentions'])