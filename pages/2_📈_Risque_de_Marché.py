import streamlit as st
import pandas as pd
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Risque de Marché",
    page_icon="📈",
    layout="wide"
)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.title("📈 Calculateur - Risque de Marché")
st.markdown("**Article 54 de la Circulaire 26/G/2006**")
st.markdown("---")

# =============================================================================
# NAVIGATION PAR TYPE DE RISQUE
# =============================================================================
st.sidebar.header("🎯 Type de Risque")
risque_type = st.sidebar.radio(
    "Sélectionner",
    ["Taux d'Intérêt", "Titres de Propriété", "Change", "Produits de Base", "Options"]
)

# =============================================================================
# RISQUE DE TAUX D'INTÉRÊT
# =============================================================================
if risque_type == "Taux d'Intérêt":
    st.markdown("### 🏦 Risque de Taux d'Intérêt")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risque Spécifique**")
        position_nette = st.number_input("Position Nette Titres de Créance (MDH)", value=100.0)
        notation_emission = st.selectbox("Notation de l'Émission", ["AAA à AA-", "A+ à BBB-", "BB+ à B-", "< B-", "Non noté"])
        
        mapping_specifique = {"AAA à AA-": 0, "A+ à BBB-": 1.6, "BB+ à B-": 8, "< B-": 12, "Non noté": 8}
        ponderation_specifique = mapping_specifique.get(notation_emission, 8)
        efp_specifique = abs(position_nette) * (ponderation_specifique / 100)
        
        st.metric("EFP Risque Spécifique", f"{efp_specifique:.2f} MDH")
    
    with col2:
        st.markdown("**Risque Général (Méthode Échéancier)**")
        position_zone1 = st.number_input("Zone 1 (0-1 an) (MDH)", value=50.0)
        position_zone2 = st.number_input("Zone 2 (1-4 ans) (MDH)", value=30.0)
        position_zone3 = st.number_input("Zone 3 (>4 ans) (MDH)", value=20.0)
        
        efp_general = (position_zone1 * 0.40 + position_zone2 * 0.30 + position_zone3 * 0.30) * 0.08
        st.metric("EFP Risque Général", f"{efp_general:.2f} MDH")
    
    efp_totale_taux = efp_specifique + efp_general
    st.markdown(f"### 💰 Exigence Totale Taux : **{efp_totale_taux:.2f} MDH**")

# =============================================================================
# RISQUE SUR TITRES DE PROPRIÉTÉ
# =============================================================================
elif risque_type == "Titres de Propriété":
    st.markdown("### 📊 Risque sur Titres de Propriété")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risque Spécifique**")
        position_brute = st.number_input("Position Brute Titres (MDH)", value=100.0)
        portefeuille_diversifie = st.checkbox("Portefeuille Liquide et Diversifié")
        
        if portefeuille_diversifie:
            ponderation_specifique = 4
        else:
            ponderation_specifique = 8
        
        efp_specifique = position_brute * (ponderation_specifique / 100)
        st.metric("EFP Risque Spécifique", f"{efp_specifique:.2f} MDH")
    
    with col2:
        st.markdown("**Risque Général**")
        position_nette_globale = st.number_input("Position Nette Globale (MDH)", value=80.0)
        efp_general = abs(position_nette_globale) * 0.08
        st.metric("EFP Risque Général", f"{efp_general:.2f} MDH")
    
    efp_totale_titres = efp_specifique + efp_general
    st.markdown(f"### 💰 Exigence Totale Titres : **{efp_totale_titres:.2f} MDH**")

# =============================================================================
# RISQUE DE CHANGE
# =============================================================================
elif risque_type == "Change":
    st.markdown("### 💱 Risque de Change")
    
    col1, col2 = st.columns(2)
    
    with col1:
        positions_longues = st.number_input("Total Positions Longues (MDH)", value=100.0)
    
    with col2:
        positions_courtes = st.number_input("Total Positions Courtes (MDH)", value=80.0)
    
    position_or = st.number_input("Position Nette Or (MDH)", value=0.0)
    
    efp_change = 0.08 * (max(positions_longues, positions_courtes) + abs(position_or))
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Position Nette Maximale", f"{max(positions_longues, positions_courtes):.2f} MDH")
    with col_res2:
        st.metric("EFP Risque de Change", f"{efp_change:.2f} MDH")

# =============================================================================
# RISQUE SUR PRODUITS DE BASE
# =============================================================================
elif risque_type == "Produits de Base":
    st.markdown("### 🛢️ Risque sur Produits de Base")
    
    methode = st.selectbox("Méthode de Calcul", ["Tableau d'Échéances", "Approche Simplifiée"])
    
    if methode == "Approche Simplifiée":
        col1, col2 = st.columns(2)
        with col1:
            position_nette = st.number_input("Position Nette (MDH)", value=100.0)
        with col2:
            position_brute = st.number_input("Position Brute (MDH)", value=150.0)
        
        efp_produits = (position_nette * 0.15) + (position_brute * 0.03)
        st.metric("EFP Produits de Base", f"{efp_produits:.2f} MDH")
    else:
        st.info("Méthode Tableau d'Échéances : Fonctionnalité en développement")

# =============================================================================
# RISQUE SUR OPTIONS
# =============================================================================
elif risque_type == "Options":
    st.markdown("### 📋 Risque sur Options (Méthode Delta-Plus)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta = st.number_input("Delta", value=0.6, step=0.1)
        valeur_sous_jacent = st.number_input("Valeur Marché Sous-jacent (MDH)", value=100.0)
    
    with col2:
        gamma = st.number_input("Gamma", value=0.02, step=0.01)
        variation_sous_jacent = st.number_input("Variation Sous-jacent (%)", value=8.0)
    
    with col3:
        vega = st.number_input("Vega", value=0.15, step=0.01)
        volatibilite_implicite = st.number_input("Volatilité Implicite (%)", value=20.0)
    
    position_equivalente = valeur_sous_jacent * delta
    risque_gamma = 0.5 * gamma * (valeur_sous_jacent * variation_sous_jacent / 100) ** 2
    risque_vega = vega * (volatibilite_implicite / 100 * 0.25)
    
    efp_options = abs(position_equivalente * 0.08) + abs(risque_gamma) + abs(risque_vega)
    
    st.metric("EFP Totale Options", f"{efp_options:.2f} MDH")

# =============================================================================
# RÉCAPITULATIF
# =============================================================================
st.markdown("---")
st.markdown("### 📊 Récapitulatif par Catégorie de Risque")

recap_data = {
    "Type de Risque": ["Taux d'Intérêt", "Titres de Propriété", "Change", "Produits de Base", "Options"],
    "EFP (MDH)": ["À calculer", "À calculer", "À calculer", "À calculer", "À calculer"],
    "Coefficient": ["8%", "8%", "8%", "15% + 3%", "Delta-Plus"]
}

st.dataframe(pd.DataFrame(recap_data), use_container_width=True, hide_index=True)

# =============================================================================
# PIED DE PAGE
# =============================================================================
st.markdown("---")
st.info("📌 **Note :** Les calculs sont basés sur la Circulaire 26/G/2006 Article 54 et la NT 02/DSB/2007 Articles 55-73")
