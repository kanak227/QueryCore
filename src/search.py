from src.parser import clean_text, tokenize, remove_stopwords


def process_query(query: str) -> list:
    query = clean_text(query)
    tokens = tokenize(query)
    tokens = remove_stopwords(tokens)
    return tokens


def search(index: dict, doc_lengths: dict, idf: dict, query: str) -> dict:
    """
    TF-IDF based search
    Returns: doc → score
    """
    query_tokens = process_query(query)
    results = {}

    for word in query_tokens:
        if word not in index:
            continue

        for doc, freq in index[word].items():
            # TF = freq / doc_length
            tf = freq / doc_lengths[doc]

            # IDF
            idf_score = idf.get(word, 0)

            # TF-IDF
            score = tf * idf_score

            if doc not in results:
                results[doc] = 0

            results[doc] += score

    return results