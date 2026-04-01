from collections import Counter


def build_inverted_index(documents: dict):
    index = {}
    positional_index = {}
    doc_lengths = {}

    for doc, data in documents.items():
        tokens = data["tokens"]

        doc_lengths[doc] = len(tokens)

        word_counts = Counter(tokens)

        for word, freq in word_counts.items():
            if word not in index:
                index[word] = {}
            index[word][doc] = freq

        # Build positional index: word -> {doc: [positions]}
        for position, word in enumerate(tokens):
            if word not in positional_index:
                positional_index[word] = {}
            if doc not in positional_index[word]:
                positional_index[word][doc] = []
            positional_index[word][doc].append(position)

    return index, doc_lengths, positional_index