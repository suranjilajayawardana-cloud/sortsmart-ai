# Architecture Documentation

This document describes the architectural layer of SortSmart.

## Baseline Architecture

The application follows a clean layered separation of concerns, extending the starter template to include a Retrieval-Augmented Generation (RAG) capability:

```text
User
  ↓
Gradio UI (app/ui.py)
  ↓
Application / AI Service (src/services/ai_service.py)
  ↓    ↑ 
  ↓  RAG Pipeline (src/capabilities/rag.py) ← TF-IDF Search ← Local JSON (data/recycling_rules.json)
  ↓
Model Client (src/models/model_client.py)
  ↓
Ollama (Local Inference Server)
  ↓
Local Model (llama3.2)