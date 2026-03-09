import streamlit as st
from datetime import datetime

# =============================================================================
# CONFIGURATION DE LA PAGE
# =============================================================================
st.set_page_config(
    page_title="EFP Calculator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# STYLE CSS PERSONNALISÉ
# =============================================================================
st.markdown("""
    <style>
    .main-header {
        font-size: 48px;
        font-weight: bold;
        color: #1f3a5f;
        text-align: center;
        margin-bottom: 20px;
    }
    .sub-header {
        font-size: 20px;
        color: #666;
        text-align: center;
        margin-bottom: 40px;
    }
    .card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    .card:hover {
        transform: translateY(-5px);
    }
    .card-credit {
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
    }
    .card-market {
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
    }
    .card-operational {
        background: linear-gradient(135deg, #9c27b0 0%, #7b1fa2 100%);
    }
    .metric-box {
        background: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.markdown('<p class="main-header">🏦 EFP Calculator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Calculateur d\'Exigences en Fonds Propres - Circulaire 26/G/2006</p>', unsafe_allow_html=True)
st.markdown("---")

# =============================================================================
# PRÉSENTATION
# =============================================================================
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="card card-credit">
            <h2>🛡️ Risque de Crédit</h2>
            <p>Calcul selon l'approche standard avec pondérations OEEC</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="card card-market">
            <h2>📈 Risque de Marché</h2>
            <p>Taux, titres, change, produits de base et options</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="card card-operational">
            <h2>⚙️ Risque Opérationnel</h2>
            <p>BIA, SA et ASA selon les lignes de métier</p>
        </div>
    """, unsafe_allow_html=True)

# =============================================================================
# INFORMATIONS RÉGLEMENTAIRES
# =============================================================================
st.markdown("---")
st.markdown("### 📚 Cadre Réglementaire")

col_info1, col_info2, col_info3 = st.columns(3)

with col_info1:
    st.info("""
    **Circulaire 26/G/2006**
    
    Bank Al-Maghrib
    
    Relative au calcul des exigences en fonds propres selon l'approche standard
    """)

with col_info2:
    st.info("""
    **Notice Technique NT 02/DSB/2007**
    
    Modalités d'application de la circulaire 26/G/2006
    
    13 avril 2007
    """)

with col_info3:
    st.info("""
    **Ratio de Solvabilité**
    
    Fonds Propres / Risques Pondérés ≥ 10%
    
    Mise à jour : Semestrielle
    """)

# =============================================================================
# MÉTRIQUES CLÉS
# =============================================================================
st.markdown("---")
st.markdown("### 📊 Métriques de Référence")

col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(
        label="Ratio Minimum de Solvabilité",
        value="10%",
        delta=None
    )

with col_m2:
    st.metric(
        label="Coefficient Risque de Crédit",
        value="8%",
        delta=None
    )

with col_m3:
    st.metric(
        label="Coefficient Risque de Marché",
        value="8%",
        delta=None
    )

with col_m4:
    st.metric(
        label="Coefficient Risque Opérationnel (BIA)",
        value="15%",
        delta=None
    )

# =============================================================================
# NAVIGATION RAPIDE
# =============================================================================
st.markdown("---")
st.markdown("### 🚀 Accès Rapide aux Calculateurs")

col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("🛡️ Calculer Risque de Crédit", use_container_width=True, type="primary"):
        st.switch_page("pages/1_💳_Risque_de_Crédit.py")

with col_nav2:
    if st.button("📈 Calculer Risque de Marché", use_container_width=True, type="primary"):
        st.switch_page("pages/2_📈_Risque_de_Marché.py")

with col_nav3:
    if st.button("⚙️ Calculer Risque Opérationnel", use_container_width=True, type="primary"):
        st.switch_page("pages/3_⚙️_Risque_Opérationnel.py")

# =============================================================================
# PIED DE PAGE
# =============================================================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #999; font-size: 12px; padding: 20px;">
        <p><strong>MASI Futures Pro v0.2 Beta</strong></p>
        <p>Développé avec Streamlit | {datetime.now().strftime("%Y")} | Déployé sur GitHub</p>
        <p>Conforme à la Circulaire 26/G/2006 de Bank Al-Maghrib</p>
    </div>
""", unsafe_allow_html=True)
