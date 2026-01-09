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

# --- ONGLETS PRINCIPAUX ---
tab1, tab2, tab3 = st.tabs(["✍️ Nouvelle Planification", "✏️ Modifier/Supprimer", "📊 Tableau de Bord"])

# ==================== ONGLET 1 : NOUVELLE PLANIFICATION ====================
with tab1:
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
                if st.checkbox(f"J{i}", key=f"new_day_{i}"):
                    jours_selectionnes.append(i)

        st.markdown("---")

        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            vto_count = st.number_input("Nombre de VTO", min_value=0, value=60, key="new_vto")
        with col_res2:
            bus_count = st.number_input("Nombre de Bus", min_value=0, value=2, key="new_bus")
        with col_res3:
            nb_jours_actifs = len(jours_selectionnes)
            st.metric("Total Jours Actifs", nb_jours_actifs)

        # CALCULS BUDGÉTAIRES
        budget_resto = vto_count * cout_resto_vto * nb_jours_actifs
        budget_bus = bus_count * cout_bus_jour * nb_jours_actifs
        total_budget = budget_resto + budget_bus

        st.subheader(f"💵 Récapitulatif Budgétaire : {total_budget:,.0f} FCFA")

        if st.button("💾 Enregistrer la planification du mois", type="primary"):
            if not jours_selectionnes:
                st.error("Veuillez sélectionner au moins un jour dans le calendrier.")
            else:
                nouvelle_entree = {
                    "ID": len(st.session_state.db_planification) + 1,
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
                st.success(f"✅ Planification de {mois_select} pour {sadi} enregistrée !")
                st.balloons()

# ==================== ONGLET 2 : MODIFIER/SUPPRIMER ====================
with tab2:
    st.header("✏️ Modifier ou Supprimer une Planification")

    if not st.session_state.db_planification.empty:
        # Affichage de toutes les planifications
        st.subheader("📋 Liste des Planifications Existantes")
        df_display = st.session_state.db_planification.copy()
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.markdown("---")

        # Sélection de la planification à modifier
        col_select, col_action = st.columns([3, 1])

        with col_select:
            # Créer une liste d'options pour la sélection
            options = []
            for idx, row in st.session_state.db_planification.iterrows():
                option = f"ID {row['ID']} - {row['SADI']} - {row['Mois']} {row['Annee']} - {row['Animation']}"
                options.append(option)

            selected_option = st.selectbox("Sélectionnez une planification à modifier/supprimer", options)
            selected_id = int(selected_option.split(" - ")[0].replace("ID ", ""))

        with col_action:
            st.write("")
            st.write("")
            action = st.radio("Action", ["Modifier", "Supprimer"], horizontal=True)

        # Récupérer la ligne sélectionnée
        selected_row = st.session_state.db_planification[
            st.session_state.db_planification['ID'] == selected_id
        ].iloc[0]

        st.markdown("---")

        if action == "Supprimer":
            st.warning(f"⚠️ Vous êtes sur le point de supprimer la planification : **{selected_row['SADI']} - {selected_row['Mois']} {selected_row['Annee']}**")

            col_confirm, col_cancel = st.columns([1, 4])
            with col_confirm:
                if st.button("🗑️ Confirmer la suppression", type="primary"):
                    st.session_state.db_planification = st.session_state.db_planification[
                        st.session_state.db_planification['ID'] != selected_id
                    ].reset_index(drop=True)
                    st.success("✅ Planification supprimée avec succès !")
                    st.rerun()

        else:  # Modifier
            st.subheader(f"✏️ Modification de : {selected_row['SADI']} - {selected_row['Mois']} {selected_row['Annee']}")

            with st.form("form_modification"):
                col1, col2 = st.columns(2)

                with col1:
                    edit_sadi = st.selectbox(
                        "SADI",
                        ["THIAROYE", "ACAD", "ZIGUINCHOR", "SAINT LOUIS", "KAOLACK", "TAMBA"],
                        index=["THIAROYE",  "ACAD", "ZIGUINCHOR", "SAINT LOUIS", "KAOLACK", "TAMBA"].index(selected_row['SADI'])
                    )
                    edit_animation = st.text_input("Nom de l'animation", value=selected_row['Animation'])

                with col2:
                    mois_noms = list(calendar.month_name)[1:]
                    edit_mois = st.selectbox(
                        "Mois",
                        mois_noms,
                        index=mois_noms.index(selected_row['Mois'])
                    )
                    edit_annee = st.number_input("Année", value=int(selected_row['Annee']), min_value=2020, max_value=2030)

                # Calendrier pour modification
                index_mois = mois_noms.index(edit_mois) + 1
                nb_jours_mois = calendar.monthrange(int(edit_annee), index_mois)[1]

                st.write(f"### 📅 Calendrier de {edit_mois} {edit_annee}")

                # Récupérer les jours déjà sélectionnés
                jours_existants = [int(j.strip()) for j in str(selected_row['Jours']).split(',') if j.strip().isdigit()]

                edit_jours_selectionnes = []
                cols_jours = st.columns(7)
                for i in range(1, nb_jours_mois + 1):
                    with cols_jours[(i-1) % 7]:
                        is_checked = i in jours_existants
                        if st.checkbox(f"J{i}", key=f"edit_day_{i}", value=is_checked):
                            edit_jours_selectionnes.append(i)

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    edit_vto = st.number_input("Nombre de VTO", min_value=0, value=int(selected_row['VTO']), key="edit_vto")
                with col_res2:
                    edit_bus = st.number_input("Nombre de Bus", min_value=0, value=int(selected_row['Bus']), key="edit_bus")
                with col_res3:
                    edit_nb_jours = len(edit_jours_selectionnes)
                    st.metric("Total Jours Actifs", edit_nb_jours)

                # Recalcul du budget
                edit_budget_resto = edit_vto * cout_resto_vto * edit_nb_jours
                edit_budget_bus = edit_bus * cout_bus_jour * edit_nb_jours
                edit_total_budget = edit_budget_resto + edit_budget_bus

                st.subheader(f"💵 Nouveau Récapitulatif Budgétaire : {edit_total_budget:,.0f} FCFA")

                submitted = st.form_submit_button("💾 Enregistrer les modifications", type="primary")

                if submitted:
                    if not edit_jours_selectionnes:
                        st.error("Veuillez sélectionner au moins un jour dans le calendrier.")
                    else:
                        # Mettre à jour la ligne
                        idx = st.session_state.db_planification[
                            st.session_state.db_planification['ID'] == selected_id
                        ].index[0]

                        st.session_state.db_planification.at[idx, 'SADI'] = edit_sadi
                        st.session_state.db_planification.at[idx, 'Mois'] = edit_mois
                        st.session_state.db_planification.at[idx, 'Annee'] = edit_annee
                        st.session_state.db_planification.at[idx, 'Animation'] = edit_animation
                        st.session_state.db_planification.at[idx, 'VTO'] = edit_vto
                        st.session_state.db_planification.at[idx, 'Bus'] = edit_bus
                        st.session_state.db_planification.at[idx, 'Jours'] = ", ".join(map(str, edit_jours_selectionnes))
                        st.session_state.db_planification.at[idx, 'Nb Jours'] = edit_nb_jours
                        st.session_state.db_planification.at[idx, 'Budget Resto'] = edit_budget_resto
                        st.session_state.db_planification.at[idx, 'Budget Bus'] = edit_budget_bus
                        st.session_state.db_planification.at[idx, 'Total'] = edit_total_budget

                        st.success(f"✅ Planification modifiée avec succès !")
                        st.balloons()
                        st.rerun()

    else:
        st.info("📭 Aucune planification à modifier. Créez-en une dans l'onglet 'Nouvelle Planification'.")

# ==================== ONGLET 3 : TABLEAU DE BORD ====================
with tab3:
    st.header("📊 Suivi Bureau - Vue Mensuelle")

    if not st.session_state.db_planification.empty:
        # Filtre par mois pour le décideur
        mois_noms = list(calendar.month_name)[1:]
        mois_filtre = st.selectbox("Filtrer la vue par mois", ["Tous"] + mois_noms)

        if mois_filtre == "Tous":
            df_mois = st.session_state.db_planification
        else:
            df_mois = st.session_state.db_planification[
                st.session_state.db_planification["Mois"] == mois_filtre
            ]

        if not df_mois.empty:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(f"Budget total", f"{df_mois['Total'].sum():,.0f} FCFA")
            m2.metric("Total Bus mobilisés", int(df_mois['Bus'].sum()))
            m3.metric("Total VTO mobilisés", int(df_mois['VTO'].sum()))
            m4.metric("Nombre de planifications", len(df_mois))

            st.markdown("---")
            st.dataframe(df_mois, use_container_width=True, hide_index=True)

            # Graphiques
            col_graph1, col_graph2 = st.columns(2)

            with col_graph1:
                st.subheader("💰 Budget par SADI")
                st.bar_chart(df_mois.set_index("SADI")["Total"])

            with col_graph2:
                st.subheader("📊 Répartition par mois")
                budget_par_mois = df_mois.groupby("Mois")["Total"].sum()
                st.bar_chart(budget_par_mois)
        else:
            st.warning(f"Aucune donnée enregistrée pour le mois de {mois_filtre}")
    else:
        st.info("📭 La base de données est vide. Veuillez saisir une planification dans l'onglet 'Nouvelle Planification'.")