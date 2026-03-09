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
# STYLE CSS PERSONNALISÉ
# =============================================================================
st.markdown("""
    <style>
    .concept-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #667eea;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .concept-title {
        font-size: 22px;
        font-weight: bold;
        color: #1f3a5f;
        margin-bottom: 15px;
    }
    .concept-content {
        font-size: 14px;
        line-height: 1.8;
        color: #333;
    }
    .article-box {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 15px 0;
    }
    .article-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .formula-box {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #667eea;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
        font-family: 'Courier New', monospace;
    }
    .warning-box {
        background: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 15px 0;
    }
    .success-box {
        background: #d4edda;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.title("⚙️ Calculateur - Risque Opérationnel")
st.markdown("**Articles 56-62 de la Circulaire 26/G/2006 + NT 02/DSB/2007**")
st.markdown("---")

# =============================================================================
# BARRE LATÉRALE - CHOIX DE L'APPROCHE
# =============================================================================
st.sidebar.header("🎯 Approche de Calcul")

approche = st.sidebar.radio(
    "Sélectionner l'approche",
    [
        "📊 Approche Indicateur de Base (BIA)",
        "📈 Approche Standard (SA)",
        "🔄 Approche Standard Alternative (ASA)"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Autorisation BAM :**
- ✅ BIA : Aucune autorisation requise
- ⚠️ SA : Autorisation préalable requise
- ⚠️ ASA : Autorisation préalable requise
""")

# =============================================================================
# DONNÉES PAR APPROCHE
# =============================================================================
APPROACHES_DATA = {
    "📊 Approche Indicateur de Base (BIA)": {
        "concept": {
            "titre": "Approche Indicateur de Base (BIA)",
            "description": """
            L'approche indicateur de base est la méthode la plus simple pour calculer 
            l'exigence en fonds propres au titre du risque opérationnel. Elle se base 
            exclusivement sur le **Produit Net Bancaire (PNB)** comme indicateur de 
            l'activité de l'établissement.
            
            **Caractéristiques principales :**
            - ✅ Aucune autorisation préalable de Bank Al-Maghrib requise
            - ✅ Formule unique applicable à tous les établissements
            - ✅ Coefficient fixe de 15% appliqué au PNB moyen
            - ✅ Seuls les PNB positifs sont pris en compte
            - ✅ Calcul sur la moyenne des 3 dernières années
            """,
            "formule": "KIB = [Σ(PNB₁...ₙ × α)] / n",
            "variables": {
                "KIB": "Exigence en fonds propres",
                "PNB": "Produit Net Bancaire positif (arrêté fin juin ou fin décembre)",
                "n": "Nombre d'années avec PNB positif sur les 3 dernières années",
                "α": "Coefficient fixe = 15%"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 58",
                "titre": "Calcul selon l'approche indicateur de base",
                "contenu": """
                L'exigence en fonds propres, selon l'approche indicateur de base, 
                est égale à 15% de la moyenne du produit net bancaire, calculée sur 3 ans.
                
                Cette moyenne est déterminée sur la base des trois derniers produits 
                nets bancaires, calculés sur une période d'un an, arrêtés à fin juin 
                ou à fin décembre de chaque exercice.
                
                Seuls les produits nets bancaires positifs sont pris en considération 
                dans le calcul de cette moyenne.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 74",
                "titre": "Formule de calcul - Approche BIA",
                "contenu": """
                L'exigence en fonds propres visée à l'article 58 de la circulaire 
                26/G/2006 est obtenue par application de la formule suivante :
                
                KIB = [Σ(PNB₁...ₙ × α)] / n
                
                Où :
                - KIB = exigence en fonds propres
                - PNB₁...ₙ = produit net bancaire positif (arrêté à fin juin ou à fin décembre)
                - n = nombre d'années pour lesquelles le produit net bancaire est positif 
                      au cours des 3 dernières années
                - α = 15%
                """
            }
        ]
    },
    "📈 Approche Standard (SA)": {
        "concept": {
            "titre": "Approche Standard (SA)",
            "description": """
            L'approche standard est une méthode plus sophistiquée qui ventile les 
            activités de l'établissement en **8 lignes de métier**, chacune avec un 
            coefficient de pondération spécifique (β).
            
            **Caractéristiques principales :**
            - ⚠️ Autorisation préalable de Bank Al-Maghrib requise
            - ✅ 8 lignes de métier avec coefficients β variables (12%-18%)
            - ✅ Prise en compte des PNB positifs et négatifs
            - ✅ Calcul sur la moyenne des 3 dernières années
            - ✅ Meilleure sensibilité au profil de risque
            """,
            "formule": "KTSA = {Σ années 1-3 max[Σ(PNB₁₋₈ × β₁₋₈), 0]} / 3",
            "variables": {
                "KTSA": "Exigence globale en fonds propres",
                "PNB₁₋₈": "Produit Net Bancaire pour chaque ligne de métier",
                "β₁₋₈": "Coefficient de pondération par ligne de métier",
                "3": "Moyenne sur 3 ans"
            },
            "coefficients": {
                "Financement des entreprises": "18%",
                "Activités de marché": "18%",
                "Banque de détail": "12%",
                "Banque commerciale": "15%",
                "Paiement et règlement": "18%",
                "Courtage de détail": "12%",
                "Service d'agence": "15%",
                "Gestion d'actifs": "12%"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 59",
                "titre": "Calcul selon l'approche standard",
                "contenu": """
                Pour l'application de l'approche standard, les établissements sont 
                tenus de ventiler leurs activités en huit lignes de métier.
                
                L'exigence globale en fonds propres est égale à la moyenne sur trois 
                ans des sommes des exigences en fonds propres de toutes les lignes 
                de métier pour chaque année.
                
                Lorsque l'exigence en fonds propres, au titre d'une année donnée, 
                est négative, elle est prise en compte en tant que valeur nulle.
                """
            },
            {
                "numéro": "Article 60",
                "titre": "Lignes de métier et coefficients",
                "contenu": """
                Les lignes de métier et les coefficients de pondération correspondants 
                sont les suivants :
                
                - Financement des entreprises : 18%
                - Activités de marché : 18%
                - Banque de détail : 12%
                - Banque commerciale : 15%
                - Paiement et règlement : 18%
                - Courtage de détail : 12%
                - Service d'agence : 15%
                - Gestion d'actifs : 12%
                """
            },
            {
                "numéro": "Article 61",
                "titre": "Conditions d'utilisation",
                "contenu": """
                L'utilisation de l'approche standard est subordonnée au respect 
                préalable des recommandations édictées par Bank Al-Maghrib en 
                matière de gestion des risques opérationnels.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 75",
                "titre": "Formule de calcul - Approche SA",
                "contenu": """
                L'exigence globale en fonds propres visée à l'article 59 de la 
                circulaire 26/G/2006 est obtenue par application de la formule 
                suivante :
                
                KTSA = {Σ années 1-3 max[Σ(PNB₁₋₈ × β₁₋₈), 0]} / 3
                
                Où :
                - KTSA = exigence globale en fonds propres
                - PNB₁₋₈ = produit net bancaire pour une année donnée pour chacune 
                          des huit lignes de métier
                - β₁₋₈ = coefficient de pondération
                """
            },
            {
                "numéro": "Article 76",
                "titre": "Ventilation des 8 lignes de métier",
                "contenu": """
                La ventilation des 8 lignes de métier est la suivante :
                
                1. Financement des entreprises : Prise ferme, conseil, fusion-acquisition
                2. Activité de marché : Négociation pour compte propre, intermédiation
                3. Banque de détail : Prêts particuliers et TPE, dépôts
                4. Banque commerciale : Prêts PME/GE, dépôts
                5. Paiement et règlement : Opérations de paiement, émission moyens 
                   de paiement
                6. Courtage de détail : Réception/transmission d'ordres
                7. Service d'agence : Garde et administration d'instruments
                8. Gestion d'actifs : Gestion de portefeuille, OPCVM
                """
            },
            {
                "numéro": "Article 77",
                "titre": "Politiques de mapping",
                "contenu": """
                Les établissements doivent élaborer et consigner par écrit des 
                politiques et conditions spécifiques aux fins de la mise en 
                correspondance (mapping) du PNB des lignes de métier.
                
                Principes applicables :
                a) Exhaustivité et exclusivité de la répartition
                b) Activités connexes intégrées à la ligne qu'elles appuient
                c) Affectation à la ligne avec pourcentage le plus élevé si ambiguïté
                d) Possibilité d'utiliser des méthodes de tarification interne
                e) Concordance avec catégories risque crédit et marché
                f) Responsabilité de la Direction Générale
                g) Réexamen indépendant du processus
                """
            }
        ]
    },
    "🔄 Approche Standard Alternative (ASA)": {
        "concept": {
            "titre": "Approche Standard Alternative (ASA)",
            "description": """
            L'approche standard alternative est une méthode hybride qui combine :
            - L'approche standard pour **6 lignes de métier** (avec β = 18%)
            - Une formule basée sur les **encours de crédits** pour les lignes 
              **Banque de Détail** et **Banque Commerciale**
            
            **Caractéristiques principales :**
            - ⚠️ Autorisation préalable de Bank Al-Maghrib requise
            - ✅ ASA applicable uniquement pour Banque de Détail + Banque Commerciale
            - ✅ Basée sur les encours de crédits bruts (ECNI)
            - ✅ Coefficients : β₁ = 15%, m = 0,035
            - ✅ Les 6 autres lignes utilisent SA avec β = 18%
            """,
            "formule": "KNI = β₁ × m × ECNI",
            "variables": {
                "KNI": "Exigence pour lignes Banque de Détail + Banque Commerciale",
                "β₁": "Coefficient fixe = 15%",
                "m": "Facteur multiplicateur = 0,035",
                "ECNI": "Moyenne sur 3 ans des encours de crédits bruts"
            },
            "encours_detail": """
            **Banque de Détail :**
            - Crédits clientèle de détail (Art. 3 NT)
            - Prêts immobiliers résidentiels (Art. 11-H Circulaire)
            
            **Banque Commerciale :**
            - Crédits PME (Art. 4 NT : CA 3-50 MDH)
            - Crédits GE (Art. 5 NT : CA >50 MDH)
            - Crédits souverains, BMD, banques
            - Titres de créance hors portefeuille de négociation
            """
        },
        "articles_g26": [
            {
                "numéro": "Article 62",
                "titre": "Calcul selon l'approche standard alternative",
                "contenu": """
                L'exigence en fonds propres, selon l'approche standard alternative, 
                est égale à la somme des exigences en fonds propres pour les lignes 
                de métiers « banque de détail » et « banque commerciale » et de 
                celles des six autres lignes de métiers.
                
                L'exigence relative aux lignes « banque de détail » et 
                « banque commerciale » est égale à la moyenne, sur trois ans, des 
                encours de crédit bruts pondérés par 15%, multipliée par 0,035.
                
                L'exigence relative aux six autres lignes de métiers est égale à 
                la moyenne, sur trois ans, du produit net bancaire correspondant, 
                affectée d'un coefficient de pondération de 18%.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 78",
                "titre": "Formule de calcul - Approche ASA",
                "contenu": """
                L'exigence en fonds propres relative aux lignes de métiers 
                « banque de détail » et « banque commerciale » est obtenue par 
                application de la formule suivante :
                
                KNI = β₁ × m × ECNI
                
                Où :
                - KNI = exigence en fonds propres (détail + commercial)
                - β₁ = 15%
                - m = 0,035
                - ECNI = moyenne sur trois ans de l'encours total de crédits
                """
            },
            {
                "numéro": "Article 79",
                "titre": "Encours - Banque de détail",
                "contenu": """
                L'encours brut des crédits pour la banque de détail comprend :
                
                - Les crédits accordés à la clientèle de détail telle que définie 
                  à l'article 3 (particuliers et TPE)
                - Les prêts immobiliers à usage résidentiel visés au paragraphe H) 
                  de l'article 11 de la circulaire 26/G/2006
                """
            },
            {
                "numéro": "Article 80",
                "titre": "Encours - Banque commerciale",
                "contenu": """
                L'encours brut des crédits pour la banque commerciale comprend :
                
                - Le total des crédits accordés à la clientèle « PME » et « GE » 
                  (articles 4 et 5 NT)
                - Les entités visées aux paragraphes A), B), C), D) et E) de 
                  l'article 11 de la circulaire 26/G/2006
                - La valeur comptable des titres de créances n'appartenant pas 
                  au portefeuille de négociation
                """
            }
        ]
    }
}

# =============================================================================
# AFFICHAGE DYNAMIQUE SELON L'APPROCHE SÉLECTIONNÉE
# =============================================================================

data = APPROACHES_DATA[approche]

# -----------------------------------------------------------------------------
# SECTION 1 : CONCEPT DE L'APPROCHE (ENCADRÉ)
# -----------------------------------------------------------------------------
st.markdown("### 📚 Concept de l'Approche")

concept = data["concept"]

st.markdown(f"""
    <div class="concept-box">
        <div class="concept-title">{concept['titre']}</div>
        <div class="concept-content">{concept['description']}</div>
    </div>
""", unsafe_allow_html=True)

# Formule
if "formule" in concept:
    st.markdown("#### 🧮 Formule de Calcul")
    st.markdown(f"""
        <div class="formula-box">
            {concept['formule']}
        </div>
    """, unsafe_allow_html=True)
    
    # Variables
    col_var1, col_var2 = st.columns(2)
    with col_var1:
        st.markdown("**Variables :**")
        for var, desc in concept.get("variables", {}).items():
            st.markdown(f"- **{var}** : {desc}")
    
    with col_var2:
        if "coefficients" in concept:
            st.markdown("**Coefficients β par ligne de métier :**")
            df_coeff = pd.DataFrame({
                "Ligne de métier": list(concept["coefficients"].keys()),
                "Coefficient β": list(concept["coefficients"].values())
            })
            st.dataframe(df_coeff, use_container_width=True, hide_index=True)
        elif "encours_detail" in concept:
            st.markdown("**Détail des encours :**")
            st.info(concept["encours_detail"])

st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 2 : ARTICLES RÉGLEMENTAIRES (EXPANDERS)
# -----------------------------------------------------------------------------
st.markdown("### 📖 Articles Réglementaires")

# Circulaire 26/G/2006
with st.expander("📘 Circulaire 26/G/2006", expanded=True):
    for article in data["articles_g26"]:
        st.markdown(f"""
            <div class="article-box">
                <div class="article-header">
                    {article['numéro']} - {article['titre']}
                </div>
                <div style="line-height: 1.8;">
                    {article['contenu']}
                </div>
            </div>
        """, unsafe_allow_html=True)

# Notice Technique NT 02/DSB/2007
with st.expander("📙 Notice Technique NT 02/DSB/2007", expanded=False):
    for article in data["articles_nt"]:
        st.markdown(f"""
            <div class="article-box">
                <div class="article-header">
                    {article['numéro']} - {article['titre']}
                </div>
                <div style="line-height: 1.8;">
                    {article['contenu']}
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 3 : CALCULATEUR PRATIQUE
# -----------------------------------------------------------------------------
st.markdown("### 🧮 Calculateur Pratique")

if "BIA" in approche:
    # =============================================================================
    # CALCULATEUR BIA
    # =============================================================================
    st.markdown("#### Approche Indicateur de Base (BIA)")
    
    st.markdown("##### 📊 Produit Net Bancaire (3 dernières années)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pnb_n1 = st.number_input("PNB Année N-1 (MDH)", min_value=-1000.0, value=500.0, step=10.0, key="bia_n1")
        pnb_n1_positif = st.checkbox("PNB N-1 Positif", value=True if pnb_n1 > 0 else False, key="bia_chk1")
    
    with col2:
        pnb_n2 = st.number_input("PNB Année N-2 (MDH)", min_value=-1000.0, value=450.0, step=10.0, key="bia_n2")
        pnb_n2_positif = st.checkbox("PNB N-2 Positif", value=True if pnb_n2 > 0 else False, key="bia_chk2")
    
    with col3:
        pnb_n3 = st.number_input("PNB Année N-3 (MDH)", min_value=-1000.0, value=400.0, step=10.0, key="bia_n3")
        pnb_n3_positif = st.checkbox("PNB N-3 Positif", value=True if pnb_n3 > 0 else False, key="bia_chk3")
    
    # Calcul
    pnb_values = []
    if pnb_n1_positif and pnb_n1 > 0:
        pnb_values.append(pnb_n1)
    if pnb_n2_positif and pnb_n2 > 0:
        pnb_values.append(pnb_n2)
    if pnb_n3_positif and pnb_n3 > 0:
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
    st.markdown("##### 📈 Résultats du Calcul")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric(
            label="Nombre d'années PNB positif",
            value=n,
            delta=None
        )
    
    with col_res2:
        st.metric(
            label="Moyenne PNB (3 ans)",
            value=f"{moyenne_pnb:.2f} MDH",
            delta=None
        )
    
    with col_res3:
        st.metric(
            label="KIB (Exigence FP)",
            value=f"{kib:.2f} MDH",
            delta=None
        )
    
    # Détails du calcul
    with st.expander("📝 Détails du Calcul"):
        st.write(f"""
        **Formule appliquée :**
        
        KIB = [Σ(PNB × α)] / n
        
        **Application :**
        - PNB positifs : {pnb_values}
        - Somme PNB : {sum(pnb_values):.2f} MDH
        - Nombre d'années (n) : {n}
        - Moyenne PNB : {moyenne_pnb:.2f} MDH
        - Coefficient α : {alpha*100:.0f}%
        - KIB = {moyenne_pnb:.2f} × {alpha*100:.0f}% = **{kib:.2f} MDH**
        
        **Références réglementaires :**
        - Article 58 de la Circulaire 26/G/2006
        - Article 74 de la NT 02/DSB/2007
        """)
    
    # Risque pondéré
    st.markdown("---")
    st.markdown("##### 📊 Impact sur le Ratio de Solvabilité")
    
    risque_pondere = kib * 12.5
    fp_base_min = kib * 0.50
    
    col_rp1, col_rp2 = st.columns(2)
    with col_rp1:
        st.metric("Risque Opérationnel Pondéré", f"{risque_pondere:.2f} MDH")
    with col_rp2:
        st.metric("Fonds Propres de Base (Min 50%)", f"{fp_base_min:.2f} MDH")

elif "Standard (SA)" in approche:
    # =============================================================================
    # CALCULATEUR SA
    # =============================================================================
    st.markdown("#### Approche Standard (SA)")
    
    st.markdown("##### 📊 Produit Net Bancaire par Ligne de Métier")
    st.info("⚠️ Saisir les PNB pour chaque ligne de métier (positifs ou négatifs)")
    
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
    
    # 3 années
    st.markdown("###### Année N-1")
    pnb_n1 = {}
    for ligne, beta in lignes_metier.items():
        pnb_n1[ligne] = st.number_input(f"{ligne} (MDH)", min_value=-500.0, value=100.0, step=10.0, key=f"sa_n1_{ligne}")
    
    st.markdown("###### Année N-2")
    pnb_n2 = {}
    for ligne, beta in lignes_metier.items():
        pnb_n2[ligne] = st.number_input(f"{ligne} (MDH)", min_value=-500.0, value=95.0, step=10.0, key=f"sa_n2_{ligne}")
    
    st.markdown("###### Année N-3")
    pnb_n3 = {}
    for ligne, beta in lignes_metier.items():
        pnb_n3[ligne] = st.number_input(f"{ligne} (MDH)", min_value=-500.0, value=90.0, step=10.0, key=f"sa_n3_{ligne}")
    
    # Calcul par année
    def calcul_annee(pnb_dict, beta_dict):
        total = 0
        for ligne, pnb in pnb_dict.items():
            total += pnb * beta_dict[ligne]
        return max(total, 0)  # Si négatif, pris comme 0
    
    exigence_n1 = calcul_annee(pnb_n1, lignes_metier)
    exigence_n2 = calcul_annee(pnb_n2, lignes_metier)
    exigence_n3 = calcul_annee(pnb_n3, lignes_metier)
    
    ktsa = (exigence_n1 + exigence_n2 + exigence_n3) / 3
    
    st.markdown("---")
    st.markdown("##### 📈 Résultats du Calcul")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric("Exigence Année N-1", f"{exigence_n1:.2f} MDH")
    with col_res2:
        st.metric("Exigence Année N-2", f"{exigence_n2:.2f} MDH")
    with col_res3:
        st.metric("Exigence Année N-3", f"{exigence_n3:.2f} MDH")
    
    st.markdown("---")
    
    col_ktsa1, col_ktsa2 = st.columns(2)
    with col_ktsa1:
        st.metric("KTSA (Moyenne 3 ans)", f"{ktsa:.2f} MDH", delta=None)
    with col_ktsa2:
        risque_pondere = ktsa * 12.5
        st.metric("Risque Opérationnel Pondéré", f"{risque_pondere:.2f} MDH")
    
    # Détails
    with st.expander("📝 Détails du Calcul"):
        st.write(f"""
        **Formule appliquée :**
        
        KTSA = {{Σ années 1-3 max[Σ(PNB₁₋₈ × β₁₋₈), 0]}} / 3
        
        **Application :**
        - Exigence N-1 : {exigence_n1:.2f} MDH
        - Exigence N-2 : {exigence_n2:.2f} MDH
        - Exigence N-3 : {exigence_n3:.2f} MDH
        - KTSA = ({exigence_n1:.2f} + {exigence_n2:.2f} + {exigence_n3:.2f}) / 3 = **{ktsa:.2f} MDH**
        
        **Références réglementaires :**
        - Articles 59-61 de la Circulaire 26/G/2006
        - Articles 75-77 de la NT 02/DSB/2007
        """)

elif "ASA" in approche:
    # =============================================================================
    # CALCULATEUR ASA
    # =============================================================================
    st.markdown("#### Approche Standard Alternative (ASA)")
    
    st.warning("⚠️ Autorisation préalable de Bank Al-Maghrib requise")
    
    # Partie 1 : ASA pour Détail + Commercial
    st.markdown("##### 📊 Encours de Crédits Bruts (Banque de Détail + Banque Commerciale)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ecni_n1 = st.number_input("Encours N-1 (MDH)", min_value=0.0, value=1000.0, step=50.0, key="asa_n1")
    with col2:
        ecni_n2 = st.number_input("Encours N-2 (MDH)", min_value=0.0, value=950.0, step=50.0, key="asa_n2")
    with col3:
        ecni_n3 = st.number_input("Encours N-3 (MDH)", min_value=0.0, value=900.0, step=50.0, key="asa_n3")
    
    moyenne_ecni = (ecni_n1 + ecni_n2 + ecni_n3) / 3
    beta1 = 0.15
    m = 0.035
    kni = beta1 * m * moyenne_ecni
    
    st.markdown("---")
    st.markdown("##### 📊 PNB pour les 6 Autres Lignes de Métier (Approche Standard)")
    
    autres_lignes = {
        "Financement des entreprises": 0.18,
        "Activités de marché": 0.18,
        "Paiement et règlement": 0.18,
        "Courtage de détail": 0.12,
        "Service d'agence": 0.15,
        "Gestion d'actifs": 0.12
    }
    
    pnb_autres = {}
    for ligne, beta in autres_lignes.items():
        pnb_autres[ligne] = st.number_input(f"{ligne} (MDH)", min_value=-500.0, value=100.0, step=10.0, key=f"asa_{ligne}")
    
    exigence_autres = sum([pnb * beta for pnb, beta in zip(pnb_autres.values(), autres_lignes.values())])
    exigence_autres = max(exigence_autres, 0)
    
    # Total ASA
    exigence_asa_totale = kni + exigence_autres
    
    st.markdown("---")
    st.markdown("##### 📈 Résultats du Calcul")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    
    with col_res1:
        st.metric("Moyenne Encours 3 ans", f"{moyenne_ecni:.2f} MDH")
    with col_res2:
        st.metric("KNI (Détail + Commercial)", f"{kni:.2f} MDH")
    with col_res3:
        st.metric("Exigence 6 Autres Lignes", f"{exigence_autres:.2f} MDH")
    
    st.markdown("---")
    
    col_total1, col_total2 = st.columns(2)
    with col_total1:
        st.metric("KNI Total (Exigence ASA)", f"{exigence_asa_totale:.2f} MDH", delta=None)
    with col_total2:
        risque_pondere = exigence_asa_totale * 12.5
        st.metric("Risque Opérationnel Pondéré", f"{risque_pondere:.2f} MDH")
    
    # Détails
    with st.expander("📝 Détails du Calcul"):
        st.write(f"""
        **Formule appliquée :**
        
        KNI = β₁ × m × ECNI
        
        **Application :**
        - Moyenne ECNI : {moyenne_ecni:.2f} MDH
        - β₁ = {beta1*100:.0f}%
        - m = {m}
        - KNI = {beta1*100:.0f}% × {m} × {moyenne_ecni:.2f} = **{kni:.2f} MDH**
        - 6 autres lignes (SA) : **{exigence_autres:.2f} MDH**
        - Total ASA : **{exigence_asa_totale:.2f} MDH**
        
        **Références réglementaires :**
        - Article 62 de la Circulaire 26/G/2006
        - Articles 78-80 de la NT 02/DSB/2007
        """)

# =============================================================================
# EXPORT DES RÉSULTATS
# =============================================================================
st.markdown("---")
st.markdown("### 💾 Exporter les Résultats")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    if st.button("📥 Exporter les Résultats (CSV)", use_container_width=True):
        resultats = {
            "Approche": [approche],
            "Exigence FP (MDH)": [kib if "BIA" in approche else (ktsa if "Standard (SA)" in approche else exigence_asa_totale)],
            "Risque Pondéré (MDH)": [risque_pondere if "risque_pondere" in locals() else "N/A"]
        }
        df_export = pd.DataFrame(resultats)
        csv = df_export.to_csv(index=False, encoding='utf-8-sig').encode('utf-8')
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name=f"risque_operationnel_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col_exp2:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.rerun()

# =============================================================================
# PIED DE PAGE
# =============================================================================
st.markdown("---")
st.info("📌 **Note :** Les calculs sont basés sur la Circulaire 26/G/2006 Articles 56-62 et la NT 02/DSB/2007 Articles 74-80")
