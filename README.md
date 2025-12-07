# Contract Intelligence API

## 📖 Overview
This is a "production-ish" API designed to ingest legal contracts (PDFs), extract structured data, answer questions (RAG), and audit documents for risk. It is built using FastAPI, PostgreSQL (pgvector), and Google Gemini.

## 🚀 Features
 * **Ingestion Pipeline:** Parses PDFs, chunks text, and generates vector embeddings using a local Hugging Face model (all-MiniLM-L6-v2).

 * **Structured Extraction:** Uses LLM Function Calling to extract parties, dates, liability caps, and terms into valid JSON.

 * **RAG (Q&A):** Answers natural language questions based only on the document context with citations.

 * **Risk Audit:** Automatically detects high-risk clauses (e.g., Unlimited Liability, Auto-renewal < 30 days).

 * **Observability:** Includes Health checks (/healthz) and Prometheus Metrics (/metrics).

## 🛠️ Tech Stack
 * **Framework:** FastAPI (Python 3.10+)

 * **Database:** PostgreSQL 16 + pgvector extension

 * **LLM:** Google Gemini 1.5 Flash (via LangChain)

 * **Embeddings:** HuggingFace sentence-transformers/all-MiniLM-L6-v2 (Local/CPU)

 * **Infrastructure:** Docker & Docker Compose

 * **Testing:** Pytest & Custom LLM-as-a-Judge Eval script

## ⚡ Quick Start

**1. Prerequisites**
 * Docker & Docker Compose

 * Google AI Studio API Key (Free tier available)

**2. Configuration**

 * Create a .env file in the root directory:
 * Populate it with your credentials:
   ```
   DATABASE_URL=postgresql://user:password@db:5432/contract_db
   GOOGLE_API_KEY=AIzaSyYourKeyHere...
   ```

***3. Run the Application***

Build and start the containerized services:
```
docker-compose up --build
```
 * **API:** http://localhost:8000

 * **Swagger Docs:** http://localhost:8000/docs

 * **Database:** Port 5432

## 🏗️ Design Decisions & Trade-offs
1. **FastAPI vs Django:** Chosen FastAPI for native async support (critical for LLM streaming/concurrency) and Pydantic integration for strict data validation.

2. **Postgres (pgvector) vs. Pinecone:**

 * Decision: Used pgvector.

 * Rationale: Reduces infrastructure complexity. Metadata (Document ID) and Vectors live in the same DB, making joins and filtering easier and transactionally safe.

3. **Embeddings (Local vs. OpenAI):**

 * Decision: Used HuggingFace (all-MiniLM-L6-v2) running locally.

 * Trade-off: Saves money and ensures data privacy for embeddings, but is slightly slower on CPU than an API call to OpenAI's text-embedding-3-small.

4. **Sync vs. Async Ingestion:**

 * Current Implementation: The /ingest endpoint processes files synchronously.

 * Production Trade-off: In a real high-scale system, this would be offloaded to a Celery/Redis worker queue to prevent blocking the API thread during large PDF uploads.

5. **LLM Choice:**

 * Decision: **Gemini 1.5 Flash.**

 * Rationale: High speed, low cost, and massive context window (1M tokens) allowing for potential full-document analysis without complex windowing strategies.
