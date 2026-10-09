import streamlit as st
from groq import Groq
import datetime
from fpdf import FPDF
import tempfile

# --- CONFIGURATION ---
MOT_DE_PASSE = "Crossway2026"

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
        # Récupération sécurisée de la clé depuis le coffre-fort Streamlit
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        st.error("Clé API introuvable. Vérifiez les secrets de Streamlit.")
        st.stop()
    
    SYSTEM_PROMPT = """Tu es un formateur expert pour le Titre Pro Conducteur de Transport en Commun sur Route (CTCR), le Permis D et la FIMO Voyageurs, basé sur le référentiel AFTRAL 2026.
Ton rôle est d'interroger l'élève sur :
1. Le Socle 1 (vérifications courantes de sécurité) et le Socle 2 (freins, maniabilité).
2. Les fiches orales (les 6 fiches thématiques de l'autocar).
3. Le programme de la FIMO Voyageurs (réglementation sociale européenne, temps de conduite/repos, sécurité, accueil des passagers).
Pédagogie : Pose une question claire, attends la réponse, puis valide ou corrige avec bienveillance. Ne donne pas de longues listes indigestes. Concentre-toi sur la sécurité, la réglementation en vigueur et les mots-clés essentiels. Les utilisateurs révisent sur leur smartphone, sois concis."""

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # --- ZONE DE SAISIE EN HAUT (Idéal pour smartphone) ---
    st.markdown("---")
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Pose ta question ou demande à être interrogé :", placeholder="Ex: Pose-moi une question sur le thème 3...")
        submit_button = st.form_submit_button("Envoyer au formateur 🚀")

    if submit_button and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Le formateur réfléchit..."):
            try:
                # Nouveau modèle Llama 3 actif et fonctionnel
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=st.session_state.messages
                )
                reponse_texte = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reponse_texte})
            except Exception as e:
                st.error(f"Erreur de communication avec l'API Groq: {e}")
        
        # Recharge l'interface pour afficher la réponse immédiatement
        st.rerun()

    # --- AFFICHAGE DE L'HISTORIQUE (Du plus récent au plus ancien) ---
    st.markdown("### Historique de la session")
    
    # On filtre pour ne pas afficher les instructions secrètes (system prompt)
    messages_a_afficher = [msg for msg in st.session_state.messages if msg["role"] != "system"]
    
    # On inverse la liste pour avoir le message le plus récent juste sous le formulaire d'envoi
    for msg in reversed(messages_a_afficher):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Bouton d'export PDF toujours accessible en bas
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
