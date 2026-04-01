import pickle
import os

INDEX_PATH = "index/index.pkl"


def save_index(index, doc_lengths, idf):
    """
    Save index data to disk
    """
    os.makedirs("index", exist_ok=True)

    with open(INDEX_PATH, "wb") as f:
        pickle.dump({
            "index": index,
            "doc_lengths": doc_lengths,
            "idf": idf
        }, f)

    print(" Index saved successfully!")


def load_index():
    """
    Load index data from disk
    """
    if not os.path.exists(INDEX_PATH):
        return None

    with open(INDEX_PATH, "rb") as f:
        data = pickle.load(f)

    print("Index loaded from disk!")

    return data["index"], data["doc_lengths"], data["idf"]