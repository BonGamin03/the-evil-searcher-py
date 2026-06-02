# the-evil-searcher-py

A full-stack search engine specialized in football news, built from scratch using classical Information Retrieval techniques combined with modern NLP and generative AI. The system indexes articles scraped from major sports outlets and delivers ranked results alongside an LLM-generated answer when the query warrants it.

---

## Architecture

The project is organized around a clean **layered architecture** that separates concerns across three main layers:

```
┌─────────────────────────────────────────┐
│              Frontend (React)           │  Search UI · Results · AI answer panel
├─────────────────────────────────────────┤
│           Backend (FastAPI)             │  REST API · Use case orchestration
├────────────────┬────────────────────────┤
│   Application  │       Domain           │  Use cases · Pure IR logic & models
├────────────────┴────────────────────────┤
│             Infrastructure              │  DB · Vector store · LLM · Scrapers
├──────────────────────────────────────────┤
│   MongoDB        ChromaDB        HF API  │  Persistence layer
└──────────────────────────────────────────┘
```

### Domain layer

All core IR logic lives here, with no external dependencies:

- **`InvertedIndex`** — in-memory term → posting list mapping. Each posting list is backed by a custom **SkipList** that supports O(log n) inserts and efficient AND-query intersection between posting lists.
- **`ProbabilisticModel`** — implements the **Binary Independence Model (BIM)**. Scores documents against a query by computing per-term weights using log-odds of relevance probability, with iterative refinement across retrieval rounds.
- **`LocalRankingCalculator`** — boosts results based on content/location affinity (e.g. La Liga articles rank higher for users in Spain).
- **`OrganicRankingCalculator`** — blends relevance (50%), domain authority (30%), and freshness (20%) into a final organic score.

### Application layer

Use cases that orchestrate the domain and infrastructure:

| Use case | Responsibility |
|---|---|
| `SmartSearchUseCase` | Main search pipeline — expands the query, retrieves candidates, triggers ranking |
| `RankingOrchestrationUseCase` | Combines BIM scores, semantic scores, local & organic signals into final ranking |
| `BuildInvertedIndexUseCase` | Loads all documents from MongoDB and builds the in-memory inverted index at startup |
| `LoadEmbeddingsUseCase` | Generates and persists document embeddings into ChromaDB |
| `SnippetExtractorUseCase` | Extracts a featured snippet from the top result using an LLM re-ranker |
| `RunScraperUseCase` | Triggers the Scrapy crawlers on demand |

### Infrastructure layer

Concrete implementations of the domain interfaces:

- **Scrapy crawlers** — four spiders targeting ESPN, Marca, AS, and TUDN. Each spider handles date extraction and stores articles into MongoDB.
- **`DocumentProcessor`** (spaCy) — tokenization, lemmatization, and stopword removal for Spanish text.
- **`HGEmbeddingGen`** — wraps `sentence-transformers/all-MiniLM-L6-v2` to generate dense vector representations.
- **`ChromaVectorRepository`** — persists and queries embeddings using cosine similarity via ChromaDB.
- **`Word2VecQueryExpander`** — trains or loads a Word2Vec model on the corpus and expands the user's query with semantically related football terms.
- **`MetaLLamaRAG`** — calls `meta-llama/Llama-3.1-8B-Instruct` via Hugging Face Inference API to generate a direct answer from retrieved context.
- **`ReRankCTexts`** — re-ranks document chunks using an LLM to extract the most relevant snippet.
- **`ZenserpSearcher`** — fallback organic web search via Zenserp API when local results are insufficient.

### Search pipeline (end-to-end)

```
User query
    │
    ▼
Query expansion (Word2Vec) ──► expanded terms
    │
    ├──► Inverted index (AND query) ──► BIM scoring
    │
    └──► ChromaDB (cosine similarity) ──► semantic scoring
              │
              ▼
    Ranking orchestration
    (BIM + semantic + freshness + authority + location)
              │
              ▼
    Featured snippet extraction (LLM re-ranker)
              │
              ▼
    RAG answer generation (Llama 3.1 8B)
              │
              ▼
    Results returned to frontend
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React · TypeScript · Vite · Tailwind CSS |
| Backend | Python · FastAPI · Uvicorn |
| Database | MongoDB |
| Vector store | ChromaDB |
| NLP | spaCy · Gensim (Word2Vec) · Sentence Transformers |
| LLM / RAG | Llama 3.1 8B via Hugging Face Inference API |
| Web scraping | Scrapy |
| Infrastructure | Docker · Docker Compose |

---

## Running with Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/) installed.


### Steps

**1. Clone the repository**

```bash
git clone https://github.com/BonGamin03/the-evil-searcher-py.git
cd the-evil-searcher-py
```

**2. Configure environment variables** *(optional)*

Create a `.env` file at the project root to override the defaults:

```env
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=admin
MONGO_INITDB_DATABASE=evil_searcher
MONGODB_PORT=27017
HF_TOKEN=your_huggingface_token   # required for RAG
ZENSERP_API_KEY=your_api_key # required for web search
```

**3. Start the services**

```bash
docker compose up --build
```

This spins up three containers:

| Service | URL |
|---|---|
| Frontend (Vite) | http://localhost:5173 |
| Backend (FastAPI) | http://localhost:8000 |
| MongoDB | localhost:27017 |

**4. Populate the database** *(first run)*

Once the containers are up, trigger the scrapers to collect articles:

```bash
docker exec -it evil_api python crawl.py
```

**5. Stop the services**

```bash
docker compose down
```

To also remove persistent data volumes:

```bash
docker compose down -v
```