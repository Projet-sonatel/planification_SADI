import streamlit as st
import pandas as pd
import calendar
from datetime import datetime
import sqlite3

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Planification SADI",
    layout="wide",
    initial_sidebar_state="collapsed",
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
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    h2, h3 {
        color: #003D7A;
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* Tabs centrés et compacts */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #f5f5f5;
        padding: 5px;
        border-radius: 8px;
        width: 60%;
        margin: 0 auto;
        display: flex;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: #003D7A;
        font-weight: 500;
        border-radius: 6px;
        padding: 10px 30px;
        flex: 0 1 auto;
        white-space: nowrap;
    }

    .stTabs [aria-selected="true"] {
        background-color: #FF6600;
        color: white;
    }

    /* Boutons primaires */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #FF6600 0%, #FF8533 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 0.5rem 2rem;
        border-radius: 8px;
        transition: all 0.3s;
    }

    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #E65C00 0%, #FF6600 100%);
        box-shadow: 0 4px 12px rgba(255, 102, 0, 0.3);
    }

    /* Métriques */
    [data-testid="stMetricValue"] {
        color: #003D7A;
        font-weight: 600;
    }

    [data-testid="stMetricLabel"] {
        color: #666;
    }

    /* Tableaux */
    .stDataFrame {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
    }

    /* Messages */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #FF6600;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
    }

    /* Checkbox */
    .stCheckbox label {
        font-weight: 500;
        color: #003D7A;
    }

    /* Selectbox */
    .stSelectbox label {
        color: #003D7A;
        font-weight: 500;
    }

    /* Sidebar - Optimisation de l'espace */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #003D7A 0%, #0052A3 100%);
    }

    section[data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #003D7A 0%, #0052A3 100%);
        padding-top: 0.5rem !important;
        padding-bottom: 0.5rem !important;
    }

    /* Réduction des espacements dans la sidebar */
    section[data-testid="stSidebar"] .element-container {
        margin-bottom: 0.2rem !important;
    }

    section[data-testid="stSidebar"] h3 {
        margin-top: 0 !important;
        margin-bottom: 0.3rem !important;
    }

    section[data-testid="stSidebar"] .stMarkdown p {
        margin-bottom: 0.2rem !important;
        margin-top: 0.2rem !important;
    }

    /* Réduction de la hauteur des inputs dans la sidebar */
    section[data-testid="stSidebar"] .stNumberInput > div > div > input {
        padding: 0.3rem 0.5rem !important;
    }

    section[data-testid="stSidebar"] label {
        margin-bottom: 0.1rem !important;
    }

    /* Réduction de l'espace du bouton download */
    section[data-testid="stSidebar"] .stDownloadButton {
        margin-top: 0.3rem !important;
    }

    section[data-testid="stSidebar"] .stDownloadButton button {
        padding: 0.4rem 1rem !important;
    }

    /* Sidebar - titres et textes en blanc */
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
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

    /* Sidebar - inputs */
    section[data-testid="stSidebar"] input {
        background-color: rgba(255, 255, 255, 0.9);
        color: #003D7A;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 6px;
    }

    /* Sidebar - bouton download */
    section[data-testid="stSidebar"] .stDownloadButton button {
        background-color: #FF6600;
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 6px;
    }

    section[data-testid="stSidebar"] .stDownloadButton button:hover {
        background-color: #E65C00;
    }

    /* Masquer les éléments du menu en haut à droite */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    button[title="View app in GitHub"] {display: none;}
    button[kind="header"] {display: none;}
    [data-testid="stToolbar"] {display: none;}

    /* Réduction des marges */
    .element-container {
        margin-bottom: 0.5rem;
    }

    /* Séparateurs */
    hr {
        margin: 1rem 0;
        border-color: #e0e0e0;
    }

    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

DB_FILE = "planifications_sadi.db"

# --- FONCTIONS BASE DE DONNÉES ---
def init_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS planifications (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            SADI TEXT NOT NULL,
            Mois TEXT NOT NULL,
            Annee INTEGER NOT NULL,
            Animation TEXT,
            VTO INTEGER,
            Bus INTEGER,
            Jours TEXT,
            Nb_Jours INTEGER,
            Budget_Resto REAL,
            Budget_Bus REAL,
            Total REAL,
            Date_Creation TEXT
        )
    ''')
    conn.commit()
    conn.close()

def sauvegarder_planification(data):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO planifications
            (SADI, Mois, Annee, Animation, VTO, Bus, Jours, Nb_Jours, Budget_Resto, Budget_Bus, Total, Date_Creation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['SADI'], data['Mois'], data['Annee'], data['Animation'],
            data['VTO'], data['Bus'], data['Jours'], data['Nb Jours'],
            data['Budget Resto'], data['Budget Bus'], data['Total'], data['Date_Creation']
        ))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def charger_toutes_planifications():
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql_query("SELECT * FROM planifications ORDER BY ID DESC", conn)
        conn.close()
        if not df.empty:
            df.rename(columns={
                'Nb_Jours': 'Nb Jours',
                'Budget_Resto': 'Budget Resto',
                'Budget_Bus': 'Budget Bus'
            }, inplace=True)
        return df
    except:
        return pd.DataFrame()

def modifier_planification(id_planif, data):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE planifications
            SET SADI=?, Mois=?, Annee=?, Animation=?, VTO=?, Bus=?,
                Jours=?, Nb_Jours=?, Budget_Resto=?, Budget_Bus=?, Total=?
            WHERE ID=?
        ''', (
            data['SADI'], data['Mois'], data['Annee'], data['Animation'],
            data['VTO'], data['Bus'], data['Jours'], data['Nb Jours'],
            data['Budget Resto'], data['Budget Bus'], data['Total'], id_planif
        ))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def supprimer_planification(id_planif):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM planifications WHERE ID=?", (id_planif,))
        conn.commit()
        conn.close()
        return True
    except:
        return False

# Initialisation
init_database()

if 'db_planification' not in st.session_state:
    st.session_state.db_planification = charger_toutes_planifications()

# --- EN-TÊTE ---
st.title("Planification Mensuelle SADI")
st.markdown("---")

# --- SIDEBAR DESIGN OPTIMISÉ ---
with st.sidebar:
    st.markdown("### ⚙️ Configuration")

    st.markdown("**Tarifs journaliers**")
    cout_bus_jour = st.number_input("Location Bus (FCFA)", value=60000, step=5000)
    cout_resto_vto = st.number_input("Restauration VTO (FCFA)", value=1500, step=100)

    st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)

    if not st.session_state.db_planification.empty:
        st.markdown("**Export des données**")
        from io import BytesIO

        # Préparer les données pour Excel
        colonnes_export = ['ID', 'SADI', 'Mois', 'Annee', 'Animation', 'VTO', 'Bus', 'Nb Jours', 'Total']
        df_export = st.session_state.db_planification[colonnes_export].copy()

        # Créer le fichier Excel en mémoire
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_export.to_excel(writer, index=False, sheet_name='Planifications')

            # Formater la feuille
            worksheet = writer.sheets['Planifications']

            # Largeur des colonnes
            column_widths = {'A': 8, 'B': 15, 'C': 12, 'D': 10, 'E': 30, 'F': 10, 'G': 10, 'H': 12, 'I': 18}
            for col, width in column_widths.items():
                worksheet.column_dimensions[col].width = width

            # Styliser l'en-tête
            from openpyxl.styles import Font, PatternFill, Alignment
            header_fill = PatternFill(start_color="FF6600", end_color="FF6600", fill_type="solid")
            header_font = Font(bold=True, color="FFFFFF", size=11)

            for cell in worksheet[1]:
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal='center', vertical='center')

        buffer.seek(0)

        st.download_button(
            label="📥 Exporter en Excel",
            data=buffer,
            file_name=f"planification_sadi_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# --- ONGLETS (ordre modifié) ---
tab1, tab2, tab3 = st.tabs(["Tableau de bord", "Nouvelle planification", "Modifier / Supprimer"])

# ==================== ONGLET 1 : TABLEAU DE BORD ====================
with tab1:
    if not st.session_state.db_planification.empty:
        mois_noms = list(calendar.month_name)[1:]

        col_filtre1, col_filtre2 = st.columns(2)
        with col_filtre1:
            mois_filtre = st.selectbox("Mois", ["Tous"] + mois_noms)
        with col_filtre2:
            sadi_filtre = st.selectbox("SADI", ["Tous"] + ["THIAROYE", "ACAD", "ZIGUINCHOR", "SAINT LOUIS", "KAOLACK", "TAMBA"])

        # Filtres
        df_mois = st.session_state.db_planification.copy()

        if mois_filtre != "Tous":
            df_mois = df_mois[df_mois["Mois"] == mois_filtre]

        if sadi_filtre != "Tous":
            df_mois = df_mois[df_mois["SADI"] == sadi_filtre]

        if not df_mois.empty:
            # Métriques
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Budget total", f"{df_mois['Total'].sum():,.0f} FCFA")
            m2.metric("Bus", int(df_mois['Bus'].sum()))
            m3.metric("VTO", int(df_mois['VTO'].sum()))
            m4.metric("Planifications", len(df_mois))

            st.markdown("---")

            # Afficher uniquement les colonnes pertinentes
            colonnes_affichees = ['ID', 'SADI', 'Mois', 'Annee', 'Animation', 'VTO', 'Bus', 'Nb Jours', 'Total']
            df_affichage = df_mois[colonnes_affichees]

            st.dataframe(
                df_affichage,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("Aucune donnée pour ces filtres")
    else:
        st.info("La base de données est vide")

# ==================== ONGLET 2 : NOUVELLE PLANIFICATION ====================
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        sadi = st.selectbox("SADI", ["THIAROYE", "ACAD", "ZIGUINCHOR", "SAINT LOUIS", "KAOLACK", "TAMBA"])
        animation = st.text_input("Animation", placeholder="Ex: Tous sur la Fibre")

    with col2:
        annee_actuelle = datetime.now().year
        mois_noms = list(calendar.month_name)[1:]
        mois_select = st.selectbox("Mois", mois_noms, index=datetime.now().month-1)
        index_mois = mois_noms.index(mois_select) + 1
        nb_jours_mois = calendar.monthrange(annee_actuelle, index_mois)[1]

    st.markdown(f"### 📅 Calendrier - {mois_select} {annee_actuelle}")

    # Calendrier
    jours_selectionnes = []
    cols_jours = st.columns(7)
    for i in range(1, nb_jours_mois + 1):
        with cols_jours[(i-1) % 7]:
            if st.checkbox(f"{i}", key=f"new_day_{i}"):
                jours_selectionnes.append(i)

    st.markdown("---")

    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        vto_count = st.number_input("Nombre de VTO", min_value=0, value=60, key="new_vto")
    with col_res2:
        bus_count = st.number_input("Nombre de Bus", min_value=0, value=2, key="new_bus")
    with col_res3:
        nb_jours_actifs = len(jours_selectionnes)
        st.metric("Jours sélectionnés", nb_jours_actifs)

    # Calculs
    budget_resto = vto_count * cout_resto_vto * nb_jours_actifs
    budget_bus = bus_count * cout_bus_jour * nb_jours_actifs
    total_budget = budget_resto + budget_bus

    st.markdown(f"### Budget total : **{total_budget:,.0f} FCFA**")

    col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
    with col_btn2:
        if st.button("Enregistrer", type="primary", use_container_width=True):
            if not jours_selectionnes:
                st.error("Sélectionnez au moins un jour")
            else:
                nouvelle_entree = {
                    "SADI": sadi,
                    "Mois": mois_select,
                    "Annee": annee_actuelle,
                    "Animation": animation,
                    "VTO": vto_count,
                    "Bus": bus_count,
                    "Jours": ", ".join(map(str, jours_selectionnes)),
                    "Nb Jours": nb_jours_actifs,
                    "Budget Resto": budget_resto,
                    "Budget Bus": budget_bus,
                    "Total": total_budget,
                    "Date_Creation": datetime.now().strftime("%Y-%m-%d %H:%M")
                }

                if sauvegarder_planification(nouvelle_entree):
                    st.success("Planification enregistrée")
                    st.session_state.db_planification = charger_toutes_planifications()
                    st.rerun()

# ==================== ONGLET 3 : MODIFIER/SUPPRIMER ====================
with tab3:
    if not st.session_state.db_planification.empty:
        # Afficher uniquement les colonnes pertinentes
        colonnes_affichees = ['ID', 'SADI', 'Mois', 'Annee', 'Animation', 'VTO', 'Bus', 'Nb Jours', 'Total']
        df_affichage = st.session_state.db_planification[colonnes_affichees]

        st.dataframe(
            df_affichage,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        col_select, col_action = st.columns([3, 1])

        with col_select:
            options = []
            for idx, row in st.session_state.db_planification.iterrows():
                option = f"ID {row['ID']} - {row['SADI']} - {row['Mois']} {row['Annee']} - {row['Animation']}"
                options.append(option)

            selected_option = st.selectbox("Sélectionner une planification", options, label_visibility="collapsed")
            selected_id = int(selected_option.split(" - ")[0].replace("ID ", ""))

        with col_action:
            action = st.radio("", ["Modifier", "Supprimer"], horizontal=True, label_visibility="collapsed")

        selected_row = st.session_state.db_planification[
            st.session_state.db_planification['ID'] == selected_id
        ].iloc[0]

        st.markdown("---")

        if action == "Supprimer":
            st.warning(f"Supprimer : **{selected_row['SADI']}** - {selected_row['Mois']} {selected_row['Annee']}")

            col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
            with col_btn2:
                if st.button("Confirmer", type="primary", use_container_width=True):
                    if supprimer_planification(selected_id):
                        st.success("Supprimée")
                        st.session_state.db_planification = charger_toutes_planifications()
                        st.rerun()

        else:  # Modifier
            with st.form("form_modification"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_sadi = st.selectbox(
                        "SADI",
                        ["THIAROYE", "ACAD", "ZIGUINCHOR", "SAINT LOUIS", "KAOLACK", "TAMBA"],
                        index=["THIAROYE", "ACAD", "ZIGUINCHOR", "SAINT LOUIS", "KAOLACK", "TAMBA"].index(selected_row['SADI'])
                    )
                    edit_animation = st.text_input("Animation", value=selected_row['Animation'])

                with col2:
                    mois_noms = list(calendar.month_name)[1:]
                    edit_mois = st.selectbox("Mois", mois_noms, index=mois_noms.index(selected_row['Mois']))
                    edit_annee = st.number_input("Année", value=int(selected_row['Annee']), min_value=2020, max_value=2030)

                # Calendrier
                index_mois = mois_noms.index(edit_mois) + 1
                nb_jours_mois = calendar.monthrange(int(edit_annee), index_mois)[1]

                st.markdown(f"### 📅 Calendrier - {edit_mois} {edit_annee}")
                jours_existants = [int(j.strip()) for j in str(selected_row['Jours']).split(',') if j.strip().isdigit()]

                edit_jours_selectionnes = []
                cols_jours = st.columns(7)
                for i in range(1, nb_jours_mois + 1):
                    with cols_jours[(i-1) % 7]:
                        is_checked = i in jours_existants
                        if st.checkbox(f"{i}", key=f"edit_day_{i}", value=is_checked):
                            edit_jours_selectionnes.append(i)

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    edit_vto = st.number_input("VTO", min_value=0, value=int(selected_row['VTO']), key="edit_vto")
                with col_res2:
                    edit_bus = st.number_input("Bus", min_value=0, value=int(selected_row['Bus']), key="edit_bus")
                with col_res3:
                    edit_nb_jours = len(edit_jours_selectionnes)
                    st.metric("Jours sélectionnés", edit_nb_jours)

                edit_budget_resto = edit_vto * cout_resto_vto * edit_nb_jours
                edit_budget_bus = edit_bus * cout_bus_jour * edit_nb_jours
                edit_total_budget = edit_budget_resto + edit_budget_bus

                st.markdown(f"### Budget total : **{edit_total_budget:,.0f} FCFA**")

                submitted = st.form_submit_button("Enregistrer les modifications", type="primary", use_container_width=True)

                if submitted:
                    if not edit_jours_selectionnes:
                        st.error("Sélectionnez au moins un jour")
                    else:
                        data_modifiee = {
                            "SADI": edit_sadi,
                            "Mois": edit_mois,
                            "Annee": edit_annee,
                            "Animation": edit_animation,
                            "VTO": edit_vto,
                            "Bus": edit_bus,
                            "Jours": ", ".join(map(str, edit_jours_selectionnes)),
                            "Nb Jours": edit_nb_jours,
                            "Budget Resto": edit_budget_resto,
                            "Budget Bus": edit_budget_bus,
                            "Total": edit_total_budget
                        }

                        if modifier_planification(selected_id, data_modifiee):
                            st.success("Planification modifiée")
                            st.session_state.db_planification = charger_toutes_planifications()
                            st.rerun()
    else:
        st.info("Aucune planification disponible")