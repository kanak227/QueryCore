from src.parser import clean_text, tokenize, remove_stopwords


def process_query(query: str) -> list:
    query = clean_text(query)
    tokens = tokenize(query)
    tokens = remove_stopwords(tokens)
    return tokens


def is_phrase_query(query: str) -> bool:
    """Detect if query is wrapped in quotes e.g. "machine learning" """
    query = query.strip()
    return query.startswith('"') and query.endswith('"')


def extract_phrase_tokens(query: str) -> list:
    """Extract raw tokens from a phrase query (preserve order, no stopword removal)"""
    phrase = query.strip().strip('"')
    phrase = clean_text(phrase)
    return tokenize(phrase)


def phrase_match(positional_index: dict, phrase_tokens: list) -> set:
    """
    Return set of docs where phrase_tokens appear consecutively in order.
    Uses positional index: word -> {doc: [positions]}
    """
    if not phrase_tokens:
        return set()

    # Start with docs that contain the first word
    first_word = phrase_tokens[0]
    if first_word not in positional_index:
        return set()

    candidate_docs = set(positional_index[first_word].keys())

    # Filter to docs containing ALL words in the phrase
    for word in phrase_tokens[1:]:
        if word not in positional_index:
            return set()
        candidate_docs &= set(positional_index[word].keys())

    matched_docs = set()

    for doc in candidate_docs:
        # Get starting positions of the first word in this doc
        start_positions = positional_index[first_word][doc]

        for start_pos in start_positions:
            # Check if subsequent words appear at consecutive positions
            match = True
            for offset, word in enumerate(phrase_tokens[1:], start=1):
                expected_pos = start_pos + offset
                if expected_pos not in positional_index[word][doc]:
                    match = False
                    break
            if match:
                matched_docs.add(doc)
                break  # No need to check other start positions for this doc

    return matched_docs


def search(index: dict, doc_lengths: dict, idf: dict, query: str, mode="OR", positional_index: dict = None) -> dict:
    """
    mode = "OR" or "AND"
    Supports phrase queries when query is wrapped in quotes e.g. "machine learning"
    """
    # --- Phrase search path ---
    if is_phrase_query(query) and positional_index is not None:
        phrase_tokens = extract_phrase_tokens(query)
        matched_docs = phrase_match(positional_index, phrase_tokens)

        # Score matched docs using TF-IDF on phrase tokens (stopwords removed for scoring)
        score_tokens = [t for t in phrase_tokens if t in idf]
        results = {}
        for doc in matched_docs:
            score = 0
            for word in score_tokens:
                if word in index and doc in index[word]:
                    freq = index[word][doc]
                    tf = freq / doc_lengths[doc]
                    score += tf * idf.get(word, 0)
            results[doc] = score
        return results

    # --- Normal keyword search path ---
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