
import argparse
import sys
from collections import Counter
import string


def clean_words(text):
    """Convert text into lowercase words and remove punctuation."""
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    words = text.split()
    return words


def read_file(filename):
    """Read the contents of a text file."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    return text


def main(argv=None):
    """Read command-line arguments and count the most common words."""
    parser = argparse.ArgumentParser(
        description="Count words in a text file"
    )

    parser.add_argument("filename")
    parser.add_argument("--top", type=int, default=5)

    args = parser.parse_args(argv)

    text = read_file(args.filename)

    if not text.strip():
        print("Error: The file is empty.")
        sys.exit(1)

    words = clean_words(text)
    word_counts = Counter(words)
    top_words = word_counts.most_common(args.top)

    if not top_words:
        print("No words found.")
    else:
        for word, count in top_words:
            print(f"{word}: {count}")


if __name__ == "__main__":
    main()
