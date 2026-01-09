import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="SADI - Gestion Planification",
    page_icon="🗓️",
    layout="wide"
)

# En-tête principal
st.title("🗓️ Système de Planification SADI")
st.markdown("---")

# Introduction
st.markdown("""
## Bienvenue dans l'application de planification digitale SADI

Cette application vous permet de :
- ✅ Planifier les animations mensuelles par SADI
- 📊 Visualiser les budgets et ressources mobilisées
- 📅 Gérer le calendrier des activités terrain
- 💰 Suivre les coûts (Bus, Restauration, etc.)

### 🚀 Pour commencer

👈 **Utilisez le menu latéral** pour accéder à la planification mensuelle.

---

### 📋 Les 7 SADI couverts :
1. THIAROYE
2. RUFISQUE
3. PIKINE
4. GUEDIAWAYE
5. KEUR MASSAR
6. SUD EST
7. NORD

---

### 💡 Fonctionnalités principales

""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 📝 Planification
    - Sélection des jours actifs
    - Calcul automatique des budgets
    - Configuration des ressources (VTO, Bus)
    """)

with col2:
    st.markdown("""
    #### 📊 Suivi
    - Vue mensuelle consolidée
    - Filtres par SADI et période
    - Graphiques de synthèse
    """)

with col3:
    st.markdown("""
    #### 💰 Budget
    - Coûts paramétrables
    - Budget resto par VTO/jour
    - Location bus par jour
    """)

st.markdown("---")

# Informations de contact ou support
st.info("💬 Pour toute question ou assistance, contactez l'équipe de support.")

st.markdown("---")
st.caption("Application développée pour la gestion des planifications SADI - Version 1.0")