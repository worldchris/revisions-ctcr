import streamlit as st
from groq import Groq
import datetime
from fpdf import FPDF
import tempfile

# --- CONFIGURATION ---
MOT_DE_PASSE = "Crossway2026"
# Remplace par ta vraie clé API Groq
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# --- PAGE CONFIGURATION (Mobile Friendly) ---
st.set_page_config(
    page_title="Révisions Permis D & FIMO", 
    page_icon="🚌", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# --- SYSTÈME DE MOT DE PASSE ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        st.markdown("### 🔒 Accès Réservé - Groupe de Révision AFTRAL")
        st.markdown("Connectez-vous pour réviser le Titre Pro Voyageurs et la FIMO.")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Valider"):
            if pwd == MOT_DE_PASSE:
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect.")
        return False
    return True

# --- GÉNÉRATION DU PDF ---
def create_pdf(messages):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="Session de Revision - Titre Pro CTCR & FIMO", ln=True, align='C')
    pdf.ln(10)
    
    for msg in messages:
        if msg["role"] == "system": continue
        role = "Eleve" if msg["role"] == "user" else "Formateur IA"
        
        # Nettoyage des accents pour le PDF basique
        texte = f"{role}: {msg['content']}".encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=texte)
        pdf.ln(4)
        
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --- APPLICATION PRINCIPALE ---
if check_password():
    st.title("🚌 Formateur IA - Permis D & FIMO")
    st.markdown("**Titre Pro CTCR Voyageurs - Référentiel AFTRAL 2026**")
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.error("Veuillez configurer la clé API Groq dans le script.")
    
    SYSTEM_PROMPT = """Tu es un formateur expert pour le Titre Pro Conducteur de Transport en Commun sur Route (CTCR), le Permis D et la FIMO Voyageurs, basé sur le référentiel AFTRAL 2026.
Ton rôle est d'interroger l'élève sur :
1. Le Socle 1 (vérifications courantes de sécurité) et le Socle 2 (freins, maniabilité).
2. Les fiches orales (les 6 fiches thématiques de l'autocar).
3. Le programme de la FIMO Voyageurs (réglementation sociale européenne, temps de conduite/repos, sécurité, accueil des passagers).
Pédagogie : Pose une question claire, attends la réponse, puis valide ou corrige avec bienveillance. Ne donne pas de longues listes indigestes. Concentre-toi sur la sécurité, la réglementation en vigueur et les mots-clés essentiels. Les utilisateurs révisent sur leur smartphone, sois concis."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ex: Pose-moi une question sur les temps de conduite FIMO..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                # Appel API Groq avec le modèle Mixtral
                response = client.chat.completions.create(
                    model="mixtral-8x7b-32768",
                    messages=st.session_state.messages
                )
                reponse_texte = response.choices[0].message.content
                message_placeholder.markdown(reponse_texte)
                st.session_state.messages.append({"role": "assistant", "content": reponse_texte})
            except Exception as e:
                st.error(f"Erreur de communication avec l'API Groq: {e}")

    st.markdown("---")
    if len(st.session_state.messages) > 1:
        pdf_path = create_pdf(st.session_state.messages)
        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="📥 Télécharger la session en PDF",
                data=pdf_file,
                file_name=f"Revisions_PermisD_FIMO_{datetime.date.today()}.pdf",
                mime="application/pdf"
            )