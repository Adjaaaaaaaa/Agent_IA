from langchain_core.tools import Tool

def simplify_text(text: str) -> str:
    # Exemple simplification factice (à remplacer par un vrai modèle/langage simple)
    return "Texte simplifié : " + (text[:300] + "..." if len(text) > 300 else text)

simplifier_tool = Tool(
    name="Simplifier",
    func=simplify_text,
    description="Simplifie un texte administratif en langage clair."
)
