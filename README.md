# ♻️ SortSmart: An AI Recycling Guide

**Group Members:** Suranjila Jayawardana and Madhuni Kanchana  
**Project Video Presentation:** [Insert your Unlisted YouTube or Google Drive link here]

## Repository Navigation
To assist with evaluation, our final documentation is located here:
* **Final Architecture & Decisions:** [`docs/architecture.md`](docs/architecture.md) and [`docs/project-decisions.md`](docs/project-decisions.md)
* **Evaluation & Test Cases:** [`evaluation/evaluation_results.md`](evaluation/evaluation_results.md)
* **Source Code:** Main UI in `app/` and AI/RAG logic in `src/`

**Intended Users and Problem:**

The intended users are students, households, and residents who are new to their local recycling system. People often struggle to decide where an item should be disposed of, especially when packaging contains multiple materials (e.g., "dirty pizza box" or "yogurt cup with a foil lid"). General knowledge often conflicts with specific local municipal sorting instructions, leading to recycling contamination.

**Why AI is Needed:**

Standard keyword searches fail when users describe items using synonyms, colloquialisms, or complex conditions (e.g., specifying that a container is still dirty). A Large Language Model (LLM) can understand the natural language context of the user's messy description, identify the core materials, and evaluate them against specific rule conditions.

**Proposed Solution and Main Workflow:**

SortSmart is a web application that helps users identify the correct waste category for a described item based strictly on a provided set of local sorting rules.

The user types an item description into the interface (e.g., "empty plastic yoghurt cup with the foil lid attached").
The application retrieves the relevant local sorting guidelines from its knowledge base.

The AI model analyzes the user's item against the retrieved rules.

The application outputs the suggested waste category, a brief explanation citing the rule, and handles uncertain cases by asking for clarification (e.g., "Is the plastic cup rinsed?").

**Initial Architecture:**
The application strictly separates the UI from the AI logic, built upon the course's starter template.

**User Interface: **Gradio web interface for input and displaying categorized results.

**Application Logic:** Python backend handling the RAG pipeline (document chunking and retrieval) and prompt formatting.

**AI Integration:** Local Ollama service handling the LLM generation based on the retrieved context.

**Planned Additional AI Capability and Justification:**

Retrieval-Augmented Generation (RAG).
LLMs are prone to hallucinating waste management rules or providing generic advice that violates local municipal guidelines. RAG is essential for this problem because it forces the model to ground its answers in a specific, provided dataset of local sorting rules. If a rule is not in the retrieval context, the model will be instructed to admit it does not know, ensuring high reliability and preventing authoritative but incorrect guidance.

**Planned Model and Runtime:**

The application will use a lightweight local LLM (such as llama3.2 or mistral) running via Ollama. This ensures reproducible execution without relying on paid external APIs, fulfilling the course's reproducibility and secrecy requirements.
