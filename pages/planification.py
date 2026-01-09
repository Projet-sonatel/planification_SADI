import streamlit as st
import pandas as pd
import calendar
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="SADI - Planification Mensuelle", layout="wide")

# Initialisation de la base de données en mémoire
if 'db_planification' not in st.session_state:
    st.session_state.db_planification = pd.DataFrame()

st.title("🗓️ Planification Digitale SADI")
st.markdown("---")

# --- PARAMÈTRES DE COÛTS (Sidebar) ---
st.sidebar.header("💰 Configuration des Tarifs")
cout_bus_jour = st.sidebar.number_input("Location Bus / Jour (FCFA)", value=60000)
cout_resto_vto = st.sidebar.number_input("Resto / VTO / Jour (FCFA)", value=1500)

# --- SECTION 1 : SAISIE DU PLANNING ---
st.header("✍️ Saisie de la Planification")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        sadi = st.selectbox("SADI", ["THIAROYE", "RUFISQUE", "PIKINE", "GUEDIAWAYE", "KEUR MASSAR", "SUD EST", "NORD"])
        animation = st.text_input("Nom de l'animation", placeholder="Ex: Tous sur la Fibre")

    with col2:
        # Gestion dynamique du mois et de l'année
        annee_actuelle = datetime.now().year
        mois_noms = list(calendar.month_name)[1:]
        mois_select = st.selectbox("Mois de planification", mois_noms, index=datetime.now().month-1)

        # Trouver le nombre de jours exact pour ce mois
        index_mois = mois_noms.index(mois_select) + 1
        nb_jours_mois = calendar.monthrange(annee_actuelle, index_mois)[1]

    st.write(f"### 📅 Calendrier de {mois_select} {annee_actuelle}")
    st.info("Cochez les jours où l'animation aura lieu sur le terrain.")

    # Affichage des jours sous forme de grille (7 colonnes pour une semaine)
    jours_selectionnes = []
    cols_jours = st.columns(7)
    for i in range(1, nb_jours_mois + 1):
        with cols_jours[(i-1) % 7]:
            if st.checkbox(f"J{i}", key=f"day_{i}"):
                jours_selectionnes.append(i)

    st.markdown("---")

    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        vto_count = st.number_input("Nombre de VTO", min_value=0, value=60)
    with col_res2:
        bus_count = st.number_input("Nombre de Bus", min_value=0, value=2)
    with col_res3:
        nb_jours_actifs = len(jours_selectionnes)
        st.metric("Total Jours Actifs", nb_jours_actifs)

    # CALCULS BUDGÉTAIRES (Logique du fichier SADI)
    budget_resto = vto_count * cout_resto_vto * nb_jours_actifs
    budget_bus = bus_count * cout_bus_jour * nb_jours_actifs
    total_budget = budget_resto + budget_bus

    st.subheader(f"💵 Récapitulatif Budgétaire : {total_budget:,.0f} FCFA")

    if st.button("💾 Enregistrer la planification du mois"):
        if not jours_selectionnes:
            st.error("Veuillez sélectionner au moins un jour dans le calendrier.")
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
                "Total": total_budget
            }

            st.session_state.db_planification = pd.concat([
                st.session_state.db_planification,
                pd.DataFrame([nouvelle_entree])
            ], ignore_index=True)
            st.success(f"Planification de {mois_select} pour {sadi} enregistrée !")

# --- SECTION 2 : DASHBOARD DÉCIDEUR ---
st.markdown("---")
st.header("📊 Suivi Bureau - Vue Mensuelle")

if not st.session_state.db_planification.empty:
    # Filtre par mois pour le décideur
    mois_filtre = st.selectbox("Filtrer la vue par mois", mois_noms, index=mois_noms.index(mois_select))
    df_mois = st.session_state.db_planification[st.session_state.db_planification["Mois"] == mois_filtre]

    if not df_mois.empty:
        m1, m2, m3 = st.columns(3)
        m1.metric(f"Budget total {mois_filtre}", f"{df_mois['Total'].sum():,.0f} FCFA")
        m2.metric("Total Bus mobilisés", int(df_mois['Bus'].sum()))
        m3.metric("Total VTO mobilisés", int(df_mois['VTO'].sum()))

        st.dataframe(df_mois, use_container_width=True)

        # Graphique
        st.bar_chart(df_mois.set_index("SADI")["Total"])
    else:
        st.warning(f"Aucune donnée enregistrée pour le mois de {mois_filtre}")
else:
    st.info("La base de données est vide. Veuillez saisir une planification ci-dessus.")