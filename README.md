# AI engineering course

https://www.youtube.com/watch?v=WIW5hN-hApQ

## Requirements

- Python 3.12
- [Pipenv](https://pipenv.pypa.io/)
- A Groq API key. Some scripts also need a Hugging Face token, a Tavily key, or Postgres.

## Setup

```bash
pipenv install
pipenv shell
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=<your groq key>
HF_TOKEN=<your hugging face token>      # chat_bot.py (gated Llama tokenizer)
TAVILY_API_KEY=<your tavily key>        # agent.py (web search tool)
DATABASE_URL=<postgres connection uri>  # checkpointers.py
```

Every script calls `dotenv.load_dotenv()`, so the file is picked up automatically.

## Running

```bash
pipenv run python rag.py
```

Scripts with a `chat_loop` / `chat` REPL read from stdin — type `q` to exit.

## Scripts

| File | What it does |
| --- | --- |
| `chat_bot.py` | Streaming chat bot over the Groq OpenAI-compatible API. Trims and periodically summarizes history, counts tokens with the Llama 3.1 tokenizer, enforces a prompt-length and daily token budget, and reports estimated cost. |
| `sentiment_analysis.py` | Zero-shot sentiment classification with a local `transformers` pipeline (`typeform/distilbert-base-uncased-mnli`) — no API calls. |
| `embedding.py` | Sentence embeddings with `sentence-transformers/all-MiniLM-L6-v2`; cosine similarity search over a list of sentences, both by hand and via `util.semantic_search`. |
| `rag.py` | Retrieval-augmented QA over `symptoms.pdf`. Splits pages with a tiktoken-aware splitter, embeds with MiniLM, persists to a Chroma store in `./chroma`, then answers questions with a source-citing, grounded-only system prompt. |
| `agent.py` | LangChain agent with two tools: a stub `get_weather` and Tavily web search. Keeps a running message list across turns. |
| `checkpointers.py` | Agent with a `PostgresSaver` checkpointer and `SummarizationMiddleware`. Two thread IDs demonstrate persistent, switchable sessions (`ch` toggles between them); prints final state on exit. |
| `graph.py` | LangGraph write → review loop. A draft node and a scoring node run until the score hits 10 or three revisions are used, with feedback fed back into the next draft. |
| `multi_agent.py` | Supervisor pattern: a main agent delegates to a fruit expert and a veggie expert, each exposed to it as a tool. |
| `prompt_template.py` | Structured output — a Pydantic `User` model extracted from a biography paragraph via `with_structured_output(..., method='json_schema')`. |
| `pydantic_validation.py` | Scratch file for Pydantic model behavior. |

## Notes

- Chunks in `rag.py` are keyed by an MD5 of their content, so re-running the script re-ingests
  the PDF idempotently rather than duplicating documents.
- `chat_bot.py` and `rag.py` read the env var as `GROQ_APIT_KEY` (note the typo), which does not
  match `GROQ_API_KEY` in `.env`. Either fix the variable name in the code or define both.
- `chroma/` and `.env` are gitignored — the vector store rebuilds itself on the next `rag.py` run.
