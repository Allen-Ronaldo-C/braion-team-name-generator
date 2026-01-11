import nltk
from nltk.corpus import wordnet as wn

try:
    wn.synsets('test')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

DOMAIN_WORDS = {
    "AI": ['neural', 'cognito', 'brain', 'smart', 'logic', 'learn', 'predict', 'vision'],
    "IoT": ['sensor', 'connect', 'mesh', 'node', 'edge', 'device', 'stream', 'pulse'],
    "Cybersecurity": ['shield', 'guard', 'secure', 'crypto', 'vault', 'cipher', 'defend'],
    "Healthcare": ['care', 'heal', 'vital', 'pulse', 'life', 'med', 'cure', 'wellness'],
    "Fintech": ['coin', 'trade', 'capital', 'fund', 'wealth', 'asset', 'ledger', 'mint'],
    "Sustainability": ['green', 'eco', 'renew', 'earth', 'pure', 'clean', 'grow', 'leaf'],
    "Gaming": ['pixel', 'quest', 'hero', 'level', 'arcade', 'play', 'arena', 'nexus'],
    "EdTech": ['learn', 'study', 'mentor', 'skill', 'bright', 'knowledge', 'scholar']
}

TECH_WORDS = [
    'nexus', 'quantum', 'neural', 'cyber', 'forge', 'vertex',
    'synapse', 'zenith', 'apex', 'prime', 'pulse', 'spark',
    'flux', 'nova', 'matrix', 'core', 'byte', 'pixel'
]

def expand(concepts: list[str], domain=None, custom_prompt=None) -> list[str]:
    """
    Semantic expansion with domain awareness and custom prompt consideration
    """
    expanded = set()

    for concept in concepts:
        expanded.add(concept.lower())

        # Add WordNet synonyms
        for syn in wn.synsets(concept):
            for lemma in syn.lemmas()[:3]:
                word = lemma.name().replace("_", " ").lower()
                if word.isalpha() and len(word) > 2:
                    expanded.add(word)
    
    # Add domain-specific words
    if domain and domain in DOMAIN_WORDS:
        expanded.update(DOMAIN_WORDS[domain])
    
    # Add general tech words
    expanded.update(TECH_WORDS[:10])
    
    # If custom prompt exists, extract additional words from it
    if custom_prompt:
        prompt_words = custom_prompt.lower().split()
        meaningful_words = [w for w in prompt_words if len(w) > 3 and w.isalpha()]
        expanded.update(meaningful_words[:5])
    
    return list(expanded)