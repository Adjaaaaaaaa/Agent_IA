import os
from langchain.memory import ConversationSummaryBufferMemory
from langchain_ollama import ChatOllama

MEMORY_PERSIST_DIR = os.path.join(os.getcwd(), "data", "memory")
# Choisissez votre modèle ici :
# model_name = "llama3"  # ✅ modèle par défaut
# model_name = "deepseek-coder"  # 🔄 pour utiliser DeepSeek (décommentez cette ligne)
model_name = "llama3"  # <-- Changez ici pour basculer facilement
llm_for_summary = ChatOllama(model=model_name, temperature=0)

def get_memory():
    if not os.path.exists(MEMORY_PERSIST_DIR):
        os.makedirs(MEMORY_PERSIST_DIR)
    memory = ConversationSummaryBufferMemory(
        llm=llm_for_summary,
        max_token_limit=1000,
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
