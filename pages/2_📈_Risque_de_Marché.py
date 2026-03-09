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
# STYLE CSS PERSONNALISÉ
# =============================================================================
st.markdown("""
    <style>
    .concept-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #ff9800;
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
        background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%);
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
        border: 2px solid #ff9800;
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
    .risk-type-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff9800;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
    }
    .risk-type-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.title("📈 Calculateur - Risque de Marché")
st.markdown("**Article 54 de la Circulaire 26/G/2006 + Articles 55-73 de la NT 02/DSB/2007**")
st.markdown("---")

# =============================================================================
# BARRE LATÉRALE - CHOIX DU TYPE DE RISQUE
# =============================================================================
st.sidebar.header("🎯 Type de Risque de Marché")

risque_type = st.sidebar.radio(
    "Sélectionner le type de risque",
    [
        "🏦 Taux d'Intérêt",
        "📊 Titres de Propriété",
        "💱 Change",
        "🛢️ Produits de Base",
        "📋 Options (Delta-Plus)",
        "🔄 Dérivés de Crédit"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Seuils d'assujettissement (Art. 69 NT) :**
- Portefeuille > 5% du bilan OU
- Portefeuille > 6% du bilan (max) OU
- Positions moyennes > 15 MDH OU
- Positions max > 20 MDH
""")

# =============================================================================
# DONNÉES PAR TYPE DE RISQUE
# =============================================================================
RISK_TYPES_DATA = {
    "🏦 Taux d'Intérêt": {
        "concept": {
            "titre": "Risque de Taux d'Intérêt",
            "description": """
            Le risque de taux d'intérêt correspond aux pertes potentielles liées aux 
            variations des taux d'intérêt sur les positions du portefeuille de négociation.
            
            **Composantes :**
            - ✅ Risque Spécifique : Variation de prix liée à l'émetteur
            - ✅ Risque Général : Variation liée au marché global
            - ✅ Calcul séparé par devise : MAD, EUR, USD
            
            **Méthodes de calcul :**
            - Méthode de l'Échéancier (standard)
            - Méthode de la Duration (sur autorisation BAM)
            """,
            "formule": "EFP = Risque Spécifique + Risque Général",
            "variables": {
                "EFP": "Exigence en Fonds Propres totale",
                "Risque Spécifique": "Σ(|Position Nette| × Pondération selon notation)",
                "Risque Général": "Calcul selon méthode échéancier ou duration",
                "Devises": "Calcul séparé pour MAD, EUR, USD"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 54 - Section I",
                "titre": "Risque de Taux d'Intérêt - Circulaire 26/G/2006",
                "contenu": """
                L'exigence en fonds propres relative au risque de taux d'intérêt 
                correspond à la somme des exigences en fonds propres requises au 
                titre du risque spécifique et du risque général.
                
                Cette exigence est calculée, séparément, pour chacune des monnaies 
                suivantes : le dirham, l'euro et le dollar.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 70 - Section II",
                "titre": "Calcul Détaillé - NT 02/DSB/2007",
                "contenu": """
                A) Risque Spécifique :
                - 0% : État marocain, BAM, BRI, FMI, BCE (MAD)
                - 4% : Collectivités locales (MAD), OPCVM taux
                - 0,25%-12% : Selon notation et échéance résiduelle
                
                B) Risque Général - Méthode Échéancier :
                - 3 zones d'échéances (Zone 1: 0-1 an, Zone 2: 1-4 ans, Zone 3: >4 ans)
                - Compensation intra-fourchette, intra-zone, inter-zones
                - Pondérations : 10%, 30%, 40%, 100% selon compensation
                
                C) Méthode Duration :
                - Duration modifiée = Duration / (1 + r)
                - Même logique de compensation que méthode échéancier
                """
            },
            {
                "numéro": "Article 63-68",
                "titre": "Éligibilité et Évaluation - NT 02/DSB/2007",
                "contenu": """
                Conditions d'éligibilité au portefeuille de négociation :
                - Stratégie documentée et approuvée
                - Gestion active avec limites
                - Évaluation quotidienne (prix marché ou modèle)
                - Vérification indépendante mensuelle des prix
                - Séparation claire portefeuille négociation/bancaire
                """
            }
        ],
        "tables": {
            "Pondérations Risque Spécifique": {
                "headers": ["Nature Émission", "Notation", "Échéance", "Pondération"],
                "data": [
                    ["État Marocain (MAD)", "-", "Toutes", "0%"],
                    ["Souverain AAA-AA-", "AAA à AA-", "Toutes", "0%"],
                    ["Souverain A+-BBB-", "A+ à BBB-", "≤ 6 mois", "0,25%"],
                    ["Souverain A+-BBB-", "A+ à BBB-", "6-24 mois", "1,00%"],
                    ["Souverain A+-BBB-", "A+ à BBB-", "> 24 mois", "1,60%"],
                    ["Souverain BB+-B-", "BB+ à B-", "Toutes", "8,00%"],
                    ["Souverain < B-", "< B-", "Toutes", "12,00%"],
                    ["Qualifiées", "≥ BBB-", "≤ 6 mois", "0,25%"],
                    ["Qualifiées", "≥ BBB-", "6-24 mois", "1,00%"],
                    ["Qualifiées", "≥ BBB-", "> 24 mois", "1,60%"],
                    ["Autres", "BB+ à BB-", "Toutes", "8,00%"],
                    ["Autres", "< BB-", "Toutes", "12,00%"],
                    ["Autres", "Non noté", "Toutes", "8,00%"]
                ]
            },
            "Zones Échéancier": {
                "headers": ["Zone", "Fourchette Coupon ≥3%", "Fourchette Coupon <3%", "Pondération %", "Variation Taux %"],
                "data": [
                    ["Zone 1", "0-1 mois", "0-1 mois", "0,00", "1,00"],
                    ["Zone 1", "1-3 mois", "1-3 mois", "0,20", "1,00"],
                    ["Zone 1", "3-6 mois", "3-6 mois", "0,70", "1,00"],
                    ["Zone 1", "6-12 mois", "6-12 mois", "0,70", "1,00"],
                    ["Zone 2", "1-2 ans", "1,0-1,9 ans", "1,25", "0,90"],
                    ["Zone 2", "2-3 ans", "1,9-2,8 ans", "1,75", "0,80"],
                    ["Zone 2", "3-4 ans", "2,8-3,6 ans", "2,25", "0,75"],
                    ["Zone 2", "4-5 ans", "3,6-4,3 ans", "2,75", "0,75"],
                    ["Zone 3", "5-7 ans", "4,3-5,7 ans", "3,25", "0,70"],
                    ["Zone 3", "7-10 ans", "5,7-7,3 ans", "3,75", "0,65"],
                    ["Zone 3", "10-15 ans", "7,3-9,3 ans", "4,50", "0,60"],
                    ["Zone 3", "15-20 ans", "9,3-10,6 ans", "5,25", "0,60"],
                    ["Zone 3", ">20 ans", "10,6-12 ans", "6,00", "0,60"],
                    ["Zone 3", ">20 ans", "12-20 ans", "8,00", "0,60"],
                    ["Zone 3", ">20 ans", ">20 ans", "12,50", "0,60"]
                ]
            }
        }
    },
    "📊 Titres de Propriété": {
        "concept": {
            "titre": "Risque sur Titres de Propriété",
            "description": """
            Le risque sur titres de propriété correspond aux pertes potentielles liées 
            aux variations de prix des actions et instruments assimilés.
            
            **Composantes :**
            - ✅ Risque Spécifique : Facteur lié à l'émetteur
            - ✅ Risque Général : Évolution générale du marché
            
            **Conditions portefeuille liquide et diversifié :**
            - Titres dans indices boursiers (Annexe 1 NT)
            - Aucune position > 5% du portefeuille (ou 10% si total < 50%)
            """,
            "formule": "EFP = Risque Spécifique + Risque Général",
            "variables": {
                "EFP": "Exigence en Fonds Propres totale",
                "Risque Spécifique": "8% (ou 4% si liquide/diversifié) × Position Brute",
                "Risque Général": "8% × Position Nette Globale",
                "OPCVM Actions": "2% × Position Brute"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 54 - Section II",
                "titre": "Risque Titres de Propriété - Circulaire 26/G/2006",
                "contenu": """
                L'exigence en fonds propres relative aux titres de propriété 
                correspond à la somme des exigences en fonds propres requises au 
                titre du risque spécifique et du risque général.
                
                Le risque spécifique est de 8% de la position brute (ou 4% si 
                portefeuille liquide et diversifié).
                
                Le risque général est de 8% de la position nette globale.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 70 - Section III",
                "titre": "Calcul Détaillé - NT 02/DSB/2007",
                "contenu": """
                A) Risque Spécifique :
                - 8% : Position brute standard
                - 4% : Portefeuille liquide et diversifié
                - 2% : Parts OPCVM actions, contrats indices majeurs
                - 4% : Indices sectoriels insuffisamment diversifiés
                
                B) Risque Général :
                - 8% × Position Nette Globale
                - Calcul séparé par marché national
                - Conversion au taux de change au comptant BAM
                
                C) Indices Boursiers (Annexe 1 NT) :
                MASI, MADEX, CAC 40, FTSE 100, S&P 500, DAX, Nikkei 225, etc.
                """
            }
        ],
        "tables": {
            "Pondérations Titres": {
                "headers": ["Type de Position", "Condition", "Coefficient"],
                "data": [
                    ["Titres de propriété", "Portefeuille standard", "8%"],
                    ["Titres de propriété", "Liquide et diversifié", "4%"],
                    ["Parts OPCVM actions", "-", "2%"],
                    ["Contrats indices majeurs", "Liste Annexe 1", "2%"],
                    ["Contrats indices sectoriels", "Insuffisamment diversifiés", "4%"],
                    ["Arbitrage instruments à terme", "Par branche", "2%"]
                ]
            }
        }
    },
    "💱 Change": {
        "concept": {
            "titre": "Risque de Change",
            "description": """
            Le risque de change correspond aux pertes potentielles liées aux 
            variations des taux de change sur l'ensemble des positions en devises.
            
            **Caractéristiques :**
            - ✅ S'applique à TOUS les éléments (bilan + hors-bilan)
            - ✅ Inclut ou non le portefeuille de négociation
            - ✅ Position or calculée séparément
            
            **Seuil de calcul :**
            - Positions de change nettes > 2% des fonds propres
            """,
            "formule": "EFP = 8% × [max(Σ|Long|, Σ|Court|) + |Position Or|]",
            "variables": {
                "EFP": "Exigence en Fonds Propres",
                "Σ|Long|": "Total des positions nettes longues en devises",
                "Σ|Court|": "Total des positions nettes courtes en devises",
                "Position Or": "Valeur absolue de la position nette sur or"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 54 - Section III",
                "titre": "Risque de Change - Circulaire 26/G/2006",
                "contenu": """
                L'exigence en fonds propres au titre du risque de change est égale 
                à 8% de la somme des deux éléments suivants :
                
                1) Le montant le plus élevé du total des positions nettes courtes 
                   ou du total des positions nettes longues en devises
                2) La valeur absolue de la position nette sur or
                """
            },
            {
                "numéro": "Article 52",
                "titre": "Seuil de Calcul - Circulaire 26/G/2006",
                "contenu": """
                Les établissements sont tenus de procéder au calcul d'une exigence 
                en fonds propres au titre du risque de change, sur base individuelle 
                et/ou sur base consolidée, dès lors que la somme de leurs positions 
                de change nettes excède 2% de leurs fonds propres.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 70 - Section IV",
                "titre": "Calcul Détaillé - NT 02/DSB/2007",
                "contenu": """
                Étape 1 : Calcul de la Position Nette
                - Position nette par devise selon circulaire 16/G/2005
                - Position sur or calculée séparément
                - Conversion en MAD au taux BAM
                
                Étape 2 : Calcul de l'Exigence
                - 8% × [max(Σ|Long|, Σ|Court|) + |Position Or|]
                - Toutes positions nettes converties quotidiennement en MAD
                """
            },
            {
                "numéro": "Article 73",
                "titre": "Base Consolidée - NT 02/DSB/2007",
                "contenu": """
                Pour le calcul sur base consolidée, lorsque la consolidation 
                technique est difficile pour certaines positions de devises 
                négligeables, la limite interne pour chaque devise est à ajouter 
                à la position ouverte nette dans chaque devise.
                """
            }
        ],
        "tables": {}
    },
    "🛢️ Produits de Base": {
        "concept": {
            "titre": "Risque sur Produits de Base",
            "description": """
            Le risque sur produits de base correspond aux pertes potentielles liées 
            aux variations de prix des matières premières.
            
            **Catégories couvertes :**
            - ✅ Métaux de base
            - ✅ Métaux précieux (sauf or)
            - ✅ Produits agricoles
            - ✅ Produits énergétiques
            
            **Méthodes de calcul :**
            - Méthode Tableau d'Échéances (standard)
            - Méthode Simplifiée (volumes négligeables)
            """,
            "formule": "EFP = 1,5% × Compensées + 0,6% × Reports + 15% × Résiduelles",
            "variables": {
                "EFP": "Exigence en Fonds Propres",
                "Compensées": "Positions compensées intra-fourchette",
                "Reports": "Positions reportées (0,6% par report)",
                "Résiduelles": "Positions résiduelles non compensées"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 54 - Section IV",
                "titre": "Risque Produits de Base - Circulaire 26/G/2006",
                "contenu": """
                L'exigence en fonds propres sur les positions du bilan et du 
                hors-bilan relatives aux produits de base est calculée selon :
                
                A) Méthode Tableau d'Échéances :
                - 1,5% × positions compensées intra-fourchette
                - 0,6% × positions reportées par fourchette
                - 15% × position résiduelle non compensée
                
                B) Méthode Simplifiée :
                - 15% × position nette
                - 3% × positions brutes
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 70 - Section V",
                "titre": "Calcul Détaillé - NT 02/DSB/2007",
                "contenu": """
                Fourchettes d'échéances :
                0-1 mois | 1-3 mois | 3-6 mois | 6-12 mois | 1-2 ans | 2-3 ans | >3 ans
                
                Méthode Simplifiée (volumes négligeables) :
                - 15% de la position nette longue ou courte
                - 3% des positions brutes longues et courtes
                
                Compensation autorisée entre sous-catégories si :
                - Substituables entre elles
                - Corrélation de 0,9 des prix sur 1 an (avec accord BAM)
                """
            }
        ],
        "tables": {
            "Fourchettes Échéances": {
                "headers": ["Fourchette", "Coefficient"],
                "data": [
                    ["0-1 mois", "1,5%"],
                    ["1-3 mois", "1,5%"],
                    ["3-6 mois", "1,5%"],
                    ["6-12 mois", "1,5%"],
                    ["1-2 ans", "1,5%"],
                    ["2-3 ans", "1,5%"],
                    ["> 3 ans", "1,5%"]
                ]
            }
        }
    },
    "📋 Options (Delta-Plus)": {
        "concept": {
            "titre": "Risque sur Options - Méthode Delta-Plus",
            "description": """
            Le risque sur options est calculé selon la méthode delta-plus qui prend 
            en compte les risques linéaires et non-linéaires.
            
            **Composantes :**
            - ✅ Risque Spécifique (via delta)
            - ✅ Risque Général (via delta)
            - ✅ Risques Résiduels (Gamma + Vega)
            
            **Facteurs de risque :**
            - Delta : Sensibilité au sous-jacent
            - Gamma : Non-linéarité (convexité)
            - Vega : Sensibilité à la volatilité
            """,
            "formule": "EFP = Risque Delta + |Gamma Nets Négatifs| + |Vega Nets|",
            "variables": {
                "Risque Delta": "Position équivalente = Valeur × Delta (intégré risques spécifique/général)",
                "Gamma": "½ × Gamma × (Variation Sous-jacent)²",
                "Vega": "Vega × (25% × Volatilité Implicite)",
                "Variation Sous-jacent": "8% (titres/change), 15% (matières)"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 54 - Section V",
                "titre": "Risque Options - Circulaire 26/G/2006",
                "contenu": """
                L'exigence en fonds propres au titre du risque sur options est 
                déterminée selon la méthode dite « delta-plus ».
                
                Cette exigence correspond à la somme des fonds propres requis au 
                titre des risques spécifique, général et résiduel.
                
                Les risques résiduels (gamma + vega) correspondent à la somme des 
                valeurs absolues des risques gamma nets négatifs et des risques vega.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 70 - Section VI",
                "titre": "Calcul Détaillé - NT 02/DSB/2007",
                "contenu": """
                A) Risque Gamma :
                - Formule : ½ × gamma × (variation du sous-jacent)²
                - Variation sous-jacent :
                  * Taux : variation présumée du tableau échéancier
                  * Titres/Indices : 8% × valeur marché
                  * Devises/Or : 8% × cours
                  * Matières : 15% × valeur marché
                
                B) Risque Vega :
                - Formule : vega × (25% × volatilité implicite)
                - Applicable à toutes catégories de sous-jacent
                
                C) Agrégation :
                - Pas de compensation entre fourchettes différentes
                - Calcul séparé par devise (taux) ou marché (titres)
                """
            }
        ],
        "tables": {
            "Variation Sous-jacent": {
                "headers": ["Type d'Option", "Variation du Sous-jacent"],
                "data": [
                    ["Instruments de taux", "Variation présumée tableau échéancier"],
                    ["Titres de propriété", "8% × valeur marché"],
                    ["Indices boursiers", "8% × valeur marché"],
                    ["Devises", "8% × cours du couple"],
                    ["Or", "8% × cours de l'or"],
                    ["Produits de base", "15% × valeur marché"]
                ]
            }
        }
    },
    "🔄 Dérivés de Crédit": {
        "concept": {
            "titre": "Risque sur Dérivés de Crédit",
            "description": """
            Le risque sur dérivés de crédit correspond aux pertes potentielles liées 
            aux positions sur instruments de transfert de risque de crédit.
            
            **Instruments couverts :**
            - ✅ Credit Default Swap (CDS)
            - ✅ Total Return Swap (TRS)
            - ✅ Credit Linked Notes (CLN)
            - ✅ First/Second Default Swap (FDS/SDS)
            
            **Compensation autorisée :**
            - 80% si conditions strictes remplies
            - 20% position résiduelle soumise au risque
            """,
            "formule": "EFP = Risque Spécifique + Risque Général",
            "variables": {
                "Risque Spécifique": "Position résiduelle × Pondération (selon Art. 54-I-A)",
                "Risque Général": "Calcul selon méthode taux d'intérêt",
                "Compensation": "80% si mêmes créances, montant, devise, échéance"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 54 - Section VI",
                "titre": "Risque Dérivés de Crédit - Circulaire 26/G/2006",
                "contenu": """
                L'exigence en fonds propres relative aux positions nettes sur 
                dérivés de crédit correspond à la somme des exigences en fonds 
                propres requises au titre du risque spécifique et du risque général.
                
                Le risque spécifique est calculé selon les pondérations du risque 
                de taux d'intérêt (Section I-A).
                
                Le risque général est calculé conformément au paragraphe B de la 
                Section I (méthode échéancier ou duration).
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 70 - Section VII",
                "titre": "Calcul Détaillé - NT 02/DSB/2007",
                "contenu": """
                A) Compensation (80%) :
                - CDS et/ou CLN opposés
                - Mêmes créances de référence, montant, devise, échéance
                - Position résiduelle de 20% soumise au risque spécifique
                
                B) TRS :
                - Vendeur protection = Position longue créance référence
                - Acheteur protection = Position courte créance référence
                
                C) FDS/SDS :
                - Couvre actif du panier avec pondération la plus faible
                - Choix libre si plusieurs actifs même pondération
                - Position résiduelle 20% après compensation
                """
            }
        ],
        "tables": {}
    }
}

# =============================================================================
# AFFICHAGE DYNAMIQUE SELON LE TYPE DE RISQUE SÉLECTIONNÉ
# =============================================================================

data = RISK_TYPES_DATA[risque_type]

# -----------------------------------------------------------------------------
# SECTION 1 : CONCEPT DU RISQUE (ENCADRÉ)
# -----------------------------------------------------------------------------
st.markdown("### 📚 Concept du Risque")

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

st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 2 : TABLEAUX RÉGLEMENTAIRES (SI DISPONIBLES)
# -----------------------------------------------------------------------------
if data.get("tables"):
    st.markdown("### 📊 Tableaux Réglementaires")
    
    for table_name, table_data in data["tables"].items():
        with st.expander(f"📋 {table_name}", expanded=True):
            df_table = pd.DataFrame(table_data["data"], columns=table_data["headers"])
            st.dataframe(df_table, use_container_width=True, hide_index=True)
    
    st.markdown("---")

# -----------------------------------------------------------------------------
# SECTION 3 : ARTICLES RÉGLEMENTAIRES (EXPANDERS)
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
# SECTION 4 : CALCULATEUR PRATIQUE
# -----------------------------------------------------------------------------
st.markdown("### 🧮 Calculateur Pratique")

if "Taux d'Intérêt" in risque_type:
    # =============================================================================
    # CALCULATEUR TAUX D'INTÉRÊT
    # =============================================================================
    st.markdown("#### 🏦 Risque de Taux d'Intérêt")
    
    # Risque Spécifique
    st.markdown("##### A) Risque Spécifique")
    
    col1, col2 = st.columns(2)
    
    with col1:
        position_nette = st.number_input("Position Nette Titres de Créance (MDH)", value=100.0, step=10.0)
        type_emission = st.selectbox(
            "Nature de l'Émission",
            ["État Marocain (MAD)", "Souverain AAA-AA-", "Souverain A+-BBB-", "Souverain BB+-B-", "Souverain < B-", "Qualifiées", "Autres Non Notés"]
        )
    
    with col2:
        echeance = st.selectbox(
            "Échéance Résiduelle",
            ["≤ 6 mois", "6-24 mois", "> 24 mois", "Toutes"]
        )
    
    # Mapping pondérations
    mapping_ponderation = {
        "État Marocain (MAD)": 0,
        "Souverain AAA-AA-": 0,
        "Souverain A+-BBB-": {"≤ 6 mois": 0.25, "6-24 mois": 1.0, "> 24 mois": 1.6, "Toutes": 1.0},
        "Souverain BB+-B-": 8.0,
        "Souverain < B-": 12.0,
        "Qualifiées": {"≤ 6 mois": 0.25, "6-24 mois": 1.0, "> 24 mois": 1.6, "Toutes": 1.0},
        "Autres Non Notés": 8.0
    }
    
    ponderation = mapping_ponderation.get(type_emission, 8.0)
    if isinstance(ponderation, dict):
        ponderation = ponderation.get(echeance, 1.0)
    
    efp_specifique = abs(position_nette) * (ponderation / 100)
    
    st.metric("EFP Risque Spécifique", f"{efp_specifique:.3f} MDH")
    
    # Risque Général
    st.markdown("---")
    st.markdown("##### B) Risque Général (Méthode Échéancier)")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        position_zone1 = st.number_input("Zone 1 (0-1 an) (MDH)", value=50.0, step=10.0)
    with col4:
        position_zone2 = st.number_input("Zone 2 (1-4 ans) (MDH)", value=30.0, step=10.0)
    with col5:
        position_zone3 = st.number_input("Zone 3 (>4 ans) (MDH)", value=20.0, step=10.0)
    
    # Calcul simplifié risque général
    efp_general = (position_zone1 * 0.40 + position_zone2 * 0.30 + position_zone3 * 0.30) * 0.08
    
    st.metric("EFP Risque Général", f"{efp_general:.3f} MDH")
    
    # Total
    efp_totale_taux = efp_specifique + efp_general
    
    st.markdown("---")
    st.markdown("##### 💰 Résultat Final")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("EFP Totale Taux d'Intérêt", f"{efp_totale_taux:.3f} MDH")
    with col_res2:
        risque_pondere = efp_totale_taux * 12.5
        st.metric("Risque Pondéré Marché", f"{risque_pondere:.3f} MDH")

elif "Titres de Propriété" in risque_type:
    # =============================================================================
    # CALCULATEUR TITRES DE PROPRIÉTÉ
    # =============================================================================
    st.markdown("#### 📊 Risque sur Titres de Propriété")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Risque Spécifique**")
        position_brute = st.number_input("Position Brute Titres (MDH)", value=100.0, step=10.0)
        portefeuille_diversifie = st.checkbox("Portefeuille Liquide et Diversifié", value=False)
        
        if portefeuille_diversifie:
            ponderation_specifique = 4.0
        else:
            ponderation_specifique = 8.0
        
        efp_specifique = position_brute * (ponderation_specifique / 100)
        st.metric("EFP Risque Spécifique", f"{efp_specifique:.2f} MDH")
    
    with col2:
        st.markdown("**Risque Général**")
        position_nette_globale = st.number_input("Position Nette Globale (MDH)", value=80.0, step=10.0)
        efp_general = abs(position_nette_globale) * 0.08
        st.metric("EFP Risque Général", f"{efp_general:.2f} MDH")
    
    efp_totale_titres = efp_specifique + efp_general
    
    st.markdown("---")
    st.markdown("##### 💰 Résultat Final")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("EFP Totale Titres", f"{efp_totale_titres:.2f} MDH")
    with col_res2:
        risque_pondere = efp_totale_titres * 12.5
        st.metric("Risque Pondéré Marché", f"{risque_pondere:.2f} MDH")

elif "Change" in risque_type:
    # =============================================================================
    # CALCULATEUR CHANGE
    # =============================================================================
    st.markdown("#### 💱 Risque de Change")
    
    col1, col2 = st.columns(2)
    
    with col1:
        positions_longues = st.number_input("Total Positions Longues (MDH)", value=100.0, step=10.0)
    
    with col2:
        positions_courtes = st.number_input("Total Positions Courtes (MDH)", value=80.0, step=10.0)
    
    position_or = st.number_input("Position Nette Or (MDH)", value=0.0, step=10.0)
    
    efp_change = 0.08 * (max(positions_longues, positions_courtes) + abs(position_or))
    
    st.markdown("---")
    st.markdown("##### 💰 Résultat Final")
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("Position Nette Maximale", f"{max(positions_longues, positions_courtes):.2f} MDH")
    with col_res2:
        st.metric("Position Or", f"{abs(position_or):.2f} MDH")
    with col_res3:
        st.metric("EFP Risque de Change", f"{efp_change:.2f} MDH")

elif "Produits de Base" in risque_type:
    # =============================================================================
    # CALCULATEUR PRODUITS DE BASE
    # =============================================================================
    st.markdown("#### 🛢️ Risque sur Produits de Base")
    
    methode = st.selectbox("Méthode de Calcul", ["Tableau d'Échéances", "Approche Simplifiée"])
    
    if methode == "Approche Simplifiée":
        col1, col2 = st.columns(2)
        with col1:
            position_nette = st.number_input("Position Nette (MDH)", value=100.0, step=10.0)
        with col2:
            position_brute = st.number_input("Position Brute (MDH)", value=150.0, step=10.0)
        
        efp_produits = (position_nette * 0.15) + (position_brute * 0.03)
        st.metric("EFP Produits de Base", f"{efp_produits:.2f} MDH")
    else:
        st.info("📌 Méthode Tableau d'Échéances : Calcul complet par fourchette en développement")
        
        col1, col2 = st.columns(2)
        with col1:
            positions_compensees = st.number_input("Positions Compensées Intra-Fourchette (MDH)", value=50.0, step=10.0)
        with col2:
            positions_residuelles = st.number_input("Positions Résiduelles (MDH)", value=30.0, step=10.0)
        
        reports = st.number_input("Nombre de Reports", value=1, min_value=0)
        
        efp_produits = (positions_compensees * 0.015) + (positions_compensees * 0.006 * reports) + (positions_residuelles * 0.15)
        st.metric("EFP Produits de Base", f"{efp_produits:.2f} MDH")

elif "Options" in risque_type:
    # =============================================================================
    # CALCULATEUR OPTIONS
    # =============================================================================
    st.markdown("#### 📋 Risque sur Options (Méthode Delta-Plus)")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        delta = st.number_input("Delta", value=0.6, step=0.1)
        valeur_sous_jacent = st.number_input("Valeur Marché Sous-jacent (MDH)", value=100.0, step=10.0)
    
    with col2:
        gamma = st.number_input("Gamma", value=0.02, step=0.01)
        type_sous_jacent = st.selectbox("Type de Sous-jacent", ["Titres/Indices", "Devises/Or", "Produits de Base"])
    
    with col3:
        vega = st.number_input("Vega", value=0.15, step=0.01)
        volatibilite_implicite = st.number_input("Volatilité Implicite (%)", value=20.0, step=1.0)
    
    # Calcul
    position_equivalente = valeur_sous_jacent * delta
    
    if type_sous_jacent == "Produits de Base":
        variation_sous_jacent = 0.15 * valeur_sous_jacent
    else:
        variation_sous_jacent = 0.08 * valeur_sous_jacent
    
    risque_gamma = 0.5 * gamma * (variation_sous_jacent ** 2)
    risque_vega = vega * (volatibilite_implicite / 100 * 0.25)
    
    efp_delta = abs(position_equivalente * 0.08)
    efp_options = efp_delta + abs(risque_gamma) + abs(risque_vega)
    
    st.markdown("---")
    st.markdown("##### 💰 Résultat Final")
    
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    with col_res1:
        st.metric("Risque Delta", f"{efp_delta:.3f} MDH")
    with col_res2:
        st.metric("Risque Gamma", f"{risque_gamma:.3f} MDH")
    with col_res3:
        st.metric("Risque Vega", f"{risque_vega:.3f} MDH")
    with col_res4:
        st.metric("EFP Totale Options", f"{efp_options:.3f} MDH")

elif "Dérivés de Crédit" in risque_type:
    # =============================================================================
    # CALCULATEUR DÉRIVÉS DE CRÉDIT
    # =============================================================================
    st.markdown("#### 🔄 Risque sur Dérivés de Crédit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        valeur_nominale = st.number_input("Valeur Nominale Créance Référence (MDH)", value=100.0, step=10.0)
        type_instrument = st.selectbox("Type d'Instrument", ["CDS", "TRS", "CLN", "FDS/SDS"])
    
    with col2:
        compensation_possible = st.checkbox("Conditions de Compensation Remplies (80%)", value=False)
        ponderation_reference = st.selectbox("Pondération Créance Référence", ["0%", "20%", "50%", "100%", "150%"])
    
    # Mapping pondérations
    mapping_pond = {"0%": 0, "20%": 0.20, "50%": 0.50, "100%": 1.0, "150%": 1.50}
    pond = mapping_pond.get(ponderation_reference, 1.0)
    
    if compensation_possible:
        position_residuelle = valeur_nominale * 0.20  # 20% résiduel
    else:
        position_residuelle = valeur_nominale
    
    efp_specifique = position_residuelle * pond * 0.08
    efp_derivs_credit = efp_specifique  # Risque général souvent nul pour CDS/FDS
    
    st.markdown("---")
    st.markdown("##### 💰 Résultat Final")
    
    col_res1, col_res2 = st.columns(2)
    with col_res1:
        st.metric("Position Résiduelle", f"{position_residuelle:.2f} MDH")
    with col_res2:
        st.metric("EFP Dérivés de Crédit", f"{efp_derivs_credit:.2f} MDH")

# =============================================================================
# EXPORT DES RÉSULTATS
# =============================================================================
st.markdown("---")
st.markdown("### 💾 Exporter les Résultats")

col_exp1, col_exp2 = st.columns(2)

with col_exp1:
    if st.button("📥 Exporter les Résultats (CSV)", use_container_width=True):
        resultats = {
            "Type de Risque": [risque_type],
            "EFP Calculée (MDH)": [efp_totale_taux if "Taux" in risque_type else (efp_totale_titres if "Titres" in risque_type else (efp_change if "Change" in risque_type else (efp_produits if "Produits" in risque_type else (efp_options if "Options" in risque_type else efp_derivs_credit))))],
            "Risque Pondéré (MDH)": [risque_pondere if "risque_pondere" in locals() else "N/A"]
        }
        df_export = pd.DataFrame(resultats)
        csv = df_export.to_csv(index=False, encoding='utf-8-sig').encode('utf-8')
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name=f"risque_marche_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

with col_exp2:
    if st.button("🔄 Réinitialiser", use_container_width=True):
        st.rerun()

# =============================================================================
# PIED DE PAGE
# =============================================================================
st.markdown("---")
st.info("📌 **Note :** Les calculs sont basés sur la Circulaire 26/G/2006 Article 54 et la NT 02/DSB/2007 Articles 55-73")
