from backend.sem import expand
from backend.phon import phonetic_blend
from backend.llm import llm_rank_names
import random

def generate_names(concepts, count=10, use_llm=False, tone="professional", 
                   domain=None, project_context=None, custom_prompt=None):
    """
    Generate both meaningful AND creative/random team names
    """
    all_names = {
        'meaningful': [],
        'creative': []
    }
    
    # Generate meaningful names (context-based)
    meaningful_names = generate_meaningful_names(concepts, domain, tone, count//2)
    all_names['meaningful'] = meaningful_names
    
    # Generate creative/cool random names
    creative_names = generate_creative_names(concepts, domain, tone, count//2)
    all_names['creative'] = creative_names
    
    # Combine for LLM ranking if enabled
    if use_llm and (project_context or custom_prompt):
        combined = meaningful_names + creative_names
        ranked = llm_rank_names(
            concepts, 
            combined, 
            top_k=count,
            project_context=project_context,
            custom_prompt=custom_prompt,
            tone=tone,
            domain=domain
        )
        # Redistribute after ranking
        return {
            'meaningful': [n for n in ranked if n in meaningful_names][:count//2],
            'creative': [n for n in ranked if n in creative_names][:count//2]
        }
    
    return all_names


def generate_meaningful_names(concepts, domain, tone, count):
    """
    Generate meaningful names based on actual concepts and domain
    """
    words = expand(concepts, domain=domain)
    tone_words = get_tone_words(tone)
    words.extend(tone_words)
    
    names = set()
    attempts = 0
    
    # Strategy 1: Direct concept combinations
    for concept in concepts[:3]:
        for word in words[:10]:
            if word != concept.lower():
                blend = phonetic_blend(concept.capitalize(), word.capitalize())
                if is_valid_name(blend, tone):
                    names.add(blend)
                
                # Also try compound words
                compound = concept.capitalize() + word.capitalize()
                if 5 <= len(compound) <= 15:
                    names.add(compound)
    
    # Strategy 2: Semantic blending
    while len(names) < count * 3 and attempts < 1000:
        if len(words) >= 2:
            w1, w2 = random.sample(words, 2)
            blend = phonetic_blend(w1, w2)
            if is_valid_name(blend, tone):
                names.add(blend)
        attempts += 1
    
    return sorted(list(names), key=lambda x: len(x))[:count]


def generate_creative_names(concepts, domain, tone, count):
    """
    Generate cool, random, creative names that sound awesome
    """
    # Cool prefixes and suffixes
    cool_prefixes = [
        'Neo', 'Hyper', 'Ultra', 'Meta', 'Quantum', 'Cyber', 'Infinity',
        'Alpha', 'Beta', 'Gamma', 'Delta', 'Omega', 'Prime', 'Apex',
        'Nexus', 'Zenith', 'Vertex', 'Vortex', 'Eclipse', 'Phoenix',
        'Nova', 'Stellar', 'Cosmic', 'Astro', 'Lunar', 'Solar'
    ]
    
    cool_suffixes = [
        'Labs', 'Tech', 'Dynamics', 'Systems', 'Solutions', 'Innovations',
        'Squad', 'Crew', 'Force', 'Guild', 'Collective', 'Alliance',
        'Hub', 'Core', 'Forge', 'Works', 'Studio', 'Vector',
        'Pulse', 'Wave', 'Flow', 'Spark', 'Flux', 'Matrix'
    ]
    
    cool_words = [
        'Titan', 'Phantom', 'Storm', 'Thunder', 'Lightning', 'Blaze',
        'Shadow', 'Ghost', 'Raven', 'Wolf', 'Dragon', 'Phoenix',
        'Pulse', 'Echo', 'Fusion', 'Synergy', 'Catalyst', 'Impulse',
        'Velocity', 'Momentum', 'Orbit', 'Gravity', 'Photon', 'Electron'
    ]
    
    # Domain-specific cool words
    domain_cool_words = {
        'AI': ['Neural', 'Cognito', 'Synapse', 'Logic', 'Vision', 'Mind'],
        'IoT': ['Mesh', 'Node', 'Signal', 'Beacon', 'Stream', 'Link'],
        'Cybersecurity': ['Cipher', 'Vault', 'Shield', 'Guard', 'Sentinel'],
        'Healthcare': ['Vital', 'Remedy', 'Cure', 'Heal', 'Pulse', 'Life'],
        'Sustainability': ['Terra', 'Eco', 'Green', 'Pure', 'Verdant'],
        'Gaming': ['Pixel', 'Arena', 'Quest', 'Hero', 'Legend', 'Epic']
    }
    
    names = set()
    
    # Strategy 1: Prefix + Cool Word
    for prefix in random.sample(cool_prefixes, min(10, len(cool_prefixes))):
        for word in random.sample(cool_words, min(5, len(cool_words))):
            names.add(prefix + word)
    
    # Strategy 2: Cool Word + Suffix
    for word in random.sample(cool_words, min(10, len(cool_words))):
        for suffix in random.sample(cool_suffixes, min(5, len(cool_suffixes))):
            names.add(word + suffix)
    
    # Strategy 3: Domain-specific combinations
    if domain:
        # Handle multiple domains (domain could be "AI and IoT")
        domain_parts = domain.replace(' and ', ',').split(',')
        for domain_part in domain_parts:
            domain_part = domain_part.strip()
            if domain_part in domain_cool_words:
                domain_words = domain_cool_words[domain_part]
                for dword in domain_words:
                    # Combine with prefixes
                    for prefix in random.sample(cool_prefixes, 3):
                        names.add(prefix + dword)
                    # Combine with suffixes
                    for suffix in random.sample(cool_suffixes, 3):
                        names.add(dword + suffix)
    
    # Strategy 4: Pure random cool combinations
    for _ in range(count * 2):
        strategy = random.choice(['prefix_word', 'word_suffix', 'word_word'])
        
        if strategy == 'prefix_word':
            name = random.choice(cool_prefixes) + random.choice(cool_words)
        elif strategy == 'word_suffix':
            name = random.choice(cool_words) + random.choice(cool_suffixes)
        else:
            name = random.choice(cool_words) + random.choice(cool_words)
        
        if 5 <= len(name) <= 18:
            names.add(name)
    
    # Filter and sort
    filtered = [n for n in names if is_valid_name(n, tone)]
    return sorted(filtered, key=lambda x: (len(x), x))[:count]


def is_valid_name(name: str, tone: str) -> bool:
    """
    Check if name is valid for the given tone
    """
    if len(name) < 4 or len(name) > 18:
        return False
    
    if tone == "minimal" and len(name) > 10:
        return False
    
    # Basic pronounceability check
    consonants = 'bcdfghjklmnpqrstvwxyz'
    consonant_count = 0
    
    for char in name.lower():
        if not char.isalpha():
            return False
        if char in consonants:
            consonant_count += 1
            if consonant_count > 4:
                return False
        else:
            consonant_count = 0
    
    return True


def get_tone_words(tone: str) -> list[str]:
    """
    Return words that match the requested tone
    """
    tone_map = {
        "professional": ["pro", "tech", "solutions", "systems", "group", "labs", "enterprise"],
        "cool": ["nexus", "vibe", "squad", "collective", "crew", "alliance", "wave"],
        "funny": ["ninja", "wizard", "guru", "maverick", "pirates", "bandits", "legends"],
        "aggressive": ["force", "dominate", "titan", "warrior", "storm", "thunder", "conquer"],
        "minimal": ["dot", "dash", "line", "edge", "core", "arc", "node"]
    }
    return tone_map.get(tone, [])