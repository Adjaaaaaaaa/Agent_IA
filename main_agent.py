import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_deepseek import ChatDeepSeek 
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import HuggingFaceEmbeddings
from rag_chain import load_documents, split_documents, create_or_load_vectordb
from memory import get_memory
import logging

# Réduire le niveau des logs pour éviter trop de verbosité
logging.getLogger("langchain").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logging.getLogger("transformers").setLevel(logging.ERROR)

# Charger les variables d'environnement du fichier .env (avec override pour forcer)
load_dotenv(override=True)

# Configuration du modèle de langage (LLM) et du modèle d'embeddings

# Configuration DeepSeek
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

if deepseek_api_key:
    # Utiliser DeepSeek pour le LLM seulement
    model = ChatDeepSeek(
        model="deepseek-chat", 
        api_key=deepseek_api_key,
        temperature=0
    )
    # Garder Ollama pour les embeddings
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    print("✅ DeepSeek configuré pour LLM + Ollama pour embeddings")
else:
    # Fallback vers Ollama si pas de clé DeepSeek
    model = ChatOllama(model="llama3", temperature=0)
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    print("⚠️ Pas de clé DeepSeek, utilisation d'Ollama")

def reset_memory(memory):
    """
    Fonction pour réinitialiser la mémoire conversationnelle.
    """
    memory.clear()
    print("🧹 Mémoire réinitialisée.")

def get_chain_and_memory():
    """
    Charge les documents, les segmente, charge/crée une base vectorielle,
    crée un retriever, récupère la mémoire conversationnelle et 
    assemble la chaîne de question-réponse conversationnelle.
    
    Retourne la chaîne (chain) et la mémoire (memory).
    """
    current_dir = os.getcwd()  # Dossier courant du projet
    db_dir = os.path.join(current_dir, "data", "db")  # Répertoire pour stocker la base vectorielle persistante

    # Chargement des documents sources (depuis rag_chain.py)
    docs = load_documents()

    # Découpage des documents en chunks plus petits pour la recherche vectorielle
    chunks = split_documents(docs)

    # Créer ou charger la base vectorielle persistante (ex: FAISS, Chroma, etc.)
    vectordb = create_or_load_vectordb(chunks, persist_directory=db_dir)

    # Création d'un retriever (pour récupérer les passages pertinents)
    retriever = vectordb.as_retriever()

    # Récupération de la mémoire conversationnelle (buffer)
    memory = get_memory(llm_model=model)

    # Création de la chaîne conversationnelle avec LLM + retriever + mémoire
    chain = ConversationalRetrievalChain.from_llm(
        llm=model,
        retriever=retriever,
        memory=memory,
        return_source_documents=True  # Pour obtenir les docs sources (utile pour debug/tracing)
    )

    return chain, memory

def interactive_loop(chain, memory):
    """
    Boucle interactive en console pour poser des questions et afficher les réponses.
    Gestion des commandes spéciales :
     - 'exit' : quitte la boucle
     - 'reset': réinitialise la mémoire
    """
    print("💬 Pose ta question (tape 'exit' pour quitter, 'reset' pour réinitialiser la mémoire)")

    while True:
        query = input("➡️  ")
        if query.lower() == "exit":
            print("👋 Au revoir !")
            break
        elif query.lower() == "reset":
            memory.clear()
            print("🧹 Mémoire réinitialisée.")
            continue

        # ⚠️ Bloc de protection contre les erreurs pendant l'appel à la chaîne
        try:
            result = chain.invoke({"question": query})
            answer = result.get("answer", "Pas de réponse.")
            print(f"🤖 Réponse : {answer}\n")
        except Exception as e:
            print(f"❌ Erreur lors du traitement de la requête : {e}")
            continue

def specific_tools(question, choosen_tool, langue="FR"):
    """
    Fonction pour traiter avec l'outil spécialisé choisi
    """
    # Prompts optimisés pour DeepSeek
    if choosen_tool in ["Résumé", "Summary"]:
        prompt = f"""Résume ce document médical avec cette structure :
📋 DIAGNOSTIC PRINCIPAL
🩺 EXAMENS CLÉS  
💊 TRAITEMENTS
⚠️ POINTS ATTENTION
📅 SUIVI

Document: {question}"""
        
    elif choosen_tool in ["Simplification"]:
        prompt = f"""Simplifie ce texte médical pour un patient :
- Remplace les mots compliqués
- Explique avec "vous" et "votre"
- Phrases courtes et claires

Texte: {question}"""
        
    elif choosen_tool in ["Éligibilité CSS"]:
        prompt = f"""Analyse l'éligibilité CSS avec les plafonds 2024 :
1 pers: 847€, 2 pers: 1271€, 3 pers: 1525€, 4 pers: 1779€

Situation: {question}

Donne: composition foyer, calcul ressources, décision éligibilité"""
    else:
        return None
    
    # Appel du modèle (DeepSeek ou Ollama selon config)
    try:
        response = model.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        print(f"❌ Erreur dans specific_tools : {e}")
        return None

def test_deepseek():
    """Test rapide de DeepSeek"""
    if deepseek_api_key:
        try:
            response = model.invoke("Bonjour, peux-tu me confirmer que tu es DeepSeek ?")
            print(f"🤖 Test DeepSeek : {response.content[:100]}...")
            return True
        except Exception as e:
            print(f"❌ Erreur test DeepSeek : {e}")
            return False
    return False

if __name__ == "__main__":
    # Test du modèle configuré
    if deepseek_api_key:
        print("🧪 Test de DeepSeek...")
        test_deepseek()
    
    # Chargement de la chaîne et mémoire au lancement du script
    chain, memory = get_chain_and_memory()

    # Démarrage de la boucle interactive console
    interactive_loop(chain, memory)