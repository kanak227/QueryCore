from src.parser import parse_all_documents
from src.indexer import build_inverted_index
from src.search import search

DATA_PATH = "data"

if __name__ == "__main__":
    docs = parse_all_documents(DATA_PATH)
    index = build_inverted_index(docs)

    while True:
        query = input("\n Enter query (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = search(index, query)

        # sort results by score
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        print("\n Results:")
        for doc, score in sorted_results:
            print(f"{doc} → score: {score}")