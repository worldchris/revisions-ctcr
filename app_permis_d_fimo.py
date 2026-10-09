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
    
    # Navigation par onglets étendue
    onglet = st.tabs([
        "📚 Cours & Fiches", 
        "🧠 Entraînement QCM", 
        "📋 6 Thèmes & 12 Fiches Orales", 
        "📺 Tutos & Vidéos YouTube"
    ])

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

    # --- ONGLET 3 : 6 THÈMES & 12 FICHES ORALES ---
    with onglet[2]:
        st.header("📋 Référentiel : 6 Thèmes & 12 Fiches Orales")
        st.markdown("Structure officielle de l'épreuve du Titre Pro CTCR.")

        st.subheader("Les 6 Thèmes Majeurs")
        st.markdown("""
        1. **Réglementation du transport routier de voyageurs** (RSE, documents, contrats).
        2. **Sécurité et sûreté** (contrôles, prévention des risques, gestion des conflits/terrorisme).
        3. **Technique et mécanique du véhicule** (organes, fonctionnement, sécurité active/passive).
        4. **Environnement et éco-conduite** (maîtrise de l'énergie, cinématique du car).
        5. **Accueil, commercial et relation client** (qualité de service, prise en charge PMR).
        6. **Gestion des situations d'urgence et des aléas** (accidents, pannes, incidents de parcours).
        """)

        st.markdown("---")
        st.subheader("Les 12 Fiches Orales Officielles")
        
        fiches_orales_12 = {
            "Fiche 1 : Documents de bord et conformité réglementaire": "Vérification de la licence communautaire, cartes tachygraphes, vérification de l'assurance via le fichier FVA et carnets de route.",
            "Fiche 2 : Contrôles extérieurs de sécurité (Socle 1)": "État de la carrosserie, des optiques, des rétroviseurs, absence de chocs et propreté des surfaces vitrées.",
            "Fiche 3 : Pneumatiques et liaisons au sol": "Contrôle de l'usure de la bande de roulement, pression, hernies, coupures et présence de corps étrangers.",
            "Fiche 4 : Installation au poste de conduite et ergonomie": "Réglage du siège, du volant, des ceintures et élimination des angles morts par le positionnement des rétroviseurs.",
            "Fiche 5 : Commandes de bord et équipements de sécurité": "Vérification des voyants, avertisseurs sonores, trousse de secours, extincteurs et marteaux brise-vitres.",
            "Fiche 6 : Système de freinage et circuits pneumatiques": "Contrôle des purges de réservoirs d'air, test du frein de service, du ralentisseur et du frein de parc.",
            "Fiche 7 : Masses, dimensions et répartition du chargement": "Respect du PTAC, chargement et arrimage des bagages en soute, équilibrage des charges (gauche/droite).",
            "Fiche 8 : Sécurité des passagers et montée/descente": "Contrôle des portes, sécurisation de l'embarquement, zones de circulation à bord et port de la ceinture.",
            "Fiche 9 : Accessibilité et équipements PMR": "Mise en œuvre de la rampe d'accès UFR (Fauteuil Roulant), dispositifs de fixation et consignes d'embarquement spécifique.",
            "Fiche 10 : Éco-conduite et maîtrise de la cinématique": "Anticipation des trajectoires, gestion du porte-à-faux arrière et utilisation des plages de couple moteur.",
            "Fiche 11 : Conduite en conditions difficiles": "Adaptation de la vitesse par temps de pluie, brouillard, neige, verglas ou en circulation dense (intersections).",
            "Fiche 12 : Situations d'urgence, évacuation et incendie": "Procédures d'évacuation rapide des passagers, utilisation des issues de secours et conduites à tenir en cas de sinistre."
        }

        for titre_fo, desc_fo in fiches_orales_12.items():
            with st.expander(titre_fo):
                st.write(desc_fo)

    # --- ONGLET 4 : TUTOS & VIDÉOS YOUTUBE ---
    with onglet[3]:
        st.header("📺 Tutoriels & Vidéos YouTube Recommandés")
        st.markdown("Ressources visuelles indispensables pour réviser les gestes techniques, les fiches orales et la conduite en autocar.")

        st.markdown("""
        Pour compléter vos révisions avec des démonstrations en conditions réelles, voici les recherches ciblées et chaînes à suivre sur YouTube :

        * **🔍 Pour réviser les Fiches Orales et les Contrôles (Socle 1 & 2) :**
          * Tapez sur YouTube : `Fiches orales transport en commun autocar` ou `Contrôle avant départ car AFTRAL`.
          * Vous y trouverez des vidéos de formateurs présentant pas à pas le tour du véhicule et la méthode pour réussir l'oral.

        * **🔍 Pour la Maîtrise du Chronotachygraphe et de la RSE :**
          * Tapez sur YouTube : `Utilisation chronotachygraphe numerique conducteur autocar` ou `Temps de conduite et de repos FIMO FT`.

        * **🔍 Pour la Conduite et la Manoeuvrabilité (Porte-à-faux, angles morts) :**
          * Tapez sur YouTube : `Conduite autocar gabarit maniabilité` pour observer les trajectoires en circulation et en virage serré.

        * **💡 Conseil du groupe :** Regarder ces vidéos le soir sur smartphone permet d'ancrer visuellement les procédures avant de les pratiquer en centre de formation.
        """)
