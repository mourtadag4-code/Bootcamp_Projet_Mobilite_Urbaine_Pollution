import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler, LabelEncoder, RobustScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# 1. CHARGEMENT DES DONNÉES
def load_data(file_path):
    """Charge les données depuis le fichier Excel"""
    df = pd.read_excel(file_path)
    print(f"✅ Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    return df

# 2. DÉTECTION DES VALEURS ABERRANTES
def detect_outliers(df, numerical_cols=None, method='iqr', threshold=1.5):
    """Détecte les valeurs aberrantes dans les colonnes numériques"""

    if numerical_cols is None:
        numerical_cols = ['speed_kmh', 'traffic_density', 'air_quality_index',
                         'latitude', 'longitude']

    outliers_info = {}
    outlier_indices = set()

    for col in numerical_cols:
        if col not in df.columns:
            continue

        data = df[col].dropna()

        if method == 'iqr':
            # Méthode IQR (Interquartile Range)
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        elif method == 'zscore':
            # Méthode Z-score
            z_scores = np.abs(stats.zscore(data))
            outliers = df[z_scores > threshold]

        elif method == 'percentile':
            # Méthode des percentiles
            lower_bound = data.quantile(0.01)
            upper_bound = data.quantile(0.99)
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

        if len(outliers) > 0:
            outliers_info[col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100,
                'indices': outliers.index.tolist(),
                'min_value': outliers[col].min(),
                'max_value': outliers[col].max()
            }
            outlier_indices.update(outliers.index)

    return outliers_info, list(outlier_indices)

# 3. TRAITEMENT DES VALEURS ABERRANTES
def handle_outliers(df, numerical_cols=None, method='winsorize', winsorize_limits=(0.01, 0.01)):
    """Traite les valeurs aberrantes selon différentes méthodes"""

    df_clean = df.copy()

    if numerical_cols is None:
        numerical_cols = ['speed_kmh', 'traffic_density', 'air_quality_index']

    print("\n🔍 TRAITEMENT DES VALEURS ABERRANTES")
    print("=" * 50)

    # Détection initiale
    outliers_info, outlier_indices = detect_outliers(df_clean, numerical_cols)

    if outliers_info:
        print(f"📊 {len(outlier_indices)} enregistrements avec valeurs aberrantes détectés")

        for col, info in outliers_info.items():
            print(f"\n  {col}:")
            print(f"    • {info['count']} outliers ({info['percentage']:.2f}%)")
            print(f"    • Plage des outliers: [{info['min_value']:.2f}, {info['max_value']:.2f}]")
            print(f"    • Plage normale: [{df_clean[col].min():.2f}, {df_clean[col].max():.2f}]")
    else:
        print("✅ Aucune valeur aberrante détectée")

    # Application du traitement selon la méthode choisie
    for col in numerical_cols:
        if col not in df_clean.columns:
            continue

        if method == 'winsorize':
            # Winsorization : remplace les extrêmes par des percentiles
            lower_limit = winsorize_limits[0]
            upper_limit = 1 - winsorize_limits[1]

            lower_bound = df_clean[col].quantile(lower_limit)
            upper_bound = df_clean[col].quantile(upper_limit)

            df_clean[col] = np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
            df_clean[col] = np.where(df_clean[col] > upper_bound, upper_bound, df_clean[col])

            print(f"\n✅ {col}: Winsorization appliquée (limites: {lower_limit}, {upper_limit})")

        elif method == 'cap':
            # Capping avec IQR
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            df_clean[col] = np.where(df_clean[col] < lower_bound, lower_bound, df_clean[col])
            df_clean[col] = np.where(df_clean[col] > upper_bound, upper_bound, df_clean[col])

            print(f"\n✅ {col}: Capping IQR appliqué")

        elif method == 'log':
            # Transformation logarithmique (pour données asymétriques)
            if (df_clean[col] > 0).all():
                df_clean[col] = np.log1p(df_clean[col])
                print(f"\n✅ {col}: Transformation logarithmique appliquée")
            else:
                print(f"\n⚠️  {col}: Transformation log impossible (valeurs négatives)")

        elif method == 'remove':
            # Suppression des outliers (méthode agressive)
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            mask = (df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)
            df_clean = df_clean[mask]
            print(f"\n✅ {col}: Outliers supprimés")

    # Vérification après traitement
    outliers_info_after, _ = detect_outliers(df_clean, numerical_cols)
    if outliers_info_after:
        remaining_outliers = sum(info['count'] for info in outliers_info_after.values())
        print(f"\n⚠️  {remaining_outliers} outliers restants après traitement")
    else:
        print("\n🎉 Toutes les valeurs aberrantes ont été traitées")

    return df_clean

# 4. NETTOYAGE DES DONNÉES
def clean_data(df, outlier_method='winsorize'):
    """Nettoie les données avec traitement des outliers"""
    df_clean = df.copy()

    # Conversion du timestamp
    df_clean['timestamp'] = pd.to_datetime(df_clean['timestamp'])

    # Extraction des caractéristiques temporelles
    df_clean['hour'] = df_clean['timestamp'].dt.hour
    df_clean['day_of_week'] = df_clean['timestamp'].dt.dayofweek
    df_clean['month'] = df_clean['timestamp'].dt.month
    df_clean['is_weekend'] = df_clean['day_of_week'].isin([5, 6]).astype(int)

    # Vérification des valeurs manquantes
    print("\n🔍 Valeurs manquantes par colonne :")
    missing = df_clean.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else "✅ Aucune valeur manquante")

    # Imputation des valeurs manquantes
    if missing.sum() > 0:
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if df_clean[col].dtype in ['float64', 'int64']:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                else:
                    df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)

    # Traitement des valeurs aberrantes
    df_clean = handle_outliers(df_clean, method=outlier_method)

    # Suppression des doublons
    initial_rows = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    removed_duplicates = initial_rows - len(df_clean)
    if removed_duplicates > 0:
        print(f"\n📊 {removed_duplicates} doublons supprimés")

    return df_clean

# 5. TRANSFORMATION DES DONNÉES
def transform_data(df):
    """Transforme les données pour l'analyse"""
    df_transformed = df.copy()

    # Catégorisation des variables
    def categorize_aqi(aqi):
        if aqi <= 50:
            return 'Bon'
        elif aqi <= 100:
            return 'Modéré'
        elif aqi <= 150:
            return 'Mauvais'
        else:
            return 'Dangereux'

    df_transformed['aqi_category'] = df_transformed['air_quality_index'].apply(categorize_aqi)

    def categorize_speed(speed):
        if speed <= 20:
            return 'Lente'
        elif speed <= 35:
            return 'Normale'
        else:
            return 'Rapide'

    df_transformed['speed_category'] = df_transformed['speed_kmh'].apply(categorize_speed)

    def categorize_traffic(density):
        if density <= 0.25:
            return 'Fluide'
        elif density <= 0.5:
            return 'Modéré'
        else:
            return 'Dense'

    df_transformed['traffic_category'] = df_transformed['traffic_density'].apply(categorize_traffic)

    # Encodage
    le = LabelEncoder()
    df_transformed['weather_encoded'] = le.fit_transform(df_transformed['weather'])

    return df_transformed

# 6. CRÉATION DE FEATURES
def create_features(df):
    """Crée de nouvelles features"""
    df_features = df.copy()

    df_features['speed_traffic_product'] = df_features['speed_kmh'] * df_features['traffic_density']
    df_features['traffic_aqi_flag'] = ((df_features['traffic_density'] < 0.2) & 
                                      (df_features['air_quality_index'] > 70)).astype(int)

    # Heures de pointe
    def is_rush_hour(hour):
        return 1 if (7 <= hour <= 9) or (17 <= hour <= 19) else 0

    df_features['is_rush_hour'] = df_features['hour'].apply(is_rush_hour)

    # Moment de la journée
    def time_of_day(hour):
        if 5 <= hour < 12:
            return 'Matin'
        elif 12 <= hour < 17:
            return 'Après-midi'
        elif 17 <= hour < 22:
            return 'Soir'
        else:
            return 'Nuit'

    df_features['time_of_day'] = df_features['hour'].apply(time_of_day)



    return df_features

# 7. PIPELINE ML AVEC ROBUSTSCALER POUR OUTLIERS
def create_ml_pipeline(outlier_robust=True):
    """Crée un pipeline ML robuste aux outliers"""

    numeric_features = ['speed_kmh', 'traffic_density', 'air_quality_index',
                       'latitude', 'longitude', 'hour', 'speed_traffic_product']
    categorical_features = ['weather', 'aqi_category', 'speed_category',
                           'traffic_category', 'time_of_day']

    # Utilisation de RobustScaler pour les outliers
    if outlier_robust:
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),  # Median plus robuste
            ('scaler', RobustScaler())  # Meilleur pour les outliers que StandardScaler
        ])
    else:
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())
        ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', LabelEncoder())
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor

# 8. ANALYSE DES OUTLIERS DÉTAILLÉE
def detailed_outlier_analysis(df):
    """Analyse détaillée des valeurs aberrantes"""

    numerical_cols = ['speed_kmh', 'traffic_density', 'air_quality_index', 'speed_traffic_product']

    print("\n📊 ANALYSE DÉTAILLÉE DES VALEURS ABERRANTES")
    print("=" * 60)

    for col in numerical_cols:
        if col in df.columns:
            data = df[col].dropna()

            # Statistiques
            stats_dict = {
                'Moyenne': data.mean(),
                'Médiane': data.median(),
                'Std': data.std(),
                'Min': data.min(),
                'Max': data.max(),
                'Q1': data.quantile(0.25),
                'Q3': data.quantile(0.75),
                'IQR': data.quantile(0.75) - data.quantile(0.25),
                'Skewness': data.skew(),
                'Kurtosis': data.kurtosis()
            }

            print(f"\n📈 {col}:")
            for key, value in stats_dict.items():
                print(f"  {key}: {value:.4f}")

            # Détection IQR
            Q1 = stats_dict['Q1']
            Q3 = stats_dict['Q3']
            IQR = stats_dict['IQR']
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_percentage = (len(outliers) / len(df)) * 100

            print(f"  Outliers (IQR): {len(outliers)} ({outlier_percentage:.2f}%)")
            print(f"  Plage normale: [{lower_bound:.4f}, {upper_bound:.4f}]")

            # Visualisation textuelle
            if len(outliers) > 0:
                print(f"  Exemples d'outliers: {outliers[col].head(5).values}")

# 9. PIPELINE COMPLET
def run_full_pipeline(file_path, outlier_method='winsorize', outlier_robust=True):
    """Exécute le pipeline complet avec traitement des outliers"""

    print("🚀 DÉMARRAGE DU PIPELINE AVEC TRAITEMENT DES OUTLIERS")
    print("=" * 70)
    print(f"📌 Méthode de traitement des outliers: {outlier_method}")
    print(f"📌 RobustScaler pour ML: {outlier_robust}")

    # Étape 1: Chargement
    df = load_data(file_path)

    # Étape 2: Vérification types (NOUVELLE ÉTAPE)
    def validate_data_types(df):
        print("\n🔍 VÉRIFICATION DES TYPES DE DONNÉES")
        print("=" * 50)
        
        # Affichage des types actuels
        type_report = pd.DataFrame({
            'Colonne': df.columns,
            'Type Actuel': df.dtypes.values,
            'Valeurs Uniques': [df[col].nunique() for col in df.columns],
            'Exemple': [df[col].iloc[0] if not df[col].empty else 'N/A' for col in df.columns]
        })
        print("📋 Types avant conversion :")
        print(type_report.to_string())
        
        # Conversions critiques
        conversions = []
        
        # Vérifier timestamp
        if not pd.api.types.is_datetime64_any_dtype(df['timestamp']):
            conversions.append(('timestamp', 'datetime'))
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
        
        # Vérifier les colonnes numériques
        numeric_cols = ['speed_kmh', 'traffic_density', 'air_quality_index', 
                        'latitude', 'longitude']
        
        for col in numeric_cols:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                current_type = str(df[col].dtype)
                conversions.append((col, f'float (était {current_type})'))
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Rapport des conversions
        if conversions:
            print("\n🔄 Conversions appliquées :")
            for col, conversion in conversions:
                print(f"  • {col} → {conversion}")
        else:
            print("\n✅ Tous les types sont corrects")
        
        # Affichage final
        print(f"\n📊 Types après conversion :")
        print(df.dtypes.to_string())
        
        return df

    # Puis modifiez run_full_pipeline() pour l'inclure :
    
    

    # Étape 3: Analyse initiale des outliers
    print("\n🔍 ANALYSE INITIALE DES OUTLIERS")
    detailed_outlier_analysis(df)

    # Étape 3: Nettoyage avec traitement des outliers
    df = clean_data(df, outlier_method=outlier_method)

    # Étape 4: Transformation
    df = transform_data(df)

    # Étape 5: Création de features
    df = create_features(df)
    df = validate_data_types(df)

    # Étape 6: Analyse après traitement
    print("\n🔍 ANALYSE APRÈS TRAITEMENT DES OUTLIERS")
    detailed_outlier_analysis(df)

    # Étape 7: Pipeline ML robuste
    preprocessor = create_ml_pipeline(outlier_robust=outlier_robust)

    print("\n" + "=" * 70)
    print("✅ PIPELINE TERMINÉ AVEC SUCCÈS")
    print(f"📋 Données finales : {df.shape[0]} lignes, {df.shape[1]} colonnes")

    return df, preprocessor

# 10. EXPORT DES RÉSULTATS
def export_results(df, output_path='processed_mobility_data_with_outliers.csv'):
    """Exporte les données traitées"""
    df.to_csv(output_path, index=False)
    print(f"\n💾 Données exportées vers : {output_path}")

# 11. EXÉCUTION AVEC OPTIONS
if __name__ == "__main__":
    INPUT_FILE = "C:/Users/PC/Desktop/Bootcamp_FN/mobility_urban_pollution_300.xlsx"

    # Options de traitement des outliers
    METHODS = {
        'winsorize': 'Winsorization (remplacement par percentiles)',
        'cap': 'Capping IQR (troncature des extrêmes)',
        'log': 'Transformation logarithmique',
        'remove': 'Suppression des outliers'
    }

    print("🎯 OPTIONS DE TRAITEMENT DES OUTLIERS")
    print("=" * 50)
    for key, value in METHODS.items():
        print(f"  {key}: {value}")

    # Choix de la méthode (vous pouvez le rendre interactif)
    chosen_method = 'winsorize'  # Par défaut
    # Pour rendre interactif : chosen_method = input("\nChoisissez une méthode: ")

    try:
        # Exécution avec la méthode choisie
        processed_data, ml_pipeline = run_full_pipeline(
            INPUT_FILE,
            outlier_method=chosen_method,
            outlier_robust=True
        )

        # Affichage d'échantillon
        print("\n📄 Échantillon des données traitées :")
        print(processed_data[['speed_kmh', 'traffic_density', 'air_quality_index',
                              'weather', 'aqi_category']].head())

        # Export
        export_results(processed_data, f"mobility_data_processed_{chosen_method}.csv")

        print(f"\n🛠️ Pipeline ML créé avec RobustScaler: {ml_pipeline}")

    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        import traceback
        traceback.print_exc()