import os
import re
from utils.stopwords import STOPWORDS


def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text


def tokenize(text: str) -> list:
    return text.split()


def remove_stopwords(tokens: list) -> list:
    return [word for word in tokens if word not in STOPWORDS]


def parse_document(filepath: str) -> dict:
    """
    Returns:
    {
      "tokens": [...],
      "text": "original text"
    }
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()

    cleaned = clean_text(raw_text)
    tokens = tokenize(cleaned)
    tokens = remove_stopwords(tokens)

    return {
        "tokens": tokens,
        "text": raw_text
    }


def parse_all_documents(folder_path: str) -> dict:
    documents = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            documents[filename] = parse_document(filepath)

    return documents