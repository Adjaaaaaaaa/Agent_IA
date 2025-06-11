from langchain_core.tools import Tool

def check_css_eligibility(inputs: dict) -> str:
    # inputs attendu : dict avec âge, revenus, situation familiale etc.
    # Amélioré avec données officielles CSS 2024
    age = inputs.get("age", 0)
    revenus = inputs.get("revenus", 0)
    nb_personnes = inputs.get("nb_personnes", 1)
    
    # Plafonds CSS 2024 officiels
    plafonds_css = {1: 847, 2: 1271, 3: 1525, 4: 1779}
    plafond = plafonds_css.get(nb_personnes, 847)
    
    if age >= 18 and revenus <= plafond:
        return f"✅ Tu es éligible à la CSS gratuite (revenus {revenus}€ ≤ {plafond}€ pour {nb_personnes} personne(s))."
    elif age >= 18 and revenus <= plafond * 1.35:
        return f"🟡 Tu es éligible à la CSS avec participation (revenus {revenus}€ ≤ {int(plafond * 1.35)}€)."
    else:
        return f"❌ Tu n'es pas éligible à la CSS (revenus {revenus}€ > {int(plafond * 1.35)}€)."

eligibility_tool = Tool(
    name="CheckCSS",
    func=check_css_eligibility,
    description="Vérifie l'éligibilité à la Complémentaire Santé Solidaire (CSS)."
)
