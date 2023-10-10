#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests

def count_words(subreddit, word_list, after=None, counts={}):
    if not word_list:
        return

    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)

        if response.status_code != 200:
            return

        data = response.json()
        children = data.get('data', {}).get('children', [])
        after = data.get('data', {}).get('after', None)

        for child in children:
            title = child.get('data', {}).get('title', "").lower()
            for word in word_list:
                word_lower = word.lower()
                if word_lower not in counts:
                    counts[word_lower] = title.count(f" {word_lower} ")

        count_words(subreddit, word_list, after, counts)

    except Exception:
        return

    if after is None:
        sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Example: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        keywords = sys.argv[2].split()
        count_words(subreddit, keywords)

