import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Planification SADI",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# CSS personnalisé - Couleurs Sonatel
st.markdown("""
    <style>
    /* Couleurs Sonatel */
    :root {
        --sonatel-orange: #FF6600;
        --sonatel-blue: #003D7A;
    }

    /* Réduction des espacements */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    h1 {
        color: #003D7A;
        font-weight: 700;
        text-align: center;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    h2, h3 {
        color: #003D7A;
    }

    /* Cards personnalisées */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #FF6600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        height: 100%;
    }

    .feature-card h4 {
        color: #FF6600;
        margin-bottom: 0.5rem;
    }

    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #003D7A 0%, #0052A3 100%);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #003D7A 0%, #0052A3 100%);
    }

    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #003D7A 0%, #0052A3 100%);
    }

    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] a,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"],
    section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] span {
        color: white !important;
    }

    /* Links de navigation dans la sidebar */
    .css-1544g2n, .css-1vq4p4l, .st-emotion-cache-1vq4p4l {
        color: white !important;
    }

    /* Hover sur les liens */
    section[data-testid="stSidebar"] a:hover {
        background-color: rgba(255, 102, 0, 0.2);
        color: white !important;
    }

    /* Masquer les éléments du menu */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    button[title="View app in GitHub"] {display: none;}
    button[kind="header"] {display: none;}
    [data-testid="stToolbar"] {display: none;}

    footer {visibility: hidden;}

    /* Séparateurs */
    hr {
        margin: 1.5rem 0;
        border-color: #e0e0e0;
    }
    </style>
""", unsafe_allow_html=True)

# En-tête avec hero section
st.markdown("""
    <div class="hero-section">
        <h1 style="color: white; margin: 0;">Planification Mensuelle SADI</h1>
        <p style="font-size: 1.1rem; margin-top: 0.5rem;">Gestion des animations terrain et budgets</p>
    </div>
""", unsafe_allow_html=True)

# Description succincte
st.markdown("""
Cette application permet de planifier les animations mensuelles, gérer les ressources (VTO, Bus)
et suivre les budgets pour chaque SADI.
""")

st.markdown("---")

# Fonctionnalités principales
st.markdown("### Fonctionnalités")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h4>📊 Tableau de bord</h4>
        <p>Visualisation des planifications avec filtres par mois et SADI. Export Excel des données.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h4>📝 Planification</h4>
        <p>Création de planifications mensuelles avec sélection calendaire et calcul automatique des budgets.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h4>✏️ Gestion</h4>
        <p>Modification et suppression des planifications existantes avec mise à jour en temps réel.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# SADI couverts
st.markdown("### SADI couverts")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    - **THIAROYE**
    - **ACAD**
    - **ZIGUINCHOR**
    """)

with col2:
    st.markdown("""
    - **SAINT LOUIS**
    - **KAOLACK**
    - **TAMBA**
    """)

st.markdown("---")

# Bouton d'accès
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    st.markdown("""
    <div style="text-align: center;">
        <p style="font-size: 1.1rem; color: #003D7A; font-weight: 600;">
        👈 Accédez à la planification via le menu latéral
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Système de planification SADI - Sonatel")