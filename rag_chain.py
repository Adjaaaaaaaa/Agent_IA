import os
import requests
from dotenv import load_dotenv

# Embeddings
from langchain_ollama import OllamaEmbeddings
# from langchain_deepseek import DeepSeekEmbeddings  # Option DeepSeek, décommenter si nécessaire


# Loaders
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader, UnstructuredWordDocumentLoader
from langchain.schema import Document

from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vector store
from langchain_community.vectorstores import Chroma

load_dotenv(override=True)

# ==== Embeddings par défaut ====
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

# ==== Alternative DeepSeek ====
# Pour utiliser DeepSeek, décommentez la ligne suivante et commentez la ligne Ollama ci-dessus :
# embedding_model = DeepSeekEmbeddings(api_key=os.getenv("DEEPSEEK_API_KEY"), model="deepseek-embedding")

def load_documents(path="./data/documents"):
    """Charge tous les documents pris en charge dans un dossier."""
    loaders = [
        DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader),
        DirectoryLoader(path, glob="*.txt", loader_cls=TextLoader),
        DirectoryLoader(path, glob="*.docx", loader_cls=UnstructuredWordDocumentLoader)
    ]
    
    documents = []
    for loader in loaders:
        docs = loader.load()
        documents.extend(docs)

    print(f"✅ {len(documents)} documents chargés depuis {path}")
    return documents


# def load_from_open_api(url):
#     """Charge un document depuis une API ouverte (GET)"""
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         content = response.text
#         print(f"🌐 Données chargées depuis l'API : {url}")
#         return [Document(page_content=content)]
#     except Exception as e:
#         print(f"❌ Échec du chargement depuis {url}: {e}")
#         return []


def split_documents(documents, chunk_size=500, chunk_overlap=50):
    """Découpe les documents en chunks"""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    print(f"✅ Documents découpés en {len(chunks)} chunks")
    return chunks




def create_or_load_vectordb(chunks, persist_directory, embedding_model=None):
    """Crée ou charge une base vectorielle persistante"""
    if embedding_model is None:
        # Modèle par défaut : OllamaEmbeddings
        embedding_model = OllamaEmbeddings(model="nomic-embed-text")

        # Option DeepSeek (décommenter pour utiliser)
        # embedding_model = DeepSeekEmbeddings()

    if not os.path.exists(persist_directory) or len(os.listdir(persist_directory)) == 0:
        print("🛠️ Création de la base vectorielle...")
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embedding_model,
            persist_directory=persist_directory
        )
        vectordb.persist()
        print("✅ Base vectorielle créée et sauvegardée.")
    else:
        print("📂 Base vectorielle existante détectée. Chargement...")
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding_model
        )
    return vectordb
