# QueryCore

QueryCore is a small document search engine that builds an inverted index from text files in the `data/` directory and allows simple ranked search queries from the command line.

Files of interest

- `main.py` — CLI entrypoint. Builds or loads the index and runs an interactive query loop.
- `src/` — core modules (parser, indexer, search, ranker, snippet, storage).
- `data/` — plain text documents used as the corpus.

How to run

Make sure you have Python 3.8+ installed. From the project root:

```bash
python main.py
```

Usage

- Enter a search query at the prompt.
- Type `exit` to quit.
- When prompted, choose search mode `AND` or `OR` (case-insensitive).

Notes

- This README avoids emojis and uses plain text logging and prompts to be shell-friendly and accessible.
- If you want additional files or specific ignore rules added to `.gitignore`, tell me what to exclude.
