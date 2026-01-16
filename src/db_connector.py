!pip install pymysql

from sqlalchemy import create_engine
# Connexion à MySQL local
def connect_to_mysql():
    """Établit la connexion à MySQL"""
    try:
        engine = create_engine("mysql+pymysql://root@localhost/mobility_db")
        connection = engine.connect()
        print("✅ Connecté à MySQL avec succès")
        return engine, connection
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None, None

# Tester la connexion
engine, conn = connect_to_mysql()

def save_to_existing_table(df, table_name='mobility_processed'):
    """Insère dans la table existante avec mapping des colonnes"""
    
    # Vérifier les colonnes
    print("📋 Colonnes disponibles dans vos données:")
    print(df.columns.tolist())
    
    # Mapping entre vos colonnes et la table
    column_mapping = {
        'route_id': 'route_id',
        'timestamp': 'timestamp',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'speed_kmh': 'speed_kmh',
        'traffic_density': 'traffic_density',
        'air_quality_index': 'air_quality_index',
        'weather': 'weather',
        'hour': 'hour',
        'day_of_week': 'day_of_week',
        'month': 'month',
        'is_weekend': 'is_weekend',
        'aqi_category': 'aqi_category',
        'speed_category': 'speed_category',
        'traffic_category': 'traffic_category',
        'weather_encoded': 'weather_encoded',
        'speed_traffic_product': 'speed_traffic_product',
        'traffic_aqi_flag': 'traffic_aqi_flag',
        'is_rush_hour': 'is_rush_hour',
        'time_of_day': 'time_of_day'
        # 'created_at' sera auto-généré
    }
    
    # Sélectionner et renommer les colonnes
    df_to_insert = df[list(column_mapping.keys())].rename(columns=column_mapping)
    
    # Connexion MySQL
    engine = create_engine("mysql+pymysql://root@localhost/mobility_db")
    
    # Insérer avec append (ne pas remplacer la table)
    df_to_insert.to_sql(table_name, 
                       engine, 
                       if_exists='append',  # ← CRUCIAL: 'append' pas 'replace'
                       index=False)
    
    # Vérifier
    count = pd.read_sql(f"SELECT COUNT(*) as count FROM {table_name}", engine)
    print(f"✅ {len(df_to_insert)} lignes insérées")
    print(f"📊 Total dans la table: {count['count'][0]} lignes")
    
    engine.dispose()
    return True

# Utilisation
save_to_existing_table(processed_data)