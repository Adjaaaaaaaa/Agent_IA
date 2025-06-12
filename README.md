# Agent IA - Assistant Conversationnel Intelligent

## 🏥 Contexte et Objectif

## 📝 Description
Agent IA est un assistant conversationnel intelligent basé sur l'architecture RAG (Retrieval-Augmented Generation) qui permet d'interagir avec des documents locaux. Le système utilise des modèles de langage avancés pour fournir des réponses contextuelles et précises.

### Notre Assistant IA
Notre assistant IA est spécialement conçu pour :
- Simplifier l'accès aux informations de santé publique
- Répondre aux questions courantes sur les droits et démarches en santé
- Guider les utilisateurs dans leurs démarches administratives liées à la santé
- Fournir des informations fiables et à jour sur les dispositifs d'aide
- Aider à comprendre les procédures médicales et administratives

### Exemples de Questions Traitées
- Quels sont mes droits en matière de santé ?
- Comment accéder à la Complémentaire Santé Solidaire (CSS) ?
- Quelles sont les démarches pour obtenir une aide médicale ?
- Quelles sont les procédures pour un remboursement de soins ?


## ✨ Fonctionnalités
- Chargement et traitement de documents locaux (PDF, TXT, DOCX)
- Système de mémoire conversationnelle
- Base de données vectorielle pour la recherche sémantique
- Interface en ligne de commande interactive
- Support de différents modèles de langage (Ollama, DeepSeek)

## 🚀 Installation

### Installation des dépendances
```bash
# Cloner le repository
git clone [URL_DU_REPO]
cd Agent_IA

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement virtuel
# Sur Windows
venv\Scripts\activate
# Sur Linux/Mac
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

## 🛠️ Configuration

1. Créez un fichier `.env` à la racine du projet :
```env
# Configuration Ollama (par défaut)
OLLAMA_MODEL=llama3
OLLAMA_EMBEDDING_MODEL=nomic-embed-text

# Configuration DeepSeek (optionnel)
# DEEPSEEK_API_KEY=votre_clé_api
```

2. Structure des dossiers :
```
Agent_IA/
├── data/
│   ├── documents/    # Documents locaux
│   ├── db/          # Base de données vectorielle
│   └── memory/      # Stockage de la mémoire
├── tools/           # Outils et utilitaires
├── main_agent.py    # Agent principal
├── rag_chain.py     # Chaîne RAG
├── memory.py        # Gestion de la mémoire
└── requirements.txt # Dépendances
```

## 💻 Utilisation

### Lancer l'agent
```bash
python main_agent.py
```

### Modes de fonctionnement
- `local` : Utilise les documents locaux

### Commandes spéciales
- `exit` : Quitter l'application
- `reset` : Réinitialiser la mémoire conversationnelle

## 🔧 Architecture

Le projet est structuré en plusieurs composants principaux :

1. **MainAgent** : Gère l'interaction utilisateur et coordonne les autres composants
2. **RAGChain** : Gère le chargement et le traitement des documents
3. **Memory** : Gère la mémoire conversationnelle
4. **Vector Store** : Stocke et indexe les documents pour la recherche sémantique

## 📚 Documentation des Modèles

### Modèles supportés
- **Ollama** (par défaut)
  - Modèle de chat : llama3
  - Modèle d'embeddings : nomic-embed-text

- **DeepSeek** (optionnel)
  - Nécessite une clé API
  - Modèle de chat : deepseek-chat
  - Modèle d'embeddings : deepseek-embedding

## 🤝 Contribution
Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request


