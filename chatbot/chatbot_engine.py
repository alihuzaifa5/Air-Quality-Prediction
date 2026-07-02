import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

with open("chatbot/knowledge_base.json", "r") as f:
    KNOWLEDGE = json.load(f)

corpus = []
for entry in KNOWLEDGE:
    text = entry["topic"].replace("_", " ") + " " + " ".join(entry["keywords"])
    corpus.append(text)

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

def search(question: str, threshold=0.15):
    q_vec = vectorizer.transform([question.lower()])
    scores = cosine_similarity(q_vec, tfidf_matrix).flatten()
    best_idx = np.argmax(scores)

    if scores[best_idx] < threshold:
        return None, 0.0

    return KNOWLEDGE[best_idx], scores[best_idx]