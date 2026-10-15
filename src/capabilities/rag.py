"""
Retrieval-Augmented Generation (RAG) capability for SortSmart.

Loads documented municipal recycling rules and retrieves the top matching
rules using TF-IDF similarity to ground the LLM response.
"""

import json
import os
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_rules(filepath: str = "data/recycling_rules.json") -> List[Dict[str, Any]]:
    """Loads the local recycling rule knowledge base from JSON."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    full_path = os.path.join(base_dir, filepath)

    with open(full_path, "r", encoding="utf-8") as file:
        return json.load(file)


def retrieve_relevant_rules(
    query: str, rules_data: List[Dict[str, Any]], top_k: int = 2
) -> List[Dict[str, Any]]:
    """
    Finds the most relevant recycling rules using TF-IDF cosine similarity.
    Returns up to `top_k` rules that exceed the relevance threshold to handle
    multi-material items (e.g., 'plastic yogurt cup with foil lid').
    """
    if not query or not query.strip() or not rules_data:
        return []

    documents = [
        f"{r['category']} {r.get('examples', '')} {r['description']} {r['condition']}"
        for r in rules_data
    ]

    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vec = vectorizer.transform([query.lower()])

    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    ranked_indices = similarities.argsort()[::-1]

    matched_rules = []
    for idx in ranked_indices[:top_k]:
        if similarities[idx] >= 0.08:
            matched_rules.append(rules_data[idx])

    return matched_rules


def build_rag_prompt(user_query: str) -> str:
    """
    Executes retrieval and constructs a grounded prompt for the LLM.
    """
    rules = load_rules()
    matched_rules = retrieve_relevant_rules(user_query, rules)

    if matched_rules:
        context_blocks = []
        for rule in matched_rules:
            context_blocks.append(
                f"- Category: {rule['category']}\n"
                f"  What belongs here: {rule['description']} (Examples: {rule.get('examples', '')})\n"
                f"  Sorting Condition: {rule['condition']}\n"
                f"  Rule Source: {rule.get('source', 'Local Municipal Guidelines')}"
            )
        context_text = "\n\n".join(context_blocks)
    else:
        context_text = (
            "No matching rule was found in the local SortSmart knowledge base."
        )

    return f"""You are SortSmart, a reliable AI Recycling Guide.
Use ONLY the retrieved local sorting rules below to answer the user's disposal question.

Instructions:
1. State the recommended Waste Category clearly at the start.
2. Explain why based strictly on the retrieved rule and mention any important condition (such as rinsing, flattening, or separating lids).
3. If the user's description is missing a critical detail (for example, whether a container is empty/clean), ask a brief clarifying question.
4. Cite the Rule Source provided in the context, and remind the user to verify with their local municipality if unsure.
5. If the context says no matching rule was found, state clearly that SortSmart cannot determine the category from its current rule set and advise checking the local waste provider's instructions. Do NOT invent rules.

Retrieved Local Rules:
{context_text}

User Item Description: {user_query}
Sorting Guidance:"""