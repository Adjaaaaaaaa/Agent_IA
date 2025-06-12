import os
from langchain.memory import ConversationBufferMemory

from langchain_ollama import ChatOllama

MEMORY_PERSIST_DIR = os.path.join(os.getcwd(), "data", "memory")

# mémoire selon le modèle utilisé deepseek ou ollama

def get_memory(llm_model=None):
    """
    Crée la mémoire conversationnelle avec le même LLM que l'agent principal
    
    Args:
        llm_model: Le LLM à utiliser (DeepSeek ou Ollama selon config)
    """
    if not os.path.exists(MEMORY_PERSIST_DIR):
        os.makedirs(MEMORY_PERSIST_DIR)
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer",
    )
    return memory

def reset_memory(memory):
    """Réinitialise la mémoire conversationnelle."""
    if hasattr(memory, 'clear'):
        memory.clear()
    else:
        # Si clear() n'existe pas, on peut réinitialiser manuellement
        if hasattr(memory, 'chat_memory'):
            memory.chat_memory.clear()
