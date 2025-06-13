"""
AI Health Agent - Streamlit Application

This web application provides a user-friendly interface to interact with a health-specialized AI assistant.
Users can chat with the AI, upload medical documents (PDF or TXT), and request summaries, simplifications, or eligibility analyses.

Main Features:
- AI-powered chatbot with conversational memory
- PDF/TXT file upload and content processing
- Multi-language support (French/English)
- Selectable tools: summarization, simplification, eligibility analysis
- Persistent conversation history with reset option


To run:
    streamlit run your_script_name.py
"""
import streamlit as st
from main_agent import get_chain_and_memory, specific_tools
from io import StringIO
from memory import reset_memory
import PyPDF2

st.set_page_config(page_title="Agent IA Santé", layout="wide")

def extract_text_from_pdf(file) -> str:
    """
    Extracts and returns the text content from a PDF file.

    Args:
        file: A file-like object or path to the PDF file to extract text from.

    Returns:
        str: The extracted text from all pages of the PDF, separated by newlines.

    Raises:
        PyPDF2.errors.PdfReadError: If the file is not a valid PDF or cannot be read.
    """
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def truncate_text(text, max_chars=3000):
    """Tronque le texte pour éviter de dépasser la limite"""
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text

def main():
    """
    Main entry point for the Streamlit AI Health Agent application.
    Initializes session state variables, manages language selection, and sets up the user interface with two main tabs:
    - Chat tab: Allows users to interact with the AI agent using natural language questions, supporting multiple tools (summary, simplification, eligibility).
    - Upload tab: Enables users to upload PDF or TXT documents, extract content, and either summarize or ask questions about the uploaded content.
    Handles conversation history, memory reset, dynamic UI labels based on selected language (French/English), and error handling for AI responses.
    """

    if "chain" not in st.session_state:
        chain, memory = get_chain_and_memory()
        st.session_state.chain = chain
        st.session_state.memory = memory

    if "history" not in st.session_state:
        st.session_state.history = []

    if "language" not in st.session_state:
        st.session_state.language = "FR"

    lang_options = {"FR": "Français", "EN": "English"}
    selected_label = st.sidebar.radio("Choisis la langue / Choose language", list(lang_options.values()))
    lang = list(lang_options.keys())[list(lang_options.values()).index(selected_label)]
    st.session_state.language = lang

    texts = {
        "FR": {
            "title": "👨‍⚕️ Agent IA Santé",
            "chat_tab": "💬 Discuter avec l’IA",
            "upload_tab": "📌 Upload Document",
            "tool_label": "Outil de traitement",
            "input_label": "Pose ta question",
            "send_btn": "Envoyer",
            "empty_warning": "Merci d’entrer une question.",
            "processing": "Traitement en cours...",
            "history_title": "Historique de conversation",
            "reset_btn": "Réinitialiser",
            "reset_success": "La mémoire a été effacée.",
            "upload_label": "Uploade un document (PDF ou TXT)",
            "action_label": "Que veux-tu faire ?",
            "summary_option": "Faire un résumé",
            "question_option": "Poser une question",
            "question_file_label": "Question à poser sur le contenu :",
            "send_request_btn": "Envoyer la requête",
            "response_label": "Réponse :"
        },
        "EN": {
            "title": "👨‍⚕️ AI Health Agent",
            "chat_tab": "💬 Talk with AI",
            "upload_tab": "📌 Upload Document",
            "tool_label": "Choose tool",
            "input_label": "Ask your question",
            "send_btn": "Send",
            "empty_warning": "Please enter a question.",
            "processing": "Processing...",
            "history_title": "Conversation History",
            "reset_btn": "Reset",
            "reset_success": "Memory cleared.",
            "upload_label": "Upload a document (PDF or TXT)",
            "action_label": "What do you want to do?",
            "summary_option": "Summarize",
            "question_option": "Ask a question",
            "question_file_label": "Question about the content:",
            "send_request_btn": "Submit request",
            "response_label": "Response:"
        }
    }

    tool_options = {
        "FR": ["Résumé", "Simplification", "Éligibilité"],
        "EN": ["Summary", "Simplification", "Eligibility"]
    }

    tool_prompts = {
        "FR": {
            "Résumé": "Fais un résumé structuré avec emojis (📋🧪💊⚠️📅)",
            "Simplification": "Simplifie ce contenu médical en langage patient accessible",
            "Éligibilité": "Analyse l'éligibilité CSS avec calcul détaillé des ressources",
            "Faire un résumé": "Fais un résumé structuré avec emojis (📋🧪💊⚠️📅)",
            "Poser une question": "Réponds à cette question sur le contenu"
        },
        "EN": {
            "Summary": "Make a structured summary with emojis (📋🧪💊⚠️📅)",
            "Simplification": "Simplify this medical content in accessible patient language",
            "Eligibility": "Analyze CSS eligibility with detailed resource calculation",
            "Summarize": "Make a structured summary with emojis (📋🧪💊⚠️ 📅)",
            "Ask a question": "Answer this question about the content"
        }
    }

    t = texts[lang]
    st.title(t["title"])

    # Sidebar with dynamic labels
    selected_tool = st.sidebar.selectbox(f"🛠️ {t['tool_label']}", tool_options[lang])

    if st.sidebar.button(f"🗑️ {t['history_title']}"):
        reset_memory(st.session_state.memory)
        if "history" in st.session_state:
            del st.session_state["history"]
        st.sidebar.success(t["reset_success"])
        st.rerun()

    tab_chat, tab_upload = st.tabs([t["chat_tab"], t["upload_tab"]])

    with tab_chat:
        st.markdown("""
        <style>
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background: white;
            padding: 10px 20px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
            z-index: 999;
        }
        .chat-bubble.user {
            background-color: #cce5ff;
            color: #003366;
            text-align: right;
            border-radius: 15px 15px 0 15px;
            padding: 10px 15px;
            max-width: 70%;
            margin-left: auto;
            margin-right: 10px;
            margin-bottom: 25px;
        }
        .chat-bubble.bot {
            background-color: #f1f1f1;
            color: #333;
            text-align: left;
            border-radius: 15px 15px 15px 0;
            padding: 10px 15px;
            max-width: 70%;
            margin-right: auto;
            margin-left: 10px;
            margin-bottom: 25px;
        }
        </style>
        <div style='margin-bottom: 100px'></div>
        """, unsafe_allow_html=True)

        for qa in st.session_state.history:
            st.markdown(f'<div class="chat-bubble user"><b>Vous:</b> {qa["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-bubble bot"><b>IA:</b> {qa["answer"]}</div>', unsafe_allow_html=True)

        with st.form("chat_form", clear_on_submit=True):
            st.markdown('<div class="input-container">', unsafe_allow_html=True)
            question = st.text_input(t["input_label"], key="chat_input", label_visibility="collapsed", placeholder=t["input_label"])
            submitted = st.form_submit_button(t["send_btn"])
            st.markdown('</div>', unsafe_allow_html=True)

            if submitted:
                if not question.strip():
                    st.warning(t["empty_warning"])
                else:
                    with st.spinner(t["processing"]):
                        try:
                            answer = specific_tools(question, selected_tool, lang) or \
                                     st.session_state.chain.invoke({"question": question}).get("answer", "Pas de réponse.")
                        except Exception as e:
                            answer = f"Erreur: {e}"
                        st.session_state.history.append({"question": question, "answer": answer})
                        st.rerun()

    with tab_upload:
        st.write(t["upload_label"])
        uploaded_file = st.file_uploader("Choisir un fichier", type=["pdf", "txt"], label_visibility="collapsed")

        if uploaded_file is not None:
            try:
                # Extraction du texte selon le type de fichier
                if uploaded_file.type == "application/pdf":
                    extracted_text = extract_text_from_pdf(uploaded_file)
                else:
                    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
                    extracted_text = stringio.read()

                # Affichage du contenu extrait (aperçu)
                display_text = extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
                st.text_area("Aperçu du contenu extrait", value=display_text, height=150, disabled=True)
                
                # Sélection de l'action
                action = st.selectbox(t["action_label"], [t["summary_option"], t["question_option"]])
                
                # Interface selon l'action choisie
                if action == t["summary_option"]:
                    st.write("📋 Génération d'un résumé structuré du document...")
                    
                    if st.button(t["send_request_btn"], key="summary_btn"):
                        with st.spinner(t["processing"]):
                            try:
                                # Tronquer le texte pour éviter les erreurs de tokens
                                truncated_text = extracted_text[:3000] + "..." if len(extracted_text) > 3000 else extracted_text
                                
                                prompt = f"""Fais un résumé structuré de ce document médical avec des emojis (📋🩺💊⚠️📅) :

{truncated_text}

Réponds en {'Français' if lang == 'FR' else 'English'}."""
                                
                                result = st.session_state.chain.invoke({"question": prompt})
                                answer = result.get("answer", "Pas de réponse.")
                                
                                st.success("✅ Résumé généré avec succès !")
                                st.markdown(f"**{t['response_label']}**")
                                st.markdown(answer)
                            except Exception as e:
                                st.error(f"❌ Erreur lors de la génération du résumé : {e}")
                
                else:  # Question sur le document
                    st.write("❓ Posez une question sur le contenu du document...")
                    file_question = st.text_input(
                        t["question_file_label"], 
                        placeholder="Ex: Quels sont les symptômes mentionnés ?"
                    )
                    
                    if file_question and st.button(t["send_request_btn"], key="question_btn"):
                        with st.spinner(t["processing"]):
                            try:
                                # Tronquer le texte pour laisser de la place à la question
                                truncated_text = extracted_text[:2500] + "..." if len(extracted_text) > 2500 else extracted_text
                                
                                prompt = f"""En tant qu'assistant médical, réponds à cette question en te basant sur le contenu suivant :

CONTENU DU DOCUMENT :
{truncated_text}

QUESTION : {file_question}

Réponds de manière claire et précise en {'Français' if lang == 'FR' else 'English'}."""
                                
                                result = st.session_state.chain.invoke({"question": prompt})
                                answer = result.get("answer", "Pas de réponse.")
                                
                                st.success("✅ Réponse générée avec succès !")
                                st.markdown(f"**Question :** {file_question}")
                                st.markdown(f"**{t['response_label']}**")
                                st.markdown(answer)
                            except Exception as e:
                                st.error(f"❌ Erreur lors de la réponse : {e}")
                        
            except Exception as e:
                st.error(f"❌ Erreur lors de la lecture du fichier : {e}")
                st.info("💡 Assurez-vous que le fichier est un PDF valide ou un fichier texte UTF-8.")

if __name__ == "__main__":
    main()
