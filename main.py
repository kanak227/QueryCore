from src.parser import parse_all_documents
from src.indexer import build_inverted_index
from src.search import search, process_query
from src.ranker import compute_idf
from src.snippet import generate_snippet

DATA_PATH = "data"


def main():
    docs = parse_all_documents(DATA_PATH)

    index, doc_lengths = build_inverted_index(docs)

    total_docs = len(docs)
    idf = compute_idf(index, total_docs)

    while True:
        query = input("\n Enter query (or 'exit'): ")

        if query.lower() == "exit":
            print("Exiting QueryCore...")
            break

        mode_input = input("Choose mode (AND/OR): ").strip().upper()
        mode = "AND" if mode_input == "AND" else "OR"

        results = search(index, doc_lengths, idf, query, mode)

        sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

        query_tokens = process_query(query)

        print("\n Results:")
        if not sorted_results:
            print("No results found.")
        else:
            for doc, score in sorted_results:
                text = docs[doc]["text"]
                snippet = generate_snippet(text, query_tokens)

                print(f"\n {doc} → score: {score:.3f}")
                print(snippet)


if __name__ == "__main__":
    main()