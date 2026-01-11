from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from backend.concept import extract_concepts
from backend.gen import generate_names

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    description: str
    project_description: Optional[str] = None
    custom_prompt: Optional[str] = None
    tone: Optional[str] = "professional"
    domain: Optional[str] = None
    purpose: Optional[str] = "hackathon"

@app.post("/generate")
def generate(req: Request):
    # Build full context from all available inputs
    full_context = req.description
    
    if req.project_description:
        full_context += " " + req.project_description
    
    if req.custom_prompt:
        full_context += " " + req.custom_prompt
    
    # Extract key concepts from the full context
    concepts = extract_concepts(full_context)
    
    print(f"DEBUG - Concepts: {concepts}")  # DEBUG
    
    # Generate names based on concepts and parameters
    result = generate_names(
        concepts, 
        count=10,
        tone=req.tone,
        domain=req.domain,
        project_context=req.project_description,
        custom_prompt=req.custom_prompt
    )
    
    print(f"DEBUG - Result type: {type(result)}")  # DEBUG
    print(f"DEBUG - Result content: {result}")  # DEBUG
    
    # Handle different return types
    meaningful = []
    creative = []
    
    if isinstance(result, dict):
        # If result is a dictionary
        print("DEBUG - Result is a dict")
        
        # Check for different possible keys
        if 'meaningful_names' in result and 'creative_names' in result:
            meaningful = result.get('meaningful_names', [])
            creative = result.get('creative_names', [])
        elif 'names' in result:
            names_list = result['names']
            mid_point = len(names_list) // 2
            meaningful = names_list[:mid_point] if len(names_list) > 0 else []
            creative = names_list[mid_point:] if len(names_list) > 0 else []
        else:
            # Try to get any list values from the dict
            for key, value in result.items():
                if isinstance(value, list) and len(value) > 0:
                    names_list = value
                    mid_point = len(names_list) // 2
                    meaningful = names_list[:mid_point]
                    creative = names_list[mid_point:]
                    break
    
    elif isinstance(result, list):
        # If result is a list
        print("DEBUG - Result is a list")
        mid_point = len(result) // 2
        meaningful = result[:mid_point] if len(result) > 0 else []
        creative = result[mid_point:] if len(result) > 0 else []
    
    else:
        print(f"DEBUG - Unexpected result type: {type(result)}")
    
    print(f"DEBUG - Meaningful names: {meaningful}")  # DEBUG
    print(f"DEBUG - Creative names: {creative}")  # DEBUG
    
    return {
        "concepts": concepts,
        "meaningful_names": meaningful,
        "creative_names": creative,
        "context": {
            "tone": req.tone,
            "domain": req.domain,
            "purpose": req.purpose,
            "has_project_desc": bool(req.project_description),
            "has_custom_prompt": bool(req.custom_prompt)
        }
    }

# Health check endpoint
@app.get("/")
def read_root():
    return {"status": "ok", "message": "Braion API is running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "braion-api"}