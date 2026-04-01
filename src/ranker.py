import math


def compute_idf(index: dict, total_docs: int) -> dict:
    """
    Compute IDF for each word
    """
    idf = {}

    for word, doc_dict in index.items():
        df = len(doc_dict)
        if df == 0:
            continue

        idf[word] = math.log(total_docs / df)

    return idf