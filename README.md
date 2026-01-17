# 🚗📊 Analyse des Données de Mobilité Urbaine et de la Pollution

## 📋 Contexte
Projet réalisé dans le cadre du Bootcamp FORCE-N (Data Analysis & Data Engineering) sur l'analyse des données de mobilité urbaine au Sénégal.

## 🎯 Objectifs
- Pipeline de traitement des données de mobilité et pollution
- Identification des zones et créneaux horaires critiques
- Dashboard interactif de visualisation
- Recommandations pour réduire congestion et pollution

## Équipe – Groupe 2
Mouhamadoul Mourtadha GUEYE
Babacar WADE
Mame Maréme DIA
Absa SYLLA
Lamine NDIAYE
Cheikh Ahmed Tidiane Baidy GUEYE


## 🏗️ Architecture du Projet
Bootcamp_Projet_Mobilite_Urbaine_Pollution/
├── data/ # Données
│ ├── mobility_urban_pollution_300.xlsx # Données brutes (non versionnées)
│ └── mobility_data_processed_winsorize.csv # Données nettoyées
├── notebooks/ # Notebooks d'analyse exploratoire
│ ├── analysis.ipynb # Exploration
| ├── btcamp.ipynb # Exploration
├── src/ # Code source principal
│ │── pipeline.py # Pipeline de traitement principal
│ ├── db_connector.py # Connexion MySQL
│ │── app.py # dashboard streamlit
├── docs/ # Documentation
├── .gitignore # Fichiers ignorés par Git
├── requirements.txt # Dépendances Python
├── main.py # Point d'entrée du pipeline
└── README.md # Ce fichier

## Outils Utilisés

Catégorie	                    Outils
Analyse & Traitement	        Python, Pandas, NumPy, Scikit-learn
Visualisation               	Matplotlib, Seaborn, Power BI
Pipeline & Base de données  	MySQL, SQLAlchemy, PyMySQL
Gestion de projet           	Git, PowerPoint, Jupyter Notebook

## ⚙️ Installation

### Prérequis
- Python/Pandas
- MySQL Server (optionnel pour l'analyse locale)
- Git
- Power BI

### 1. Cloner le dépôt
git clone https://github.com/mourtadag4-code/Bootcamp_Projet_Mobilite_Urbaine_Pollution.git
cd Bootcamp_Projet_Mobilite_Urbaine_Pollution

### 2. Installer les dépendances
pip install -r requirements.txt

## Utilisation
### Exécuter le pipeline complet
python main.py

### Exécuter étape par étape
### 1. Dans un notebook Jupyter ou script Python
from src.data_processing.pipeline import run_full_pipeline
from src.database.connector import save_to_mysql

### 2. Traiter les données
df_processed = run_full_pipeline('data/raw/mobility_data.xlsx')

### 3. Sauvegarder dans MySQL (optionnel)
save_to_mysql(df_processed, table_name='mobility_processed')

### 4. Analyser les données
print(df_processed.describe())

### Accéder aux données pour analyse
import pandas as pd
df = pd.read_csv('data/mobility_data_processed_winsorize.csv')

## Étapes du Projet
### Chargement et Exploration des Données
Données initiales : 300 lignes, 8 colonnes (route_id, timestamp, latitude, longitude, speed_kmh, traffic_density, air_quality_index, weather).

Aucune valeur manquante détectée.

### Nettoyage et Transformation
Conversion du timestamp et extraction de features temporelles (hour, day_of_week, month, is_weekend).
Traitement des outliers via plusieurs méthodes (Winsorization, Capping IQR, Log, Suppression).
Catégorisation des variables :
    aqi_category (Bon, Modéré, Mauvais, Dangereux)
    speed_category (Lente, Normale, Rapide)
    traffic_category (Fluide, Modéré, Dense)
Création de nouvelles variables : speed_traffic_product, traffic_aqi_flag, is_rush_hour

###  Pipeline de Données
Intégration d’un pipeline de prétraitement robuste avec RobustScaler pour gérer les valeurs aberrantes.
Sauvegarde des données traitées en CSV et injection dans une base MySQL (mobility_db.mobility_processed).

### Analyse Exploratoire
Analyse univariée : statistiques descriptives, distribution des variables clés.
Analyse bivariée : relations entre vitesse, densité, qualité de l’air et conditions météo.
Visualisations : histograms, boxplots, scatter plots, heatmaps.

###  Tableau de Bord Interactif
Développement d’un dashboard sous Power BI pour :
    Visualiser les zones critiques (congestion, pollution).
    Analyser les tendances temporelles (heures de pointe, weekends).
    Croiser les données météo avec les indicateurs de mobilité.

## Résultats Clés
Vitesse Moyenne
    Moyenne : 28.8 km/h
    Médiane : 28.5 km/h
Interprétation : Circulation urbaine typique, avec des vitesses faibles suggérant une congestion fréquente.

Qualité de l’Air (AQI)
    Moyenne : 63.9 (niveau modéré)
    Pics jusqu’à 97 (mauvaise qualité)
Lien probable avec la densité du trafic.

Densité du Trafic
    Moyenne : 0.31
    Max : 0.84 (forte congestion)
Distribution : majorité des situations modérées, avec des pics localisés.

##  Pipeline Détaillé
# Exemple de pipeline principal
processed_data, ml_pipeline = run_full_pipeline(
    file_path="data/raw/mobility_urban_pollution_300.xlsx",
    outlier_method="winsorize",
    outlier_robust=True
)

Sorties :
    Données nettoyées et enrichies (20 colonnes)
    Pipeline ML prêt pour la modélisation (ColumnTransformer avec RobustScaler)
    Export CSV et insertion MySQL automatique

## Recommandations Opérationnelles
- Fluidifier le trafic aux heures de pointe par une régulation dynamique.
- Promouvoir les transports en commun et les mobilités douces.
- Surveiller la qualité de l’air dans les zones à fort trafic.
- Étudier les corrélations trafic-pollution pour des politiques ciblées.
- Généraliser l’approche data-driven à d’autres villes sénégalaises.

## Livrables
Pipeline de données fonctionnel (Python/SQL, Jupyter, Airflow/dbt)
Dashboard interactif (Streamlit)
Présentation synthèse (5–7 slides)
Code source et documentation (GitHub)