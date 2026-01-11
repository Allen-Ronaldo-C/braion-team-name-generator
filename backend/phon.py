# backend/phon.py

def phonetic_blend(w1: str, w2: str) -> str:
    """
    Improved phonetic blending with multiple strategies
    """
    import random
    
    strategies = [
        # Strategy 1: First half + second half
        lambda: w1[:len(w1)//2] + w2[len(w2)//2:],
        
        # Strategy 2: First 2/3 + last 1/3
        lambda: w1[:2*len(w1)//3] + w2[len(w2)//3:],
        
        # Strategy 3: Portmanteau (overlap detection)
        lambda: create_portmanteau(w1, w2),
        
        # Strategy 4: Keep consonant clusters
        lambda: w1[:len(w1)//2+1] + w2[len(w2)//2:],
    ]
    
    result = random.choice(strategies)()
    return result.capitalize()


def create_portmanteau(w1: str, w2: str) -> str:
    """
    Find overlapping sounds and blend naturally
    """
    # Look for 2-3 character overlaps
    for overlap_len in range(3, 0, -1):
        if w1[-overlap_len:].lower() == w2[:overlap_len].lower():
            return w1 + w2[overlap_len:]
    
    # No overlap found, use default blend
    return w1[:len(w1)//2] + w2[len(w2)//2:]