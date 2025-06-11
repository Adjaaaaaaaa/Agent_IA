# Agent IA Santé Publique

## 🩺 Description

Ce projet vise à créer un **assistant IA citoyen** spécialisé en droit et aides à la santé publique.  
Il répond à des questions pratiques comme :  
- Quels vaccins sont obligatoires ?  
- Puis-je bénéficier de la CSS (Complémentaire Santé Solidaire) ?  
- À quel âge faire un dépistage ?  
- Comment comprendre simplement une procédure administrative ?

L’assistant utilise des technologies modernes basées sur LangChain, avec une base documentaire riche et une interface Streamlit simple et accessible.

---

## 🎯 Objectifs

- Fournir une aide claire et fiable en santé publique  
- Offrir une expérience interactive avec mémoire conversationnelle  
- Utiliser une chaîne RAG (Retrieval-Augmented Generation) pour s’appuyer sur des documents officiels  
- Intégrer des outils IA personnalisés (résumé, simplification, calcul d’éligibilité)

---

## ⚙️ Fonctionnalités principales

- Recherche intelligente dans documents santé (vaccins, aides sociales, procédures)  
- Résumé et simplification de textes administratifs  
- Vérification d’éligibilité à la CSS  
- Mémoire conversationnelle pour échanges fluides  
- Interface Streamlit intuitive  

---

## 🛠️ Architecture du projet
assistant_sante/
├── data/                  # Documents officiels (PDF, HTML, TXT)
├── tools/                 # Outils IA personnalisés (résumé, simplification, éligibilité)
├── main_agent.py          # Chaîne principale LangChain + outils
├── rag_chain.py           # Gestion base vectorielle et RAG
├── memory.py              # Mémoire conversationnelle
├── app.py                 # Interface utilisateur Streamlit
├── requirements.txt       # Dépendances Python
└── README.md              # Documentation du projet


---

## 📚 Technologies et librairies

- Python 3.8+  
- [LangChain](https://python.langchain.com)  
- Streamlit (interface utilisateur)  
- Chroma (base vectorielle)  
- Embeddings :  
  - Par défaut : `OllamaEmbeddings` (modèle `"nomic-embed-text"`)  
  - Optionnel : `DeepSeekEmbeddings` (décommenter dans `rag_chain.py` pour utiliser)  
- Autres outils IA personnalisés (résumé, simplification)

---

## 🚀 Installation

1. Cloner le dépôt :  
   ```bash
   git clone https://github.com/votre-utilisateur/agent-ia-sante.git
   cd agent-ia-sante



installation:
  - Créer un environnement virtuel et l’activer :
    - python -m venv .venv
    - source .venv/bin/activate   # Linux/Mac
    - .venv\Scripts\activate      # Windows
  - Installer les dépendances :
    - pip install -r requirements.txt
  - Lancer l’application :
    - streamlit run app.py

configuration_embeddings:
  description: |
    Le fichier rag_chain.py utilise par défaut OllamaEmbeddings.
    Pour changer vers DeepSeekEmbeddings :
    - Décommenter la ligne correspondante dans la fonction create_or_load_vectordb
    - Commenter ou supprimer la ligne Ollama

usage:
  - Posez vos questions santé dans l’interface Streamlit
  - L’assistant consulte la base documentaire via RAG
  - Il répond en s’appuyant sur des documents officiels et simplifie les réponses si nécessaire
  - Vous pouvez tester la mémoire conversationnelle en enchaînant les questions

limitations_et_ameliorations:
  - Améliorer la qualité des documents sources et leur mise à jour automatique
  - Ajouter d’autres modèles d’embeddings selon les besoins
  - Intégrer plus d’outils IA (ex : reconnaissance vocale, FAQ dynamique)
  - Optimiser la gestion mémoire et les performances en production

contribution: |
  N’hésitez pas à proposer des améliorations, remonter des bugs ou suggérer de nouvelles fonctionnalités via issues ou pull requests.

licence: |
  Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus d’informations.
