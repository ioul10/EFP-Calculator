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
# STYLE CSS PERSONNALISÉ
# =============================================================================
st.markdown("""
    <style>
    .concept-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 25px;
        border-radius: 15px;
        border-left: 6px solid #2196f3;
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
        background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%);
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
        border: 2px solid #2196f3;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0;
        font-family: 'Courier New', monospace;
    }
    .method-selector {
        background: #e3f2fd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2196f3;
        margin: 15px 0;
    }
    .warning-box {
        background: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 15px 0;
    }
    </style>
""", unsafe_allow_html=True)

# =============================================================================
# EN-TÊTE
# =============================================================================
st.title("🛡️ Calculateur - Risque de Crédit")
st.markdown("**Articles 9-47 de la Circulaire 26/G/2006 + Articles 1-54 de la NT 02/DSB/2007**")
st.markdown("---")

# =============================================================================
# BARRE LATÉRALE - CHOIX DU TYPE DE CONTREPARTIE
# =============================================================================
st.sidebar.header("🎯 Type de Contrepartie")

contrepartie_type = st.sidebar.radio(
    "Sélectionner la catégorie",
    [
        "🏛️ État Marocain & BAM",
        "🌍 Souverains Étrangers",
        "🏦 Banques Multilatérales de Développement",
        "🏢 Établissements de Crédit",
        "🏭 Grandes Entreprises",
        "🏪 PME",
        "👤 Clientèle de Détail/TPE",
        "🏠 Immobilier Résidentiel",
        "🏬 Immobilier Commercial",
        "⚠️ Créances en Souffrance",
        "📋 Engagements de Hors-Bilan"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("""
**Ratio de Solvabilité :**
- Minimum 10% (Art. 2 G26)
- EFP Crédit = 8% × Risque Pondéré
- FP Base ≥ 50% de l'EFP Crédit
""")

# =============================================================================
# DONNÉES PAR TYPE DE CONTREPARTIE
# =============================================================================
COUNTERPARTY_DATA = {
    "🏛️ État Marocain & BAM": {
        "concept": {
            "titre": "Créances sur l'État Marocain et Bank Al-Maghrib",
            "description": """
            Les créances sur l'État marocain et Bank Al-Maghrib bénéficient du 
            traitement le plus favorable en termes de pondération du risque de crédit.
            
            **Caractéristiques principales :**
            - ✅ Pondération de 0% pour créances en dirhams
            - ✅ Inclut BRI, FMI, BCE, Commission Européenne
            - ✅ Aucune exigence en fonds propres pour ces expositions
            - ✅ Base : Article 11-A-1 de la Circulaire 26/G/2006
            """,
            "formule": "Risque Pondéré = Exposition × 0%",
            "variables": {
                "Exposition": "Montant brut de la créance (après provisions)",
                "Pondération": "0% (dirhams)",
                "EFP": "8% × Risque Pondéré = 0 MDH"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-A-1",
                "titre": "Créances sur emprunteurs souverains - Circulaire 26/G/2006",
                "contenu": """
                Nonobstant les règles générales, une pondération de 0% est appliquée 
                aux créances sur l'État marocain et sur Bank Al-Maghrib, libellées 
                et financées en dirhams, ainsi qu'aux créances sur la Banque des 
                Règlements Internationaux, le Fonds Monétaire International, la 
                Banque Centrale Européenne et la Commission Européenne.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 10-A",
                "titre": "Organismes de Crédit à l'Exportation - NT 02/DSB/2007",
                "contenu": """
                Les Organismes de Crédit à l'Exportation (OCE), visés à l'alinéa 3) 
                du paragraphe A) de l'article 11 de la circulaire 26/G/2006, dont 
                les notations de crédit peuvent être utilisées sont ceux qui adhèrent 
                à la méthodologie agréée par l'OCDE et publient leurs évaluations.
                """
            }
        ],
        "tables": {
            "Pondérations État Marocain": {
                "headers": ["Type de Créance", "Devise", "Pondération"],
                "data": [
                    ["État Marocain", "Dirhams", "0%"],
                    ["Bank Al-Maghrib", "Dirhams", "0%"],
                    ["BRI", "Toutes", "0%"],
                    ["FMI", "Toutes", "0%"],
                    ["BCE", "Toutes", "0%"],
                    ["Commission Européenne", "Toutes", "0%"]
                ]
            }
        }
    },
    "🌍 Souverains Étrangers": {
        "concept": {
            "titre": "Créances sur les États et Banques Centrales Étrangers",
            "description": """
            Les créances sur les souverains étrangers sont pondérées selon leur 
            notation externe attribuée par un OEEC éligible (Fitch, Moody's, S&P).
            
            **Caractéristiques principales :**
            - ✅ Notations externes obligatoires (Art. 9 G26)
            - ✅ 3 OEEC éligibles : Fitch, Moody's, Standard & Poor's
            - ✅ Pondérations de 0% à 150% selon notation
            - ✅ Échéance résiduelle influence la pondération (A+ à BBB-)
            """,
            "formule": "Risque Pondéré = Exposition × Pondération (selon notation)",
            "variables": {
                "Exposition": "Montant brut de la créance",
                "Notation": "Notation externe OEEC (long/court terme)",
                "Pondération": "0% à 150% selon tableau Art. 11-A-2"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-A-2",
                "titre": "Pondérations Souverains - Circulaire 26/G/2006",
                "contenu": """
                Les pondérations appliquées aux créances sur les États et leurs 
                banques centrales sont les suivantes :
                
                - AAA à AA- : 0%
                - A+ à A- : 20%
                - BBB+ à BBB- : 50%
                - BB+ à BB- : 100%
                - B+ à B- : 100%
                - Inférieure à B- : 150%
                - Pas de notation : 100%
                """
            },
            {
                "numéro": "Article 9",
                "titre": "Usage des Notations Externes - Circulaire 26/G/2006",
                "contenu": """
                Pour la détermination des pondérations du risque de crédit, les 
                établissements utilisent les notations externes attribuées par des 
                organismes externes d'évaluation du crédit (OEEC) dont la liste est 
                établie par Bank Al-Maghrib.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 1",
                "titre": "OEEC Éligibles - NT 02/DSB/2007",
                "contenu": """
                Les organismes externes d'évaluation du crédit (OEEC) dont les 
                notations externes peuvent être utilisées sont :
                - Fitch Ratings
                - Moody's Investors Service
                - Standard & Poor's Rating Services
                
                La méthodologie utilisée est celle de Standard & Poor's à titre 
                d'illustration. Les méthodologies des autres OEEC peuvent également 
                être utilisées.
                """
            }
        ],
        "tables": {
            "Pondérations Souverains Étrangers": {
                "headers": ["Notation Long Terme", "Notation Court Terme", "Pondération"],
                "data": [
                    ["AAA à AA-", "-", "0%"],
                    ["A+ à A-", "A-1+, A-1", "20%"],
                    ["BBB+ à BBB-", "A-2", "50%"],
                    ["BB+ à BB-", "A-3", "100%"],
                    ["B+ à B-", "Inférieure à A-3", "100%"],
                    ["< B-", "-", "150%"],
                    ["Non noté", "-", "100%"]
                ]
            },
            "Correspondance OEEC": {
                "headers": ["S&P", "Moody's", "Fitch"],
                "data": [
                    ["AAA à AA-", "Aaa à Aa3", "AAA à AA-"],
                    ["A+ à A-", "A1 à A3", "A+ à A-"],
                    ["BBB+ à BBB-", "Baa1 à Baa3", "BBB+ à BBB-"],
                    ["BB+ à BB-", "Ba1 à Ba3", "BB+ à BB-"],
                    ["B+ à B-", "B1 à B3", "B+ à B-"],
                    ["< B-", "< B3", "< B-"]
                ]
            }
        }
    },
    "🏦 Banques Multilatérales de Développement": {
        "concept": {
            "titre": "Créances sur les Banques Multilatérales de Développement",
            "description": """
            Les créances sur certaines BMD bénéficient d'une pondération de 0%. 
            La liste est arrêtée par Bank Al-Maghrib.
            
            **Caractéristiques principales :**
            - ✅ 12 BMD pondérées à 0% (Art. 10-B NT)
            - ✅ Autres BMD : selon notation externe
            - ✅ Inclut BIRD, SFI, BAD, BEI, etc.
            """,
            "formule": "Risque Pondéré = Exposition × 0% (BMD liste BAM)",
            "variables": {
                "Exposition": "Montant brut de la créance",
                "BMD Éligibles": "Liste de 12 BMD (Art. 10-B NT)",
                "Pondération": "0% ou selon notation"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-C",
                "titre": "BMD - Circulaire 26/G/2006",
                "contenu": """
                Une pondération de 0% est appliquée aux BMD dont la liste est 
                arrêtée par Bank Al-Maghrib.
                
                Les pondérations appliquées aux créances sur les autres BMD sont 
                déterminées selon leur notation externe (20% à 150%).
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 10-B",
                "titre": "Liste des BMD - NT 02/DSB/2007",
                "contenu": """
                Les BMD dont la pondération est fixée à 0% sont :
                - BIRD (Banque Internationale pour la Reconstruction)
                - SFI (Société Financière Internationale)
                - BAEA (Banque Arabe pour le Développement en Afrique)
                - BAsD (Banque Asiatique de Développement)
                - BAD (Banque Africaine de Développement)
                - BERD (Banque Européenne pour la Reconstruction)
                - BID (Banque Interaméricaine de Développement)
                - BEI (Banque Européenne d'Investissement)
                - BNI (Banque Nordique d'Investissement)
                - BOC (Banque de Développement des Caraïbes)
                - BIsD (Banque Islamique de Développement)
                - BDCE (Banque de Développement du Conseil de l'Europe)
                """
            }
        ],
        "tables": {
            "BMD Pondérées 0%": {
                "headers": ["Acronyme", "Nom Complet"],
                "data": [
                    ["BIRD", "Banque Internationale pour la Reconstruction et le Développement"],
                    ["SFI", "Société Financière Internationale"],
                    ["BAEA", "Banque Arabe pour le Développement Économique en Afrique"],
                    ["BAsD", "Banque Asiatique de Développement"],
                    ["BAD", "Banque Africaine de Développement"],
                    ["BERD", "Banque Européenne pour la Reconstruction et le Développement"],
                    ["BID", "Banque Interaméricaine de Développement"],
                    ["BEI", "Banque Européenne d'Investissement"],
                    ["BNI", "Banque Nordique d'Investissement"],
                    ["BOC", "Banque de Développement des Caraïbes"],
                    ["BIsD", "Banque Islamique de Développement"],
                    ["BDCE", "Banque de Développement du Conseil de l'Europe"]
                ]
            }
        }
    },
    "🏢 Établissements de Crédit": {
        "concept": {
            "titre": "Créances sur les Établissements de Crédit",
            "description": """
            Les créances sur les banques et établissements assimilés sont pondérées 
            selon leur notation externe ou selon l'échéance initiale.
            
            **Caractéristiques principales :**
            - ✅ Notation long terme : 20% à 150%
            - ✅ Notation court terme (<1 an) : 20% à 150%
            - ✅ Traitement préférentiel ≤3 mois en monnaie locale : 20%
            - ✅ Établissements assimilés marocains : CDG, CCG, etc.
            """,
            "formule": "Risque Pondéré = Exposition × Pondération (selon notation/échéance)",
            "variables": {
                "Exposition": "Montant brut de la créance",
                "Notation": "Notation externe de la banque",
                "Échéance": "Initiale <1 an ou >1 an"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-D",
                "titre": "Établissements de Crédit - Circulaire 26/G/2006",
                "contenu": """
                Les pondérations appliquées aux créances sur les établissements de 
                crédit sont déterminées selon la notation externe :
                
                - AAA à AA- : 20%
                - A+ à BBB- : 50%
                - BB+ à B- : 100%
                - < B- : 150%
                - Pas de notation : 50%
                
                Créances <1 an notées : A-1 (20%), A-2 (50%), A-3 (100%)
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 10-C",
                "titre": "Établissements Assimilés Marocains - NT 02/DSB/2007",
                "contenu": """
                Les établissements assimilés marocains sont :
                - Caisse de Dépôt et de Gestion (CDG)
                - Caisse Centrale de Garantie (CCG)
                - Banques off-shore
                - Compagnies financières
                - Associations de micro-crédit
                """
            }
        ],
        "tables": {
            "Pondérations Banques": {
                "headers": ["Notation Long Terme", "Notation Court Terme", "Pondération"],
                "data": [
                    ["AAA à AA-", "-", "20%"],
                    ["A+ à A-", "A-1", "50% / 20%"],
                    ["BBB+ à BBB-", "A-2", "50% / 50%"],
                    ["BB+ à BB-", "A-3", "100% / 100%"],
                    ["B+ à B-", "< A-3", "100% / 150%"],
                    ["< B-", "-", "150%"],
                    ["Non noté", "-", "50%"]
                ]
            }
        }
    },
    "🏭 Grandes Entreprises": {
        "concept": {
            "titre": "Créances sur les Grandes Entreprises",
            "description": """
            Les créances sur les grandes entreprises (CA > 50 MDH) sont pondérées 
            selon leur notation externe ou option pondération unique 100%.
            
            **Caractéristiques principales :**
            - ✅ CA > 50 MDH (Art. 5 NT)
            - ✅ Notation externe : 20% à 150%
            - ✅ Option pondération unique 100% (avec accord BAM)
            - ✅ Non noté : 100% (ne peut être < État du pays)
            """,
            "formule": "Risque Pondéré = Exposition × Pondération (selon notation)",
            "variables": {
                "Exposition": "Montant brut de la créance",
                "CA": "Chiffre d'Affaires > 50 MDH",
                "Notation": "Notation externe entreprise"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-F",
                "titre": "Grandes Entreprises - Circulaire 26/G/2006",
                "contenu": """
                Les pondérations des créances sur les grandes entreprises sont :
                
                - AAA à AA- : 20%
                - A+ à A- : 50%
                - BBB+ à BBB- : 100%
                - BB+ à B- : 100%
                - < B- : 150%
                - Pas de notation : 100%
                
                Option pondération unique 100% possible avec accord BAM.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 5",
                "titre": "Définition Grande Entreprise - NT 02/DSB/2007",
                "contenu": """
                Le portefeuille « grande entreprise » (GE) englobe toutes les 
                créances sur les entreprises dont le chiffre d'affaires hors taxes 
                individuel, ou celui du groupe d'intérêt, est supérieur à 50 millions 
                de dirhams.
                
                Sont également incluses les créances sur des entreprises pour 
                lesquelles l'établissement n'est pas en mesure de disposer du CA 
                consolidé du groupe.
                """
            }
        ],
        "tables": {
            "Pondérations Entreprises": {
                "headers": ["Notation Long Terme", "Notation Court Terme", "Pondération"],
                "data": [
                    ["AAA à AA-", "-", "20%"],
                    ["A+ à A-", "A-1", "50% / 20%"],
                    ["BBB+ à BBB-", "A-2", "100% / 50%"],
                    ["BB+ à BB-", "A-3", "100% / 100%"],
                    ["B+ à B-", "< A-3", "150% / 150%"],
                    ["< B-", "-", "150%"],
                    ["Non noté", "-", "100%"]
                ]
            }
        }
    },
    "🏪 PME": {
        "concept": {
            "titre": "Créances sur les Petites et Moyennes Entreprises",
            "description": """
            Les créances sur les PME (CA 3-50 MDH) suivent les mêmes pondérations 
            que les grandes entreprises selon notation externe.
            
            **Caractéristiques principales :**
            - ✅ CA 3-50 MDH (Art. 4 NT)
            - ✅ CA < 3 MDH + Exposition > 1 MDH
            - ✅ Mêmes pondérations que GE
            - ✅ Option 100% unique possible
            """,
            "formule": "Risque Pondéré = Exposition × Pondération (selon notation)",
            "variables": {
                "Exposition": "Montant brut de la créance",
                "CA": "3-50 MDH ou <3 MDH + >1 MDH exposition",
                "Notation": "Notation externe PME"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-F",
                "titre": "PME - Circulaire 26/G/2006",
                "contenu": """
                Les pondérations des créances sur les PME sont déterminées selon 
                les mêmes modalités que les grandes entreprises (20% à 150% selon 
                notation externe).
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 4",
                "titre": "Définition PME - NT 02/DSB/2007",
                "contenu": """
                Est considérée comme une créance sur une PME toute créance sur une 
                entreprise dont :
                - CA > 3 MDH et ≤ 50 MDH, ou
                - CA < 3 MDH et montant global des créances > 1 MDH
                
                Le CA est extrait des états de synthèse consolidés selon normes 
                comptables internationales.
                """
            }
        ],
        "tables": {
            "Critères Segmentation PME": {
                "headers": ["CA (MDH)", "Exposition (MDH)", "Catégorie"],
                "data": [
                    ["≤ 3", "≤ 1", "Clientèle de Détail/TPE"],
                    ["≤ 3", "> 1", "PME"],
                    ["3 - 50", "Tous", "PME"],
                    ["> 50", "Tous", "Grande Entreprise"]
                ]
            }
        }
    },
    "👤 Clientèle de Détail/TPE": {
        "concept": {
            "titre": "Créances sur la Clientèle de Détail et TPE",
            "description": """
            Les créances sur les particuliers et TPE bénéficient d'une pondération 
            fixe de 75% (sauf exceptions).
            
            **Caractéristiques principales :**
            - ✅ Particuliers ou TPE (CA ≤ 3 MDH)
            - ✅ Exposition ≤ 0,2% du portefeuille détail
            - ✅ TPE : Exposition ≤ 1 MDH + CA ≤ 3 MDH
            - ✅ Pondération fixe : 75%
            - ✅ Exclut : Titres, immobilier résidentiel garanti
            """,
            "formule": "Risque Pondéré = Exposition × 75%",
            "variables": {
                "Exposition": "Montant brut de la créance",
                "Granularité": "≤ 0,2% du portefeuille détail",
                "Pondération": "75% (fixe)"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-G",
                "titre": "Clientèle de Détail - Circulaire 26/G/2006",
                "contenu": """
                Les créances sur les très petites entreprises (TPE) et les 
                particuliers sont pondérées à 75%.
                
                Les créances sur les particuliers, hors prêt immobilier résidentiel 
                garanti, dont le montant > 1 MDH, sont pondérées à 100%.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 3",
                "titre": "Critères Clientèle de Détail - NT 02/DSB/2007",
                "contenu": """
                Critères cumulatifs :
                - Particuliers ou TPE
                - Formes : crédits renouvelables, revolving, cartes, découverts, 
                  prêts terme, crédits-bails moyen/long terme
                - Montant global ≤ 0,2% du portefeuille détail
                - TPE : Exposition ≤ 1 MDH + CA ≤ 3 MDH
                
                Exclus : Titres cotés/non cotés, prêts immobiliers résidentiels 
                garantis par hypothèque.
                """
            }
        ],
        "tables": {
            "Critères Clientèle de Détail": {
                "headers": ["Critère", "Condition", "Valeur"],
                "data": [
                    ["Type de contrepartie", "Particuliers ou TPE", "-"],
                    ["Formes de crédit", "Renouvelables, terme, crédits-bails", "-"],
                    ["Granularité", "≤ 0,2% du portefeuille détail", "-"],
                    ["TPE Exposition", "≤ 1 MDH", "-"],
                    ["TPE CA", "≤ 3 MDH", "-"],
                    ["Pondération", "Fixe", "75%"]
                ]
            }
        }
    },
    "🏠 Immobilier Résidentiel": {
        "concept": {
            "titre": "Prêts Immobiliers à Usage Résidentiel",
            "description": """
            Les prêts immobiliers résidentiels garantis par hypothèque bénéficient 
            d'une pondération réduite de 35%.
            
            **Caractéristiques principales :**
            - ✅ Garantie hypothèque 1er rang (ou 2nd si État)
            - ✅ Valeur bien ≥ 120% de l'encours (LTV ≤ 80%)
            - ✅ Occupation par emprunteur ou location
            - ✅ Pondération : 35% (ou 75% si LTV > 80%)
            - ✅ Évaluations rigoureuses et actualisées
            """,
            "formule": "Risque Pondéré = Exposition × 35% (si LTV ≤ 80%)",
            "variables": {
                "Exposition": "Encours du prêt",
                "LTV": "Loan-to-Value ≤ 80%",
                "Pondération": "35% ou 75% (portion > 80% LTV)"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-H",
                "titre": "Immobilier Résidentiel - Circulaire 26/G/2006",
                "contenu": """
                Une pondération de 35% est appliquée aux crédits consentis aux 
                particuliers pour l'acquisition, l'aménagement ou la construction 
                de logements, intégralement garantis par une hypothèque.
                
                Conditions :
                - Valeur bien hypothéqué ≥ 120% de l'encours (LTV ≤ 80%)
                - Hypothèque de 1er rang (ou 2nd si État)
                - Évaluations rigoureuses et actualisées
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 10-E",
                "titre": "Évaluation des Biens - NT 02/DSB/2007",
                "contenu": """
                La valeur des biens hypothéqués doit être calculée sur la base de 
                règles d'évaluation rigoureuses et actualisées à intervalles réguliers.
                
                La fréquence d'évaluation doit être renforcée pour les prêts les 
                plus importants ou en cas de changements significatifs du marché 
                immobilier.
                """
            }
        ],
        "tables": {
            "Pondérations Immobilier Résidentiel": {
                "headers": ["LTV", "Condition", "Pondération"],
                "data": [
                    ["≤ 80%", "Hypothèque 1er rang", "35%"],
                    ["> 80%", "Portion excédant 80%", "75%"],
                    ["Tous", "Si conditions non remplies", "100%"]
                ]
            }
        }
    },
    "🏬 Immobilier Commercial": {
        "concept": {
            "titre": "Prêts Immobiliers à Usage Commercial",
            "description": """
            Les prêts garantis par des biens immobiliers commerciaux/professionnels 
            ont une pondération de 100% (ou 50% pour crédits-bails).
            
            **Caractéristiques principales :**
            - ✅ Usage professionnel ou commercial
            - ✅ Pondération standard : 100%
            - ✅ Crédits-bails avec évaluation : 50%
            - ✅ Évaluations rigoureuses et actualisées
            """,
            "formule": "Risque Pondéré = Exposition × 100% (ou 50% crédits-bails)",
            "variables": {
                "Exposition": "Encours du prêt",
                "Type": "Prêt standard ou crédit-bail",
                "Pondération": "100% ou 50%"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-I",
                "titre": "Immobilier Commercial - Circulaire 26/G/2006",
                "contenu": """
                Une pondération de 100% est appliquée aux prêts garantis par des 
                hypothèques sur des biens immobiliers à usage professionnel ou 
                commercial.
                
                Une pondération de 50% est appliquée aux crédits-bails et locations 
                avec option d'achat sous réserve d'évaluations rigoureuses et 
                actualisées.
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 10-F",
                "titre": "Évaluation Biens Commerciaux - NT 02/DSB/2007",
                "contenu": """
                Les biens immobiliers à usage professionnel ou commercial doivent 
                faire l'objet d'évaluations strictes et actualisées à intervalles 
                réguliers.
                
                La fréquence doit être renforcée pour les prêts les plus importants 
                ou en cas de changements significatifs du marché.
                """
            }
        ],
        "tables": {
            "Pondérations Immobilier Commercial": {
                "headers": ["Type de Crédit", "Condition", "Pondération"],
                "data": [
                    ["Prêt garanti hypothèque", "Usage commercial", "100%"],
                    ["Crédit-bail", "Évaluations rigoureuses", "50%"],
                    ["Location avec option achat", "Évaluations rigoureuses", "50%"]
                ]
            }
        }
    },
    "⚠️ Créances en Souffrance": {
        "concept": {
            "titre": "Créances en Souffrance",
            "description": """
            Les créances en souffrance ont des pondérations élevées selon le niveau 
            de provisions constituées.
            
            **Caractéristiques principales :**
            - ✅ Définition : Capital restant dû + échéances impayées
            - ✅ Immobilier résidentiel : 100% (<20% prov), 50% (≥20% prov)
            - ✅ Autres créances : 150% (≤20%), 100% (20-50%), 50% (>50%)
            - ✅ Nettes des provisions non couvertes par garanties
            """,
            "formule": "Risque Pondéré = Exposition Nette Provisions × Pondération",
            "variables": {
                "Exposition Nette": "Encours - Provisions",
                "Niveau Provisions": "<20%, 20-50%, >50%",
                "Pondération": "50% à 150%"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 11-J",
                "titre": "Créances en Souffrance - Circulaire 26/G/2006",
                "contenu": """
                Pour les prêts immobiliers résidentiels :
                - 100% si provisions < 20%
                - 50% si provisions ≥ 20%
                
                Pour les autres créances :
                - 150% si provisions ≤ 20%
                - 100% si provisions 20-50%
                - 50% si provisions > 50%
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 10-G",
                "titre": "Définition Souffrance - NT 02/DSB/2007",
                "contenu": """
                L'encours des créances en souffrance est défini comme le capital 
                restant dû augmenté des échéances impayées.
                
                Les pondérations s'appliquent à la partie nette des provisions non 
                couvertes par les garanties et sûretés de la Section IV.
                """
            }
        ],
        "tables": {
            "Pondérations Créances en Souffrance": {
                "headers": ["Type de Créance", "Provisions", "Pondération"],
                "data": [
                    ["Immobilier Résidentiel", "< 20%", "100%"],
                    ["Immobilier Résidentiel", "≥ 20%", "50%"],
                    ["Autres Créances", "≤ 20%", "150%"],
                    ["Autres Créances", "20% - 50%", "100%"],
                    ["Autres Créances", "> 50%", "50%"]
                ]
            }
        }
    },
    "📋 Engagements de Hors-Bilan": {
        "concept": {
            "titre": "Engagements de Hors-Bilan",
            "description": """
            Les engagements de hors-bilan sont convertis en équivalent risque de 
            crédit via des Facteurs de Conversion (FCEC) avant pondération.
            
            **Caractéristiques principales :**
            - ✅ 4 catégories de risque : Faible, Modéré, Moyen, Élevé
            - ✅ FCEC : 0%, 20%, 50%, 100%
            - ✅ Dérivés : Méthode risque courant (coût remplacement + potentiel)
            - ✅ Puis pondération selon contrepartie
            """,
            "formule": "Risque Pondéré = (Exposition × FCEC) × Pondération Contrepartie",
            "variables": {
                "Exposition": "Montant nominal de l'engagement",
                "FCEC": "Facteur de Conversion (0-100%)",
                "Pondération": "Selon catégorie de contrepartie"
            }
        },
        "articles_g26": [
            {
                "numéro": "Article 13-14",
                "titre": "Hors-Bilan - Circulaire 26/G/2006",
                "contenu": """
                Les engagements de hors-bilan sont convertis au moyen de facteurs 
                de conversion en équivalent risque de crédit (FCEC) :
                
                - Risque faible : 0%
                - Risque modéré : 20%
                - Risque moyen : 50%
                - Risque élevé : 100%
                
                Les montants obtenus sont pondérés selon la catégorie de contrepartie.
                """
            },
            {
                "numéro": "Article 15",
                "titre": "Dérivés - Circulaire 26/G/2006",
                "contenu": """
                Pour les dérivés (taux, devises, titres, matières) :
                Équivalent-risque = Coût de remplacement + Risque potentiel futur
                
                Risque potentiel = Nominal × Coefficient selon durée résiduelle
                """
            }
        ],
        "articles_nt": [
            {
                "numéro": "Article 11",
                "titre": "Catégories Hors-Bilan - NT 02/DSB/2007",
                "contenu": """
                A) Risque faible (0%) : Engagements révocables sans condition
                B) Risque modéré (20%) : Accords ≤1 an, crédits documentaires 
                   import garantis, garanties bonne exécution
                C) Risque moyen (50%) : Accords >1 an, facilités émission effets, 
                   engagements financement projet
                D) Risque élevé (100%) : Acceptations payer, ouvertures crédit 
                   irrévocables, garanties 1ère demande financière
                """
            },
            {
                "numéro": "Article 12",
                "titre": "Dérivés - NT 02/DSB/2007",
                "contenu": """
                Coefficients risque potentiel futur selon durée résiduelle :
                - ≤ 1 an : Taux 0%, Devises 1%, Titres 6%, Matières 10%
                - 1-5 ans : Taux 0.5%, Devises 5%, Titres 8%, Matières 12%
                - > 5 ans : Taux 1.5%, Devises 7.5%, Titres 10%, Matières 15%
                """
            }
        ],
        "tables": {
            "FCEC Engagements Hors-Bilan": {
                "headers": ["Catégorie de Risque", "FCEC", "Exemples"],
                "data": [
                    ["Faible", "0%", "Engagements révocables sans condition"],
                    ["Modéré", "20%", "Accords ≤1 an, crédits documentaires import"],
                    ["Moyen", "50%", "Accords >1 an, facilités émission effets"],
                    ["Élevé", "100%", "Acceptations payer, garanties 1ère demande"]
                ]
            },
            "Coefficients Dérivés": {
                "headers": ["Durée Résiduelle", "Taux", "Devises", "Titres", "Matières"],
                "data": [
                    ["≤ 1 an", "0%", "1%", "6%", "10%"],
                    ["1-5 ans", "0.5%", "5%", "8%", "12%"],
                    ["> 5 ans", "1.5%", "7.5%", "10%", "15%"]
                ]
            }
        }
    }
}

# =============================================================================
# AFFICHAGE DYNAMIQUE SELON LE TYPE DE CONTREPARTIE
# =============================================================================

data = COUNTERPARTY_DATA[contrepartie_type]

# -----------------------------------------------------------------------------
# SECTION 1 : CONCEPT DE LA CONTREPARTIE (ENCADRÉ)
# -----------------------------------------------------------------------------
st.markdown("### 📚 Concept de la Contrepartie")

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

# =============================================================================
# CALCULATEUR PAR TYPE DE CONTREPARTIE
# =============================================================================

if "État Marocain" in contrepartie_type:
    # ÉTAT MAROCAIN & BAM
    exposition = st.number_input("Montant de l'Exposition (MDH)", min_value=0.0, value=100.0, step=10.0)
    ponderation = 0.0
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Souverains Étrangers" in contrepartie_type:
    # SOUVERAINS ÉTRANGERS
    exposition = st.number_input("Montant de l'Exposition (MDH)", min_value=0.0, value=100.0, step=10.0)
    notation = st.selectbox("Notation Externe", 
                           ["AAA à AA-", "A+ à A-", "BBB+ à BBB-", "BB+ à BB-", "B+ à B-", "< B-", "Non noté"])
    
    mapping_pond = {"AAA à AA-": 0, "A+ à A-": 20, "BBB+ à BBB-": 50, "BB+ à BB-": 100, "B+ à B-": 100, "< B-": 150, "Non noté": 100}
    ponderation = mapping_pond.get(notation, 100)
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Banques Multilatérales" in contrepartie_type:
    # BMD
    exposition = st.number_input("Montant de l'Exposition (MDH)", min_value=0.0, value=100.0, step=10.0)
    bmd_eligible = st.checkbox("BMD de la liste BAM (pondération 0%)", value=True)
    
    ponderation = 0.0 if bmd_eligible else 50.0
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Établissements de Crédit" in contrepartie_type:
    # BANQUES
    exposition = st.number_input("Montant de l'Exposition (MDH)", min_value=0.0, value=100.0, step=10.0)
    notation = st.selectbox("Notation Externe", 
                           ["AAA à AA-", "A+ à A-", "BBB+ à BBB-", "BB+ à BB-", "B+ à B-", "< B-", "Non noté"])
    echeance = st.selectbox("Échéance Initiale", ["< 1 an", "> 1 an"])
    
    mapping_pond = {"AAA à AA-": 20, "A+ à A-": 50, "BBB+ à BBB-": 50, "BB+ à BB-": 100, "B+ à B-": 100, "< B-": 150, "Non noté": 50}
    ponderation = mapping_pond.get(notation, 50)
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Grandes Entreprises" in contrepartie_type or "PME" in contrepartie_type:
    # GE / PME
    exposition = st.number_input("Montant de l'Exposition (MDH)", min_value=0.0, value=100.0, step=10.0)
    notation = st.selectbox("Notation Externe", 
                           ["AAA à AA-", "A+ à A-", "BBB+ à BBB-", "BB+ à BB-", "B+ à B-", "< B-", "Non noté"])
    
    mapping_pond = {"AAA à AA-": 20, "A+ à A-": 50, "BBB+ à BBB-": 100, "BB+ à BB-": 100, "B+ à B-": 150, "< B-": 150, "Non noté": 100}
    ponderation = mapping_pond.get(notation, 100)
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Détail" in contrepartie_type:
    # DÉTAIL / TPE
    exposition = st.number_input("Montant de l'Exposition (MDH)", min_value=0.0, value=100.0, step=10.0)
    montant_superieur_1mdh = st.checkbox("Montant > 1 MDH (pondération 100%)", value=False)
    
    ponderation = 100.0 if montant_superieur_1mdh else 75.0
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Immobilier Résidentiel" in contrepartie_type:
    # IMMOBILIER RÉSIDENTIEL
    exposition = st.number_input("Encours du Prêt (MDH)", min_value=0.0, value=100.0, step=10.0)
    valeur_bien = st.number_input("Valeur du Bien Hypothéqué (MDH)", min_value=0.0, value=150.0, step=10.0)
    
    ltv = (exposition / valeur_bien * 100) if valeur_bien > 0 else 100
    st.info(f"**LTV (Loan-to-Value)** : {ltv:.1f}%")
    
    if ltv <= 80:
        ponderation = 35.0
    else:
        ponderation = 75.0
        st.warning("⚠️ LTV > 80% : Portion excédant 80% pondérée à 75%")
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Immobilier Commercial" in contrepartie_type:
    # IMMOBILIER COMMERCIAL
    exposition = st.number_input("Encours du Prêt (MDH)", min_value=0.0, value=100.0, step=10.0)
    type_credit = st.selectbox("Type de Crédit", ["Prêt garanti hypothèque", "Crédit-bail avec évaluation"])
    
    ponderation = 50.0 if "Crédit-bail" in type_credit else 100.0
    
    risque_pondere = exposition * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Souffrance" in contrepartie_type:
    # CRÉANCES EN SOUFFRANCE
    exposition_brute = st.number_input("Encours Brut (MDH)", min_value=0.0, value=100.0, step=10.0)
    provisions = st.number_input("Provisions Constituées (MDH)", min_value=0.0, value=20.0, step=5.0)
    type_creance = st.selectbox("Type de Créance", ["Immobilier Résidentiel", "Autres Créances"])
    
    exposition_nette = exposition_brute - provisions
    taux_provisions = (provisions / exposition_brute * 100) if exposition_brute > 0 else 0
    st.info(f"**Taux de Provisions** : {taux_provisions:.1f}%")
    
    if type_creance == "Immobilier Résidentiel":
        ponderation = 50.0 if taux_provisions >= 20 else 100.0
    else:
        if taux_provisions <= 20:
            ponderation = 150.0
        elif taux_provisions <= 50:
            ponderation = 100.0
        else:
            ponderation = 50.0
    
    risque_pondere = exposition_nette * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50

elif "Hors-Bilan" in contrepartie_type:
    # HORS-BILAN
    exposition_nominale = st.number_input("Montant Nominal (MDH)", min_value=0.0, value=100.0, step=10.0)
    categorie_risque = st.selectbox("Catégorie de Risque", ["Faible (0%)", "Modéré (20%)", "Moyen (50%)", "Élevé (100%)"])
    type_contrepartie = st.selectbox("Type de Contrepartie", ["État Marocain", "Souverain AAA-AA-", "Banque A+-BBB-", "Entreprise Non Notée"])
    
    mapping_fcec = {"Faible (0%)": 0, "Modéré (20%)": 20, "Moyen (50%)": 50, "Élevé (100%)": 100}
    fcec = mapping_fcec.get(categorie_risque, 50)
    
    mapping_pond = {"État Marocain": 0, "Souverain AAA-AA-": 0, "Banque A+-BBB-": 50, "Entreprise Non Notée": 100}
    ponderation = mapping_pond.get(type_contrepartie, 100)
    
    exposition_equivalente = exposition_nominale * (fcec / 100)
    risque_pondere = exposition_equivalente * (ponderation / 100)
    efp = risque_pondere * 0.08
    fp_base = efp * 0.50
    
    st.info(f"**Exposition Équivalente** : {exposition_equivalente:.2f} MDH (Nominal × FCEC)")

# =============================================================================
# RÉSULTATS DU CALCUL
# =============================================================================
st.markdown("---")
st.markdown("##### 💰 Résultats du Calcul")

col_res1, col_res2, col_res3, col_res4 = st.columns(4)

with col_res1:
    st.metric(
        label="Pondération Appliquée",
        value=f"{ponderation:.0f}%",
        delta=None
    )

with col_res2:
    st.metric(
        label="Risque Pondéré",
        value=f"{risque_pondere:.2f} MDH",
        delta=None
    )

with col_res3:
    st.metric(
        label="Exigence en Fonds Propres (8%)",
        value=f"{efp:.2f} MDH",
        delta=None
    )

with col_res4:
    st.metric(
        label="Fonds Propres de Base (Min 50%)",
        value=f"{fp_base:.2f} MDH",
        delta=None
    )

# =============================================================================
# DÉTAILS DU CALCUL
# =============================================================================
with st.expander("📝 Détails du Calcul"):
    if "Hors-Bilan" in contrepartie_type:
        st.write(f"""
        **Formule appliquée :**
        
        1. Exposition Équivalente = Nominal × FCEC
           - {exposition_nominale:.2f} MDH × {fcec}% = {exposition_equivalente:.2f} MDH
        
        2. Risque Pondéré = Exposition Équivalente × Pondération
           - {exposition_equivalente:.2f} MDH × {ponderation}% = {risque_pondere:.2f} MDH
        
        3. Exigence en Fonds Propres = Risque Pondéré × 8%
           - {risque_pondere:.2f} MDH × 8% = {efp:.2f} MDH
        
        4. Fonds Propres de Base (Min 50%) = EFP × 50%
           - {efp:.2f} MDH × 50% = {fp_base:.2f} MDH
        """)
    elif "Souffrance" in contrepartie_type:
        st.write(f"""
        **Formule appliquée :**
        
        1. Exposition Nette = Brut - Provisions
           - {exposition_brute:.2f} MDH - {provisions:.2f} MDH = {exposition_nette:.2f} MDH
        
        2. Taux de Provisions = {taux_provisions:.1f}%
           - Pondération appliquée : {ponderation}%
        
        3. Risque Pondéré = Exposition Nette × Pondération
           - {exposition_nette:.2f} MDH × {ponderation}% = {risque_pondere:.2f} MDH
        
        4. Exigence en Fonds Propres = Risque Pondéré × 8%
           - {risque_pondere:.2f} MDH × 8% = {efp:.2f} MDH
        """)
    else:
        st.write(f"""
        **Formule appliquée :**
        
        1. Risque Pondéré = Exposition × Pondération
           - {exposition:.2f} MDH × {ponderation}% = {risque_pondere:.2f} MDH
        
        2. Exigence en Fonds Propres = Risque Pondéré × 8%
           - {risque_pondere:.2f} MDH × 8% = {efp:.2f} MDH
        
        3. Fonds Propres de Base (Min 50%) = EFP × 50%
           - {efp:.2f} MDH × 50% = {fp_base:.2f} MDH
        
        **Références réglementaires :**
        - Article 11 de la Circulaire 26/G/2006 (Pondérations)
        - Article 6 de la Circulaire 26/G/2006 (Couverture FP)
        - Notice Technique NT 02/DSB/2007 (Modalités d'application)
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
            "Type de Contrepartie": [contrepartie_type],
            "Exposition (MDH)": [exposition if "Hors-Bilan" not in contrepartie_type else exposition_nominale],
            "Pondération": [f"{ponderation}%"],
            "Risque Pondéré (MDH)": [f"{risque_pondere:.2f}"],
            "EFP (MDH)": [f"{efp:.2f}"],
            "FP Base Min (MDH)": [f"{fp_base:.2f}"]
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

# =============================================================================
# PIED DE PAGE
# =============================================================================
st.markdown("---")
st.info("📌 **Note :** Les calculs sont basés sur la Circulaire 26/G/2006 Articles 9-47 et la NT 02/DSB/2007 Articles 1-54")
