import streamlit as st
import pandas as pd
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Risque Opérationnel",
    page_icon="⚙️",
    layout="wide"
)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.title("⚙️ Calculateur - Risque Opérationnel")
st.markdown("**Articles 56-62 de la Circulaire 26/G/2006**")
st.markdown("---")

# =============================================================================
# CHOIX DE L'APPROCHE
# =============================================================================
st.sidebar.header("🎯 Approche de Calcul")
approche = st.sidebar.radio(
    "Sélectionner",
    ["Approche Indicateur de Base (BIA)", "Approche Standard (SA)", "Approche Standard Alternative (ASA)"]
)

# =============================================================================
# APPROCHE INDICATEUR DE BASE (BIA)
# =============================================================================
if approche == "Approche Indicateur de Base (BIA)":
    st.markdown("### 📊 Approche Indicateur de Base (BIA)")
    st.info("**Article 58 de la Circulaire 26/G/2006** - Aucune autorisation BAM requise")
    
    st.markdown("#### Produit Net Bancaire (3 dernières années)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pnb_n1 = st.number_input("PNB Année N-1 (MDH)", min_value=0.0, value=500.0)
        pnb_n1_positif = st.checkbox("PNB N-1 Positif", value=True)
    
    with col2:
        pnb_n2 = st.number_input("PNB Année N-2 (MDH)", min_value=0.0, value=450.0)
        pnb_n2_positif = st.checkbox("PNB N-2 Positif", value=True)
    
    with col3:
        pnb_n3 = st.number_input("PNB Année N-3 (MDH)", min_value=0.0, value=400.0)
        pnb_n3_positif = st.checkbox("PNB N-3 Positif", value=True)
    
    # Calcul
    pnb_values = []
    if pnb_n1_positif:
        pnb_values.append(pnb_n1)
    if pnb_n2_positif:
        pnb_values.append(pnb_n2)
    if pnb_n3_positif:
        pnb_values.append(pnb_n3)
    
    n = len(pnb_values)
    alpha = 0.15
    
    if n > 0:
        moyenne_pnb = sum(pnb_values) / n
        kib = moyenne_pnb * alpha
    else:
        moyenne_pnb = 0
        kib = 0
    
    st.markdown("---")
    st.markdown("### 📈 Résultats")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric("Nombre d'années PNB positif", n)
    
    with col_res2:
        st.metric("Moyenne PNB", f"{moyenne_pnb:.2f} MDH")
    
    with col_res3:
        st.metric("KIB (Exigence FP)", f"{kib:.2f} MDH")
    
    # Formule
    with st.expander("📝 Formule de Calcul"):
        st.write(f"""
        **KIB = [Σ(PNB × α)] / n**
        
        Où :
        - KIB = exigence en fonds propres
        - PNB = produit net bancaire positif
        - α = 15%
        - n = nombre d'années avec PNB positif sur 3 ans
        
        Application :
        - KIB = [{moyenne_pnb:.2f} × 15%] / {n}
        - KIB = {kib:.2f} MDH
        """)

# =============================================================================
# APPROCHE STANDARD (SA)
# =============================================================================
elif approche == "Approche Standard (SA)":
    st.markdown("### 📊 Approche Standard (SA)")
    st.warning("**Article 59-61 de la Circulaire 26/G/2006** - Autorisation préalable BAM requise")
    
    st.markdown("#### Produit Net Bancaire par Ligne de Métier")
    
    lignes_metier = {
        "Financement des entreprises": 0.18,
        "Activités de marché": 0.18,
        "Banque de détail": 0.12,
        "Banque commerciale": 0.15,
        "Paiement et règlement": 0.18,
        "Courtage de détail": 0.12,
        "Service d'agence": 0.15,
        "Gestion d'actifs": 0.12
    }
    
    pnb_par_ligne = {}
    
    for ligne, beta in lignes_metier.items():
        pnb_par_ligne[ligne] = st.number_input(f"{ligne} (MDH)", min_value=0.0, value=100.0, key=ligne)
    
    # Calcul
    total_exigence = 0
    resultats = []
    
    for ligne, beta in lignes_metier.items():
        pnb = pnb_par_ligne[ligne]
        exigence_ligne = pnb * beta
        total_exigence += exigence_ligne
        resultats.append({
            "Ligne de Métier": ligne,
            "PNB (MDH)": pnb,
            "Coefficient β": f"{beta*100:.0f}%",
            "Exigence (MDH)": f"{exigence_ligne:.2f}"
        })
    
    ktsa = total_exigence / 3  # Moyenne sur 3 ans (simplifié ici)
    
    st.markdown("---")
    st.markdown("### 📈 Résultats")
    
    df_resultats = pd.DataFrame(resultats)
    st.dataframe(df_resultats, use_container_width=True, hide_index=True)
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Somme des Exigences Annuelles", f"{total_exigence:.2f} MDH")
    with col_res2:
        st.metric("KTSA (Moyenne 3 ans)", f"{ktsa:.2f} MDH")

# =============================================================================
# APPROCHE STANDARD ALTERNATIVE (ASA)
# =============================================================================
elif approche == "Approche Standard Alternative (ASA)":
    st.markdown("### 📊 Approche Standard Alternative (ASA)")
    st.warning("**Article 62 de la Circulaire 26/G/2006** - Autorisation préalable BAM requise")
    
    st.info("Applicable uniquement pour les lignes : **Banque de Détail** et **Banque Commerciale**")
    
    st.markdown("#### Encours de Crédits Bruts (3 dernières années)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ecni_n1 = st.number_input("Encours N-1 (MDH)", min_value=0.0, value=1000.0)
    
    with col2:
        ecni_n2 = st.number_input("Encours N-2 (MDH)", min_value=0.0, value=950.0)
    
    with col3:
        ecni_n3 = st.number_input("Encours N-3 (MDH)", min_value=0.0, value=900.0)
    
    # Calcul
    moyenne_ecni = (ecni_n1 + ecni_n2 + ecni_n3) / 3
    beta1 = 0.15
    m = 0.035
    
    kni = beta1 * m * moyenne_ecni
    
    st.markdown("---")
    st.markdown("### 📈 Résultats")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric("Moyenne Encours 3 ans", f"{moyenne_ecni:.2f} MDH")
    
    with col_res2:
        st.metric("β₁ × m", f"{beta1 * m:.4f}")
    
    with col_res3:
        st.metric("KNI (Exigence FP)", f"{kni:.2f} MDH")
    
    with st.expander("📝 Formule de Calcul"):
        st.write(f"""
        **KNI = β₁ × m × ECNI**
        
        Où :
        - KNI = exigence en fonds propres (détail + commercial)
        - β₁ = 15%
        - m = 0,035
        - ECNI = moyenne sur 3 ans des encours de crédits bruts
        
        Application :
        - KNI = 15% × 0,035 × {moyenne_ecni:.2f}
        - KNI = {kni:.2f} MDH
        
        **Pour les 6 autres lignes de métier :**
        - Appliquer l'approche standard avec β = 18%
        """)

# =============================================================================
# TABLEAU RÉCAPITULATIF DES COEFFICIENTS
# =============================================================================
st.markdown("---")
st.markdown("### 📚 Coefficients par Ligne de Métier")

coeff_data = {
    "Ligne de Métier": list(lignes_metier.keys()),
    "Coefficient β": [f"{v*100:.0f}%" for v in lignes_metier.values()],
    "ASA Applicable": ["❌", "❌", "✅", "✅", "❌", "❌", "❌", "❌"]
}

st.dataframe(pd.DataFrame(coeff_data), use_container_width=True, hide_index=True)

# =============================================================================
# PIED DE PAGE
# =============================================================================
st.markdown("---")
st.info("📌 **Note :** Les calculs sont basés sur la Circulaire 26/G/2006 Articles 56-62 et la NT 02/DSB/2007 Articles 74-80")
