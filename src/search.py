from src.parser import clean_text, tokenize, remove_stopwords


def process_query(query: str) -> list:
    query = clean_text(query)
    tokens = tokenize(query)
    tokens = remove_stopwords(tokens)
    return tokens


def search(index: dict, doc_lengths: dict, idf: dict, query: str, mode="OR") -> dict:
    """
    mode = "OR" or "AND"
    """
    query_tokens = process_query(query)

    if not query_tokens:
        return {}

    # Step 1: collect doc sets
    doc_sets = []

    for word in query_tokens:
        if word in index:
            doc_sets.append(set(index[word].keys()))
        else:
            doc_sets.append(set())

    # Step 2: combine sets
    if mode == "AND":
        common_docs = set.intersection(*doc_sets) if doc_sets else set()
    else:  # OR
        common_docs = set.union(*doc_sets) if doc_sets else set()

    # Step 3: scoring (TF-IDF)
    results = {}

    for doc in common_docs:
        score = 0

        for word in query_tokens:
            if word in index and doc in index[word]:
                freq = index[word][doc]
                tf = freq / doc_lengths[doc]
                idf_score = idf.get(word, 0)
                score += tf * idf_score

        results[doc] = score

    return results