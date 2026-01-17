# 🚗📊 Analyse des Données de Mobilité Urbaine et Pollution

## 📋 Contexte
Projet réalisé dans le cadre du Bootcamp FORCE-N (Data Analysis & Data Engineering) sur l'analyse des données de mobilité urbaine au Sénégal.

## 🎯 Objectifs
- Pipeline de traitement des données de mobilité et pollution
- Identification des zones et créneaux horaires critiques
- Dashboard interactif de visualisation
- Recommandations pour réduire congestion et pollution

## 🏗️ Architecture du Projet
Bootcamp_Projet_Mobilite_Urbaine_Pollution/
├── data/ # Données
│ ├── mobility_urban_pollution_300.xlsx # Données brutes (non versionnées)
│ └── mobility_data_processed_winsorize.csv # Données nettoyées
├── notebooks/ # Notebooks d'analyse exploratoire
│ ├── analysis.ipynb # Exploration
├── src/ # Code source principal
│ │── pipeline.py # Pipeline de traitement principal
│ ├── connector.py # Connexion MySQL
│ │── schema.sql # Schéma de la base
├── docs/ # Documentation
├── .gitignore # Fichiers ignorés par Git
├── requirements.txt # Dépendances Python
├── main.py # Point d'entrée du pipeline
└── README.md # Ce fichier


## ⚙️ Installation

### Prérequis
- Python 3.9+
- MySQL Server (optionnel pour l'analyse locale)
- Git

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