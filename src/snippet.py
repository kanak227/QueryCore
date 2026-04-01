def generate_snippet(text: str, query_tokens: list, window=20):
    """
    Extract snippet around first matching word
    """
    words = text.split()

    for i, word in enumerate(words):
        word_clean = word.lower()

        if word_clean in query_tokens:
            start = max(0, i - window)
            end = min(len(words), i + window)

            snippet = " ".join(words[start:end])
            return "..." + snippet + "..."

    return text[:120] + "..."