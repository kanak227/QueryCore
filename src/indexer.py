from collections import Counter


def build_inverted_index(documents: dict) -> dict:
    """
    Build inverted index:
    word → {doc: frequency}
    """
    index = {}

    for doc, tokens in documents.items():
        word_counts = Counter(tokens)

        for word, freq in word_counts.items():
            if word not in index:
                index[word] = {}

            index[word][doc] = freq

    return index