from typing import List
import numpy as np


def get_embedding(text: str) -> np.ndarray:
    """
    Dummy embedding for now.
    Replace later with SentenceTransformer / OpenAI / etc.
    """
    np.random.seed(abs(hash(text)) % (2**32))
    return np.random.rand(384)


def embed_and_rank(names: List[str], query: str) -> List[str]:
    """
    Rank generated names based on similarity to query.
    """
    query_emb = get_embedding(query)

    scored = []
    for name in names:
        name_emb = get_embedding(name)
        score = cosine_similarity(query_emb, name_emb)
        scored.append((score, name))

    scored.sort(reverse=True)
    return [name for _, name in scored]


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
