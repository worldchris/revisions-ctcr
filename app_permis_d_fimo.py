import streamlit as st
from groq import Groq
import datetime
from fpdf import FPDF
import tempfile

# --- CONFIGURATION ---
MOT_DE_PASSE = "Crossway2026"

st.set_page_config(page_title="Révisions Permis D & FIMO", page_icon="🚌", layout="centered")

def check_password():
    if "pwd_correct" not in st.session_state:
        st.session_state["pwd_correct"] = False
    if not st.session_state["pwd_correct"]:
        st.warning("🔒 Accès Réservé - Groupe de Révision AFTRAL")
        pwd = st.text_input("Mot de passe", type="password")
        if st.button("Valider"):
            if pwd == MOT_DE_PASSE:
                st.session_state["pwd_correct"] = True
                st.rerun()
            else:
                st.error("Mot de passe incorrect")
        return False
    return True

def create_pdf(messages):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, txt="Session de Revision - Titre Pro CTCR & FIMO", ln=True, align='C')
    pdf.ln(5)
    
    # Ajout de la mention de prévention dans le PDF
    pdf.set_font("Arial", 'I', size=9)
    pdf.multi_cell(0, 6, txt="Avertissement : Cet outil utilise l'intelligence artificielle. Il appartient a l'utilisateur de verifier systematiquement l'exactitude des informations fournies avec le referentiel officiel AFTRAL.")
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    for msg in messages:
        if msg["role"] == "system": continue
        role = "Eleve" if msg["role"] == "user" else "Formateur IA"
        
        texte = f"{role}: {msg['content']}".encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 8, txt=texte)
        pdf.ln(4)
        
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

if check_password():
    st.title("🚌 Formateur IA - Permis D & FIMO")
    st.markdown("**Titre Pro CTCR Voyageurs - Référentiel AFTRAL 2026**")
    
    # Mention importante affichée sur l'interface
    st.warning("⚠️ **Important :** Cet outil est un assistant basé sur l'IA. Il vous appartient de vérifier systématiquement les réponses fournies avec vos cours et le référentiel officiel AFTRAL.")
    
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    except Exception as e:
        st.error("Clé API introuvable. Vérifiez les secrets de Streamlit.")
        st.stop()
        
    if "messages" not in st.session_state:
        SYSTEM_PROMPT = """Tu es un formateur expert pour le Titre Pro Conducteur de Transport en Commun sur Route (CTCR), le Permis D et la FIMO Voyageurs, basé sur le référentiel AFTRAL 2026.
Ton rôle est d'interroger l'élève sur :
1. Le Socle 1 et Socle 2 (freins, maniabilité).
2. Les fiches orales de l'autocar.
3. La FIMO Voyageurs.
Pédagogie : Pose une question claire, attends la réponse, puis valide ou corrige avec bienveillance. Ne donne pas de longues listes indigestes. Concentre-toi sur la sécurité et les mots-clés essentiels. Les utilisateurs révisent sur leur smartphone, sois concis."""
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    def envoyer_message():
        texte = st.session_state.champ_saisie
        if texte.strip() != "":
            st.session_state.messages.append({"role": "user", "content": texte})
            st.session_state.champ_saisie = ""
            st.session_state.requete_en_attente = True

    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input("Poser une question :", key="champ_saisie", label_visibility="collapsed", placeholder="Pose ta question ou demande un thème...", on_change=envoyer_message)
    with col2:
        st.button("Envoyer", on_click=envoyer_message, use_container_width=True)

    if st.session_state.get("requete_en_attente", False):
        with st.spinner("Le formateur rédige sa réponse..."):
            try:
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                # Utilisation du modèle Llama 3.1 actuellement supporté et stable par Groq
                response = client.chat.completions.create(
                    model="llama3-8b-8192",",
                    messages=api_messages
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Erreur de communication avec l'API Groq : {e}")
        
        st.session_state.requete_en_attente = False

    st.markdown("### Historique de la session")
    messages_utiles = [m for m in st.session_state.messages if m["role"] != "system"]
    
    for msg in reversed(messages_utiles):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

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
