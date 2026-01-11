def extract_concepts(text: str) -> list[str]:
    """
    Simple placeholder concept extractor.
    """
    words = text.lower().split()
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'for', 'with', 'to', 'in', 'on'}
    filtered = [w for w in words if w not in stop_words]
    return list(set(filtered))