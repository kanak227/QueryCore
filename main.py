from src.parser import parse_all_documents
from src.indexer import build_inverted_index
from src.search import search
from src.ranker import compute_idf

DATA_PATH = "data"


def main():
    # Step 1: Parse all documents
    docs = parse_all_documents(DATA_PATH)

    # Step 2: Build inverted index + doc lengths
    index, doc_lengths = build_inverted_index(docs)

    # Step 3: Compute IDF
    total_docs = len(docs)
    idf = compute_idf(index, total_docs)

    # Debug prints (optional)
    print("\n📏 Document Lengths:")
    for doc, length in doc_lengths.items():
        print(f"{doc} → {length}")

    print("\n📊 IDF Sample:")
    for word in list(idf.keys())[:5]:
        print(f"{word} → {idf[word]:.3f}")

    # Step 4: Search loop
    while True:
        query = input("\n🔍 Enter query (or 'exit'): ")

        if query.lower() == "exit":
            print("Exiting QueryCore...")
            break

        results = search(index, doc_lengths, idf, query)

        # Sort results by score (descending)
        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        print("\n📊 Results:")
        if not sorted_results:
            print("No results found.")
        else:
            for doc, score in sorted_results:
                print(f"{doc} → score: {score}")


if __name__ == "__main__":
    main()