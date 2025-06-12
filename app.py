# app.py
import streamlit as st  # Importe la bibliothèque Streamlit pour créer l'interface web
from main_agent import get_chain_and_memory  # Importe la fonction pour obtenir la chaîne et la mémoire de l'agent
from io import StringIO  # Importe StringIO pour gérer les fichiers texte en mémoire
from memory import reset_memory  # Importe la fonction pour réinitialiser la mémoire
from main_agent import specific_tools # Import de la fonction d'outil specfique 

import PyPDF2  # Importe PyPDF2 pour lire les fichiers PDF

st.set_page_config(page_title="Agent IA Santé", layout="centered")  # Configure la page Streamlit

def extract_text_from_pdf(file) -> str:
    # Fonction pour extraire le texte d'un fichier PDF
    reader = PyPDF2.PdfReader(file)  # Crée un lecteur PDF
    text = ""  # Initialise une chaîne vide pour le texte
    for page in reader.pages:  # Parcourt chaque page du PDF
        text += page.extract_text() + "\n"  # Ajoute le texte de la page
    return text  # Retourne le texte extrait

def main():
    # Fonction principale de l'application

    if "chain" not in st.session_state:
        # Initialise la chaîne et la mémoire si elles n'existent pas dans la session
        chain, memory = get_chain_and_memory()
        st.session_state.chain = chain
        st.session_state.memory = memory

    if "history" not in st.session_state:
        # Initialise l'historique des questions/réponses
        st.session_state.history = []

    if "question" not in st.session_state:
        # Initialise la question courante
        st.session_state.question = ""

    if "language" not in st.session_state:
        # Initialise la langue par défaut
        st.session_state.language = "FR"

    lang_options = {"FR": "Français", "EN": "English"}  # Dictionnaire des langues disponibles
    selected_label = st.sidebar.radio("Choisis la langue / Choose language", list(lang_options.values()))  # Sélecteur de langue
    lang = list(lang_options.keys())[list(lang_options.values()).index(selected_label)]  # Récupère la clé de la langue sélectionnée
    st.session_state.language = lang  # Met à jour la langue dans la session

    # Dictionnaire des textes selon la langue
    texts = {
        "FR": {
            "title": "👨‍⚕️ Agent IA Santé",
            "chat_tab": "💬 Discuter avec l’IA",
            "upload_tab": "📎 Upload Document",
            "tool_label": "Outil de traitement",
            "input_label": "Pose ta question",
            "send_btn": "Envoyer",
            "empty_warning": "Merci d’entrer une question.",
            "processing": "Traitement en cours...",
            "history_title": "📜 Historique",
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
            "upload_tab": "📎 Upload Document",
            "tool_label": "Choose tool",
            "input_label": "Ask your question",
            "send_btn": "Send",
            "empty_warning": "Please enter a question.",
            "processing": "Processing...",
            "history_title": "📜 Conversation History",
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

    # Outils disponibles selon la langue
    tool_options = {
        "FR": ["Résumé", "Simplification", "Éligibilité CSS"],
        "EN": ["Summary", "Simplification", "CSS Eligibility"],
    }

    # Instructions pour chaque outil selon la langue
    tool_prompts = {
        "FR": {
            "Résumé": "Fais un résumé structuré avec emojis (📋🩺💊⚠️📅)",
            "Simplification": "Simplifie ce contenu médical en langage patient accessible",
            "Éligibilité CSS": "Analyse l'éligibilité CSS avec calcul détaillé des ressources"
        },
        "EN": {
            "Summary": "Make a structured summary with emojis (📋🩺💊⚠️📅",
            "Simplification": "Simplify this medical content in accessible patient language",
            "CSS Eligibility": "Analyze CSS eligibility with detailed resource calculation"
        }
    }

    t = texts[lang]  # Récupère les textes pour la langue sélectionnée
    st.title(t["title"])  # Affiche le titre de la page
    tab_chat, tab_upload = st.tabs([t["chat_tab"], t["upload_tab"]])  # Crée deux onglets : chat et upload

# Onglet Chat
    with tab_chat:
        outil_labels = tool_options[lang]  # Liste des outils selon la langue
        outil = st.selectbox(t["tool_label"], outil_labels)  # Sélecteur d'outil
        question = st.text_input(t["input_label"], value=st.session_state.question, key="input_question")  # Champ de saisie de la question

        # Si l'utilisateur clique sur le bouton d'envoi
        if st.button(t["send_btn"], key="send_button"):
            if not question.strip():
                # Affiche un avertissement si la question est vide
                st.warning(t["empty_warning"])
            else:
                # Affiche un spinner pendant le traitement
                with st.spinner(t["processing"]):
                    try:
                        # Essaie d'abord l'outil spécialisé
                        reponse_outil = specific_tools(question, outil, lang)

                        if reponse_outil:
                            # Utilise la réponse de l'outil spécialisé
                            answer = reponse_outil
                        else:
                            # Utilise la méthode originale en cas d'échec
                            lang_label = lang_options[lang]  # Récupère le label de la langue

                            # Génère le prompt selon l'outil sélectionné et la langue
                            if outil in ["Résumé", "Summary"]:
                                if lang == "FR":
                                    prompt = f"""Tu es un assistant médical intelligent. Résume clairement et utilement le sujet suivant pour un patient non spécialiste :
"{question}"
- Ne fais pas de liste à puces.
- Utilise un ton informatif et fluide.
- Reformule avec tes propres mots.
Réponds uniquement en {lang_label}."""
                                else:
                                    prompt = f"""You are a smart medical assistant. Provide a clear and useful summary of the following topic for a non-expert patient:
"{question}"
- Avoid bullet points.
- Use an informative and natural tone.
- Rephrase in your own words.
Reply only in {lang_label}."""

                            elif outil in ["Simplification"]:
                                if lang == "FR":
                                    prompt = f"""Simplifie le contenu suivant pour qu'il soit compréhensible par un patient sans connaissances médicales :
"{question}"
- Utilise des phrases courtes, un vocabulaire simple.
- Garde un ton bienveillant.
Réponds uniquement en {lang_label}."""
                                else:
                                    prompt = f"""Simplify the following content so that any patient without medical knowledge can understand:
"{question}"
- Use short sentences and simple vocabulary.
- Keep a helpful tone.
Reply only in {lang_label}."""

                            elif outil in ["Éligibilité CSS", "CSS Eligibility"]:
                                if lang == "FR":
                                    prompt = f"""Évalue si la personne décrite dans ce texte est éligible à la Complémentaire Santé Solidaire (CSS).
"{question}"
Réponds uniquement en {lang_label}, de façon claire et concise."""
                                else:
                                    prompt = f"""Assess whether the person described in the following text is eligible for the French CSS (Complémentaire Santé Solidaire) health support.
"{question}"
Reply only in {lang_label}, clearly and briefly."""

                            else:
                                # Cas générique pour d'autres outils
                                instruction = tool_prompts[lang][outil]
                                prompt = f"{instruction} : {question}\nRéponds uniquement en {lang_label}."

                            # Appelle l'agent IA
                            result = st.session_state.chain.invoke({"question": prompt})
                            answer = result.get("answer", "Pas de réponse.")  # Récupère la réponse

                    except Exception as e:
                        answer = f"❌ Erreur : {e}"  # Affiche l'erreur en cas d'échec

                    st.session_state.history.append({"question": question, "answer": answer})  # Ajoute à l'historique
                    st.session_state.question = ""  # Réinitialise la question
                st.rerun()  # Recharge la page pour afficher la nouvelle réponse

        # Affichage de l'historique des échanges
        if st.session_state.history:
            st.markdown("---")
            st.header(t["history_title"])
            for qa in st.session_state.history:
                st.markdown(f"""
                    <div style="text-align: left; margin: 10px;">
                        <div style="background-color: #daf1ff; color: #034078; padding: 10px 15px; border-radius: 15px 15px 0 15px; max-width: 70%;">
                            <b>{'Vous' if lang=='FR' else 'You'}:</b> {qa['question']}
                        </div>
                    </div>
                    <div style="text-align: left; margin: 10px;">
                        <div style="background-color: #f1f1f1; color: #333; padding: 10px 15px; border-radius: 15px 15px 15px 0; max-width: 70%;">
                            <b>{'Agent IA' if lang=='FR' else 'AI Assistant'}:</b> {qa['answer']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # Bouton pour réinitialiser la mémoire et l'historique
        if st.button(t["reset_btn"]):
            reset_memory(st.session_state.memory)  # Réinitialise la mémoire de l'agent
            st.session_state.history = []  # Vide l'historique
            st.session_state.question = ""  # Vide la question
            st.success(t["reset_success"])  # Affiche un message de succès

    # Onglet Upload de document
    with tab_upload:
        st.write(t["upload_label"])  # Affiche le label d'upload
        uploaded_file = st.file_uploader("", type=["pdf", "txt"])  # Champ d'upload de fichier

        if uploaded_file is not None:
            # Si un fichier est uploadé
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)  # Extrait le texte du PDF
            else:
                stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))  # Lit le fichier texte
                text = stringio.read()

            st.text_area("Contenu extrait", value=text, height=200)  # Affiche le texte extrait
            action = st.selectbox(t["action_label"], [t["summary_option"], t["question_option"]])  # Sélecteur d'action

            prompt = ""  # Initialise le prompt
            lang_instr = "Réponds uniquement en Français." if lang == "FR" else "Answer only in English."  # Instruction de langue

            if action == t["summary_option"]:
                # Si l'utilisateur veut un résumé
                prompt = f"{tool_prompts[lang][action]} : {text}\n{lang_instr}"
            else:
                # Si l'utilisateur veut poser une question sur le contenu
                question_file = st.text_input(t["question_file_label"])
                if question_file:
                    instruction = tool_prompts[lang][action]
                    prompt = f"{instruction} : {text}\n{t['question_file_label']} {question_file}\n{lang_instr}"

            # Si un prompt est prêt et que l'utilisateur clique sur le bouton
            if prompt and st.button(t["send_request_btn"]):
                with st.spinner(t["processing"]):
                    result = st.session_state.chain.invoke({"question": prompt})  # Appelle l'agent IA
                    answer = result.get("answer", "Pas de réponse.")  # Récupère la réponse
                    st.write(f"**{t['response_label']}** {answer}")  # Affiche la réponse

if __name__ == "__main__":
    main()  # Lance l'application si le fichier est exécuté directement