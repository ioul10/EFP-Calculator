import streamlit as st
import pandas as pd
from datetime import datetime

# =============================================================================
# CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Risque de Crédit",
    page_icon="🛡️",
    layout="wide"
)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.title("🛡️ Calculateur - Risque de Crédit")
st.markdown("**Approche Standard - Circulaire 26/G/2006**")
st.markdown("---")

# =============================================================================
# BARRE LATÉRALE - PARAMÈTRES
# =============================================================================
st.sidebar.header("⚙️ Paramètres de Calcul")

st.sidebar.markdown("### Type de Contrepartie")
contrepartie_type = st.sidebar.selectbox(
    "Catégorie",
    [
        "État Marocain (MAD)",
        "Souverain Étranger",
        "Banque Multilatérale de Développement",
        "Établissement de Crédit",
        "Grande Entreprise",
        "PME",
        "Clientèle de Détail",
        "Immobilier Résidentiel",
        "Immobilier Commercial",
        "Créances en Souffrance"
    ]
)

st.sidebar.markdown("### Notation Externe (OEEC)")
notation = st.sidebar.selectbox(
    "Notation Long Terme",
    ["AAA à AA-", "A+ à A-", "BBB+ à BBB-", "BB+ à BB-", "B+ à B-", "< B-", "Non noté"],
    index=2
)

st.sidebar.markdown("### Techniques ARC")
arc_actif = st.sidebar.checkbox("Activer Atténuation du Risque de Crédit", value=False)

# =============================================================================
# TABLEAU DES PONDÉRATIONS
# =============================================================================
st.markdown("### 📊 Tableau des Pondérations par Catégorie")

ponderations_data = {
    "Catégorie": [
        "État Marocain (MAD)", "Souverain AAA-AA-", "Souverain A+-A-", 
        "Souverain BBB+-BBB-", "Souverain BB+-B-", "Souverain <B-",
        "BMD (Liste BAM)", "Banques AAA-AA-", "Banques A+-BBB-",
        "Entreprises AAA-AA-", "Entreprises A+-A-", "Entreprises BBB+-BBB-",
        "Entreprises Non Notées", "Clientèle de Détail", "Immobilier Résidentiel",
        "Immobilier Commercial", "Créances Souffrance (<20% prov)", "Créances Souffrance (>50% prov)"
    ],
    "Pondération (%)": [
        0, 0, 20, 50, 100, 150, 0, 20, 50, 20, 50, 100, 100, 75, 35, 100, 150, 50
    ]
}

df_ponderations = pd.DataFrame(ponderations_data)
st.dataframe(df_ponderations, use_container_width=True, hide_index=True)

# =============================================================================
# CALCULATEUR
# =============================================================================
st.markdown("---")
st.markdown("### 🧮 Simulation de Calcul")

col1, col2, col3 = st.columns(3)

with col1:
    exposition = st.number_input(
        "Montant de l'Exposition (MDH)",
        min_value=0.0,
        value=100.0,
        step=1.0
    )

with col2:
    # Détermination automatique de la pondération
    mapping_ponderation = {
        "État Marocain (MAD)": 0,
        "Souverain Étranger": {"AAA à AA-": 0, "A+ à A-": 20, "BBB+ à BBB-": 50, "BB+ à BB-": 100, "B+ à B-": 100, "< B-": 150, "Non noté": 100},
        "Banque Multilatérale de Développement": 0,
        "Établissement de Crédit": {"AAA à AA-": 20, "A+ à A-": 50, "BBB+ à BBB-": 50, "BB+ à BB-": 100, "B+ à B-": 100, "< B-": 150, "Non noté": 50},
        "Grande Entreprise": {"AAA à AA-": 20, "A+ à A-": 50, "BBB+ à BBB-": 100, "BB+ à BB-": 100, "B+ à B-": 150, "< B-": 150, "Non noté": 100},
        "PME": {"AAA à AA-": 20, "A+ à A-": 50, "BBB+ à BBB-": 100, "BB+ à BB-": 100, "B+ à B-": 150, "< B-": 150, "Non noté": 100},
        "Clientèle de Détail": 75,
        "Immobilier Résidentiel": 35,
        "Immobilier Commercial": 100,
        "Créances en Souffrance": 150
    }
    
    if isinstance(mapping_ponderation[contrepartie_type], dict):
        ponderation = mapping_ponderation[contrepartie_type].get(notation, 100)
    else:
        ponderation = mapping_ponderation[contrepartie_type]
    
    st.metric("Pondération Appliquée", f"{ponderation}%")

with col3:
    hors_bilan = st.checkbox("Engagement de Hors-Bilan")
    if hors_bilan:
        fcec = st.selectbox(
            "Facteur de Conversion (FCEC)",
            [0, 20, 50, 100],
            index=2
        )
        exposition_equivalente = exposition * (fcec / 100)
        st.metric("Exposition Équivalente", f"{exposition_equivalente:.2f} MDH")
    else:
        exposition_equivalente = exposition

# =============================================================================
# RÉSULTATS
# =============================================================================
st.markdown("---")
st.markdown("### 📈 Résultats du Calcul")

risque_pondere = exposition_equivalente * (ponderation / 100)
efp = risque_pondere * 0.08  # 8%
fp_base_min = efp * 0.50  # 50% fonds propres de base

col_res1, col_res2, col_res3, col_res4 = st.columns(4)

with col_res1:
    st.metric(
        label="Risque Pondéré",
        value=f"{risque_pondere:.2f} MDH",
        delta=None
    )

with col_res2:
    st.metric(
        label="Exigence en Fonds Propres",
        value=f"{efp:.2f} MDH",
        delta=None
    )

with col_res3:
    st.metric(
        label="Fonds Propres de Base (Min 50%)",
        value=f"{fp_base_min:.2f} MDH",
        delta=None
    )

with col_res4:
    st.metric(
        label="Impact sur Ratio de Solvabilité",
        value=f"{(efp / exposition * 100):.2f}%",
        delta=None
    )

# =============================================================================
# DÉTAILS DU CALCUL
# =============================================================================
with st.expander("📝 Détails du Calcul"):
    st.write(f"""
    **Formule appliquée :**
    
    1. Risque Pondéré = Exposition × Pondération
       - {exposition_equivalente:.2f} MDH × {ponderation}% = {risque_pondere:.2f} MDH
    
    2. Exigence en Fonds Propres = Risque Pondéré × 8%
       - {risque_pondere:.2f} MDH × 8% = {efp:.2f} MDH
    
    3. Fonds Propres de Base (Min 50%) = EFP × 50%
       - {efp:.2f} MDH × 50% = {fp_base_min:.2f} MDH
    
    **Références réglementaires :**
    - Article 11 de la Circulaire 26/G/2006 (Pondérations)
    - Article 6 de la Circulaire 26/G/2006 (Couverture FP)
    - Articles 26-53 de la NT 02/DSB/2007 (Techniques ARC)
    """)

# =============================================================================
# EXPORT
# =============================================================================
st.markdown("---")
col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    if st.button("📥 Exporter les Résultats (CSV)", use_container_width=True):
        resultats = {
            "Paramètre": ["Exposition", "Pondération", "Risque Pondéré", "EFP", "FP Base Min"],
            "Valeur": [exposition, f"{ponderation}%", f"{risque_pondere:.2f} MDH", f"{efp:.2f} MDH", f"{fp_base_min:.2f} MDH"]
        }
        df_export = pd.DataFrame(resultats)
        csv = df_export.to_csv(index=False, encoding='utf-8-sig').encode('utf-8')
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name=f"risque_credit_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col_exp2:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.rerun()
