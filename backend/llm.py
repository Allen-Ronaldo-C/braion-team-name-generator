from dotenv import load_dotenv
import os
import requests
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

HF_API_KEY = os.getenv("HF_API_KEY")

def llm_rank_names(concepts, names, top_k=10, project_context=None, 
                   custom_prompt=None, tone=None, domain=None):
    """
    Rank team names using project context and custom instructions
    """
    if not HF_API_KEY:
        print("Warning: HF_API_KEY not set, returning unranked names")
        return names[:top_k]
    
    # Build rich prompt with all available context
    prompt_parts = ["You are a creative team name expert."]
    
    if project_context:
        prompt_parts.append(f"PROJECT CONTEXT: {project_context}")
    
    if custom_prompt:
        prompt_parts.append(f"CUSTOM REQUIREMENTS: {custom_prompt}")
    
    prompt_parts.extend([
        f"DOMAIN: {domain or 'General'}",
        f"TONE: {tone or 'Professional'}",
        f"KEY CONCEPTS: {', '.join(concepts)}",
        "",
        "CANDIDATE NAMES:",
        ', '.join(names),
        "",
        f"Task: Rank these names from BEST to WORST based on:"
    ])
    
    criteria = [
        "1. Memorability and pronunciation",
        f"2. Appropriateness for the tone ({tone})",
        f"3. Domain fit ({domain})"
    ]
    
    if project_context:
        criteria.insert(0, "1. Relevance to the project context")
    
    if custom_prompt:
        criteria.append(f"4. Alignment with custom requirements: {custom_prompt}")
    
    prompt_parts.extend(criteria)
    prompt_parts.append(f"\nReturn ONLY the top {top_k} names as a comma-separated list, nothing else.")
    
    prompt = "\n".join(prompt_parts)

    API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-3B-Instruct"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 300, "temperature": 0.7}
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if isinstance(result, list) and len(result) > 0:
            text = result[0].get('generated_text', '')
            ranked = [n.strip() for n in text.split(',') if n.strip() in names]
            return ranked[:top_k] if ranked else names[:top_k]
    except Exception as e:
        print(f"LLM ranking failed: {e}")
    
    return names[:top_k]