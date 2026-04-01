import os
import re
from utils.stopwords import STOPWORDS


def clean_text(text: str) -> str:
    """
    Lowercase and remove punctuation
    """
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text


def tokenize(text: str) -> list:
    """
    Split text into words
    """
    tokens = text.split()
    return tokens


def remove_stopwords(tokens: list) -> list:
    """
    Remove common stopwords
    """
    filtered = [word for word in tokens if word not in STOPWORDS]
    return filtered


def parse_document(filepath: str) -> list:
    """
    Full pipeline for a single file
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    text = clean_text(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)

    return tokens


def parse_all_documents(folder_path: str) -> dict:
    """
    Parse all .txt files in a folder
    """
    documents = {}

    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder_path, filename)
            tokens = parse_document(filepath)
            documents[filename] = tokens

    return documents