from src.parser import clean_text, tokenize, remove_stopwords


def process_query(query: str) -> list:
    """
    Parse user query using same pipeline as documents
    """
    query = clean_text(query)
    tokens = tokenize(query)
    tokens = remove_stopwords(tokens)
    return tokens


def search(index: dict, query: str) -> dict:
    """
    Basic OR search
    Returns: doc → score (simple count)
    """
    query_tokens = process_query(query)
    results = {}

    for word in query_tokens:
        if word in index:
            for doc, freq in index[word].items():
                if doc not in results:
                    results[doc] = 0
                results[doc] += freq  # simple scoring

    return results