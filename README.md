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

Create a .env file in the root directory:
