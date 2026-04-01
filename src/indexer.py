from collections import Counter


def build_inverted_index(documents: dict):
    index = {}
    doc_lengths = {}

    for doc, data in documents.items():
        tokens = data["tokens"]

        doc_lengths[doc] = len(tokens)

        word_counts = Counter(tokens)

        for word, freq in word_counts.items():
            if word not in index:
                index[word] = {}

            index[word][doc] = freq

    return index, doc_lengths