from langchain_core.tools import Tool

def check_css_eligibility(inputs: dict) -> str:
    # inputs attendu : dict avec âge, revenus, situation familiale etc.
    # Exemple simplifié avec règles basiques (à améliorer)
    age = inputs.get("age", 0)
    revenus = inputs.get("revenus", 0)
    if age >= 18 and revenus < 10000:
        return "Tu es probablement éligible à la CSS."
    return "Tu n'es probablement pas éligible à la CSS."

eligibility_tool = Tool(
    name="CheckCSS",
    func=check_css_eligibility,
    description="Vérifie l'éligibilité à la Complémentaire Santé Solidaire (CSS)."
)
