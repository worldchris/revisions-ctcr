import streamlit as st
import datetime
from fpdf import FPDF
import tempfile
import random

# --- CONFIGURATION ---
MOT_DE_PASSE = "Crossway2026"

st.set_page_config(page_title="Révisions Permis D & FIMO", page_icon="🚌", layout="centered")

# --- AUTHENTIFICATION ---
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

# --- GÉNÉRATION DU PDF ---
def create_pdf(titre, contenu):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Portail de Revision - Titre Pro CTCR & FIMO", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'I', size=9)
    pdf.multi_cell(0, 6, txt="Reference officielle AFTRAL 2026 - Document de travail du groupe.")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', size=12)
    pdf.cell(200, 10, txt=titre, ln=True, align='L')
    pdf.ln(3)
    
    pdf.set_font("Arial", size=10)
    texte_clean = contenu.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 6, txt=texte_clean)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# --- BANQUE DE QUESTIONS / ENTRAÎNEMENT INTÉGRÉE ---
BANQUE_QUESTIONS = [
    {
        "q": "Quelle est la durée maximale de conduite continue autorisée en transport de voyageurs avant d'observer une pause obligatoire ?",
        "options": ["3 heures", "4 heures 30", "6 heures", "9 heures"],
        "reponse": "4 heures 30",
        "explication": "La réglementation sociale européenne (RSE) impose une pause de 45 minutes après 4h30 de conduite continue (fractionnable en 15 min puis 30 min)."
    },
    {
        "q": "Dans le cadre du Socle 1, que doit impérativement contrôler le conducteur concernant les pneumatiques ?",
        "options": ["Uniquement la pression à chaud", "L'usure de la bande de roulement, l'absence de coupures, la pression et l'absence de corps étrangers", "Seulement le sens de rotation", "Le pays de fabrication du pneu"],
        "reponse": "L'usure de la bande de roulement, l'absence de coupures, la pression et l'absence de corps étrangers",
        "explication": "Le contrôle visuel et physique des pneumatiques est vital pour la sécurité du car : témoins d'usure, flancs, hernies et corps étrangers."
    },
    {
        "q": "Combien de fois par semaine un conducteur peut-il porter sa durée journalière de conduite à 10 heures ?",
        "options": ["1 fois par semaine", "2 fois par semaine", "3 fois par semaine", "Jamais, c'est bloqué à 9h"],
        "reponse": "2 fois par semaine",
        "explication": "La RSE autorise l'extension de la conduite journalière de 9h à 10h au maximum deux fois par semaine."
    },
    {
        "q": "Quel est le principe majeur concernant le porte-à-faux arrière d'un autocar lors d'un virage serré ?",
        "options": ["Il suit exactement la trajectoire des roues avant", "Il se déporte vers l'extérieur du virage", "Il se déporte vers l'intérieur du virage", "Il n'a aucun impact sur la trajectoire"],
        "reponse": "Il se déporte vers l'extérieur du virage",
        "explication": "En raison de la longueur du porte-à-faux arrière, l'arrière du car balaie une trajectoire inverse et externe, nécessitant une grande vigilance dans les intersections."
    },
    {
        "q": "Quelle est la durée du repos hebdomadaire normal pour un conducteur de car ?",
        "options": ["24 heures consécutives", "36 heures consécutives", "45 heures consécutives", "48 heures consécutives"],
        "reponse": "45 heures consécutives",
        "explication": "Le repos hebdomadaire normal est de 45 heures (réductible à 24h sous conditions de compensation)."
    },
    {
        "q": "Fiche Orale : Que doit vérifier en premier le conducteur lors de la prise en poste (installation) ?",
        "options": ["Le volume de la radio", "Le réglage du siège, des rétroviseurs et l'accessibilité des commandes", "La propreté des vitres latérales uniquement", "La température de la climatisation"],
        "reponse": "Le réglage du siège, des rétroviseurs et l'accessibilité des commandes",
        "explication": "L'ergonomie et la visibilité périphérique (élimination des angles morts) sont les bases de l'installation du conducteur."
    }
]

# --- APPLICATION PRINCIPALE ---
if check_password():
    st.title("🚌 Centre Complet de Révision - Permis D & FIMO")
    st.markdown("**Titre Pro CTCR Voyageurs - Référentiel AFTRAL 2026**")
    
    onglet = st.tabs(["📚 Cours & Fiches Officielles", "🧠 Entraînement & QCM", "📋 Fiches Orales Détaillées"])

    # --- ONGLET 1 : COURS & FICHES OFFICIELLES ---
    with onglet[0]:
        st.header("Modules de Cours Détaillés")
        module = st.selectbox(
            "Sélectionnez un module à consulter :",
            [
                "Module 1 : Réglementation Sociale Européenne (RSE) & Tachygraphe",
                "Module 2 : Socles de Sécurité 1 & 2 (Vérifications et Organes)",
                "Module 3 : Sécurité des Passagers & Accessibilité PMR"
            ]
        )

        st.markdown("---")

        if "Module 1" in module:
            titre_f = "Règlementation Sociale Européenne (RSE) & Temps de Travail"
            st.subheader(titre_f)
            contenu_f = """
            1. TEMPS DE CONDUITE :
            - Conduite continue max : 4h30, puis pause obligatoire de 45 min (ou 15 min + 30 min).
            - Conduite journalière max : 9h (extensible à 10h, deux fois par semaine).
            - Conduite hebdomadaire max : 56h.
            - Conduite bi-hebdomadaire max : 90h sur 2 semaines consécutives.

            2. TEMPS DE REPOS :
            - Repos journalier normal : 11h consécutives (réductible à 9h, 3 fois entre deux repos hebdo).
            - Repos journalier fractionné : 12h au total (3h + 9h).
            - Repos hebdomadaire normal : 45h consécutives.
            - Repos hebdomadaire réduit : 24h consécutives (compensé par un bloc équivalent avant la fin de la 3ème semaine).

            3. LE CHRONOTACHYGRAPHE :
            - Outil de contrôle électronique obligatoire. Enregistre la vitesse, les distances, les temps de conduite, les autres travaux, les disponibilités et les pauses.
            - Utilisation correcte de la carte conducteur et sélection manuelle des activités requise.
            """
            st.markdown(contenu_f)

        elif "Module 2" in module:
            titre_f = "Socles de Sécurité 1 & 2 (Vérifications, Freins & Mécanique)"
            st.subheader(titre_f)
            contenu_f = """
            SOCLE 1 - VÉRIFICATIONS COURANTES AVANT DÉPART :
            - PÉRIMÈTRE EXTÉRIEUR : État de la carrosserie, pare-brise, optiques de phares, rétroviseurs, propreté des surfaces vitrées.
            - PNEUMATIQUES : Profondeur des sculptures, absence de hernies, coupures, corps étrangers, vérification de la pression.
            - NIVEAUX : Liquide de refroidissement, huile moteur, liquide de direction assistée, lave-glace.
            - ÉQUIPEMENTS DE SÉCURITÉ : Extincteurs périmés ou non, triangles, gilets haute visibilité, marteaux brise-vitre d'urgence, trousse de secours.

            SOCLE 2 - FREINAGE, ORGANES MÉCANIQUES & COMMANDES :
            - CIRCUIT DE FREINAGE : Purge des réservoirs d'air (présence d'humidité/huile), contrôle du fonctionnement du frein de service et du frein de parc (ressort).
            - DIRECTION & SUSPENSIONS : Jeu dans le volant, bon fonctionnement des suspensions pneumatiques et mise à niveau de l'assiette du car.
            - PORTES & ACCÈS : Sécurisation de la fermeture des portes, fonctionnement des dispositifs anti-pincement et commandes de secours d'ouverture des portes.
            """
            st.markdown(contenu_f)

        elif "Module 3" in module:
            titre_f = "Sécurité des Passagers, Accueil & Conduite Préventive"
            st.subheader(titre_f)
            contenu_f = """
            1. ACCUEIL ET INFORMATION :
            - Accueil des voyageurs, vérification visuelle des titres de transport.
            - Rappel obligatoire des consignes de sécurité : port de la ceinture de sécurité obligatoire dans les autocars équipés, interdiction de fumer/vapoter, emplacement des issues de secours.

            2. CONDUITE PRÉVENTIVE EN VÉHICULE LOURD :
            - Anticipation du gabarit (hauteur des ponts, largeur, porte-à-faux arrière important en virage).
            - Gestion du report de charge et du confort des passagers (souplesse au freinage et à l'accélération).
            - Distances de sécurité accrues (notamment sur autoroute et par temps de pluie).
            """
            st.markdown(contenu_f)

        st.markdown("---")
        if st.button("📥 Télécharger ce module en PDF"):
            pdf_path = create_pdf(titre_f, contenu_f)
            with open(pdf_path, "rb") as f_pdf:
                st.download_button("Cliquer pour enregistrer le fichier", data=f_pdf, file_name=f"Cours_AFTRAL_{datetime.date.today()}.pdf", mime="application/pdf")

    # --- ONGLET 2 : ENTRAÎNEMENT & QCM ---
    with onglet[1]:
        st.header("🧠 Banque d'Entraînement Interactive")
        st.markdown("Teste tes connaissances sur le modèle des questions officielles de l'examen.")

        if "score" not in st.session_state:
            st.session_state.score = 0
        if "question_index" not in st.session_state:
            st.session_state.question_index = 0

        q_data = BANQUE_QUESTIONS[st.session_state.question_index]

        st.markdown(f"**Question {st.session_state.question_index + 1} sur {len(BANQUE_QUESTIONS)}**")
        st.info(q_data["q"])

        choix = st.radio("Sélectionnez votre réponse :", q_data["options"], key=f"q_{st.session_state.question_index}")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Valider la réponse"):
                if choix == q_data["reponse"]:
                    st.success("✅ Bonne réponse !")
                else:
                    st.error(f"❌ Mauvaise réponse. La bonne réponse était : **{q_data['reponse']}**")
                st.markdown(f"💡 *Explication :* {q_data['explication']}")
        
        with col_b:
            if st.button("Question suivante ➡️"):
                st.session_state.question_index = (st.session_state.question_index + 1) % len(BANQUE_QUESTIONS)
                st.rerun()

    # --- ONGLET 3 : FICHES ORALES DÉTAILLÉES ---
    with onglet[2]:
        st.header("📋 Les 6 Fiches Orales Officielles de l'Autocar")
        st.markdown("Chaque fiche doit être présentée clairement lors de l'épreuve orale avec un argumentaire structuré.")

        fiches_orales = {
            "Fiche 1 : Contrôles de sécurité avant départ": "Vérification exhaustive du véhicule : documents de bord réglementaires (copie conforme de la licence communautaire, cartes et bon fonctionnement du chronotachygraphe numérique/intelligent, conformité de l'assurance via le fichier officiel), état extérieur, propreté, fonctionnement des feux et des dispositifs de signalisation.",
            "Fiche 2 : Installation au poste de conduite & Visibilité": "Réglage ergonomique du siège (suspension, distance), réglage des rétroviseurs grand angle et de proximités pour éliminer les angles morts, prise en main des commandes de bord.",
            "Fiche 3 : Masses, dimensions et chargement": "Respect du P.T.A.C., répartition des bagages en soute (poids lourd en bas, répartition équilibrée gauche/droite), hauteur et largeur de l'autocar face aux infrastructures (ponts, tunnels, gabarits étroits).",
            "Fiche 4 : Sécurité des passagers et situations d'urgence": "Information des voyageurs, port de la ceinture, maîtrise de l'ouverture d'urgence des portes et des issues de secours, évacuation rapide en cas d'incendie ou d'accident.",
            "Fiche 5 : Éco-conduite et mécanique du véhicule": "Anticipation de la circulation, utilisation optimale des plages de régime moteur (couple), utilisation du ralentisseur (hydraulique ou électromagnétique) pour préserver les freins de service.",
            "Fiche 6 : Réglementation du transport et gestion des incidents": "Application stricte de la RSE, respect des temps de pause, gestion des aléas sur la route (retards, pannes, comportements indésirables de passagers) et procédures d'urgence."
        }

        for titre_fo, desc_fo in fiches_orales.items():
            with st.expander(titre_fo):
                st.write(desc_fo)
