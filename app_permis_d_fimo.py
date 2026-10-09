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
    pdf.ln(10)
    
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

    # --- NOUVELLE GESTION DU CHAMP DE SAISIE (Callbacks) ---
    def envoyer_message():
        texte = st.session_state.champ_saisie
        # Si le texte n'est pas vide
        if texte.strip() != "":
            # 1. On sauvegarde la question de l'élève
            st.session_state.messages.append({"role": "user", "content": texte})
            # 2. On vide instantanément le champ de saisie
            st.session_state.champ_saisie = ""
            # 3. On active un signal pour appeler l'IA
            st.session_state.requete_en_attente = True

    st.markdown("---")
    
    # Interface avec le champ de texte et le bouton alignés
    col1, col2 = st.columns([4, 1])
    with col1:
        st.text_input("Poser une question :", key="champ_saisie", label_visibility="collapsed", placeholder="Pose ta question ou demande un thème...", on_change=envoyer_message)
    with col2:
        st.button("Envoyer", on_click=envoyer_message, use_container_width=True)

    # --- APPEL A L'IA ---
    if st.session_state.get("requete_en_attente", False):
        with st.spinner("Le formateur rédige sa réponse..."):
            try:
                # Nettoyage strict des messages pour l'API Groq
                api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                
                response = client.chat.completions.create(
                    model="llama3-70b-8192",
                    messages=api_messages
                )
                reply = response.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Erreur de communication avec l'API Groq : {e}")
        
        # On remet le signal à zéro pour attendre la prochaine question
        st.session_state.requete_en_attente = False

    # --- AFFICHAGE DE L'HISTORIQUE ---
    st.markdown("### Historique de la session")
    messages_utiles = [m for m in st.session_state.messages if m["role"] != "system"]
    
    # Inversé : du plus récent au plus ancien
    for msg in reversed(messages_utiles):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- BOUTON EXPORT PDF ---
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
