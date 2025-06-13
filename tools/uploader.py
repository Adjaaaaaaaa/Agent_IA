from langchain_core.tools import Tool
from main_agent import model 
import os

def process_uploaded_file(file_content: str, action: str = "summarize") -> str:
    """Process uploaded file content and return AI response."""
    try:
        # Truncate content to avoid token limits
        max_chars = 3000
        if len(file_content) > max_chars:
            file_content = file_content[:max_chars] + "..."
        
        # Create prompt based on action
        if action == "summarize":
            prompt = f"""Fais un résumé structuré de ce document :

{file_content}

Utilise des emojis (📋🩺💊⚠️📅) pour structurer ta réponse."""
        else:
            prompt = f"""Analyse ce document et réponds aux questions qu'on pourrait te poser :

{file_content}"""
        
        # Call the model
        response = model.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        return f"Erreur lors du traitement du fichier : {str(e)}"

def answer_question_about_file(file_content: str, question: str) -> str:
    """Answer a specific question about uploaded file content."""
    try:
        # Truncate content to avoid token limits
        max_chars = 2500  # Leave room for question
        if len(file_content) > max_chars:
            file_content = file_content[:max_chars] + "..."
        
        prompt = f"""Réponds à cette question en te basant sur le contenu suivant :

CONTENU :
{file_content}

QUESTION : {question}

Réponds de manière claire et précise."""
        
        response = model.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
        
    except Exception as e:
        return f"Erreur lors de la réponse : {str(e)}"

# Tools for LangChain
upload_tool = Tool(
    name="process_file",
    description="Process uploaded file content and return summary or analysis",
    func=process_uploaded_file
)

question_tool = Tool(
    name="answer_file_question", 
    description="Answer questions about uploaded file content",
    func=answer_question_about_file
)