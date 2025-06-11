from langchain_core.tools import Tool

def summarize(text: str) -> str:
    # Ici tu peux appeler un modèle ou écrire ta logique résumé simple
    # Pour exemple, on fait un résumé factice (à remplacer)
    return text[:300] + "..." if len(text) > 300 else text

summarizer_tool = Tool(
    name="Summarizer",
    func=summarize,
    description="Résume un texte ou une procédure pour l'utilisateur."
)
