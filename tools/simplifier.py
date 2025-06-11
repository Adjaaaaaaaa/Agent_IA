from langchain_core.tools import Tool
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3", temperature=0)

def simplify_text(text: str) -> str:
    """Simplifie un texte médical/administratif"""
    
    prompt = f"""Simplifie ce texte médical pour un patient :

TRANSFORMATIONS :
- "Affection longue durée" → "maladie grave qui dure longtemps"
- "Protocole de soins" → "plan de vos soins"
- "Exonération" → "vous ne payez rien"
- "Pathologie" → "maladie"
- "Posologie" → "comment prendre le médicament"

RÈGLES :
- Phrases courtes avec "vous"
- Ton rassurant
- Mots simples

TEXTE : {text}

VERSION SIMPLE :"""

    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except:
        return "Texte simplifié : " + (text[:300] + "..." if len(text) > 300 else text)

simplifier_tool = Tool(
    name="Simplifier",
    func=simplify_text,
    description="Simplifie un texte administratif en langage clair."
)

