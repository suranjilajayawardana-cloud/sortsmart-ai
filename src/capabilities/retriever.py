import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_rules(filepath="data/recycling_rules.json"):
    # Navigate up from src/capabilities -> src -> root directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    full_path = os.path.join(base_dir, filepath)
    
    with open(full_path, 'r') as f:
        return json.load(f)

def retrieve_relevant_rule(query, rules_data):
    """Finds the most relevant recycling rule using TF-IDF text similarity."""
    documents = [f"{r['category']} {r['description']} {r['condition']}" for r in rules_data]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vec = vectorizer.transform([query])
    
    similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()
    best_match_idx = similarities.argmax()
    
    if similarities[best_match_idx] > 0.05: 
        return rules_data[best_match_idx]
    
    return None