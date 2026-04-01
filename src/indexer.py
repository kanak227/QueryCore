from collections import Counter


def build_inverted_index(documents: dict):
    """
    Build:
    1. Inverted index → word → {doc: frequency}
    2. Document lengths → doc → total words
    """
    index = {}
    doc_lengths = {}

    for doc, tokens in documents.items():
        # store document length
        doc_lengths[doc] = len(tokens)

        # count word frequency in this document
        word_counts = Counter(tokens)

        for word, freq in word_counts.items():
            if word not in index:
                index[word] = {}

            index[word][doc] = freq

    return index, doc_lengths