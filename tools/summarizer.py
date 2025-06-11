from langchain_core.tools import Tool

def summarize(text: str) -> str:
    # Résumé amélioré court et simple
    if len(text) <= 200:
        return text
    
    # Détection contexte santé
    text_lower = text.lower()
    
    if 'ald' in text_lower or 'affection' in text_lower:
        return f"📋 ALD: Prise en charge 100% pathologie chronique. {text[:100]}..."
    elif 'css' in text_lower or 'complémentaire' in text_lower:
        return f"💰 CSS: Aide santé selon revenus (847€-1779€). {text[:100]}..."
    elif 'ame' in text_lower:
        return f"🌍 AME: Soins gratuits résidents irréguliers. {text[:100]}..."
    else:
        # Résumé simple: prendre début + fin
        return text[:150] + "..." + text[-50:] if len(text) > 200 else text

summarizer_tool = Tool(
    name="Summarizer",
    func=summarize,
    description="Résume un texte ou une procédure pour l'utilisateur."
)
