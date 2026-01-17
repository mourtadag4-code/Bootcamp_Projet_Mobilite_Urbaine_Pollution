# Documentation Technique du Pipeline

## Flux de Données
1. **Entrée** : `mobility_urban_pollution_300.xlsx` (300 rows × 8 cols)
2. **Nettoyage** : 
   - Conversion dates/heures
   - Traitement outliers (méthode: winsorize)
   - Colonnes impactées: speed_kmh, traffic_density, air_quality_index
3. **Transformation** :
   - Catégories AQI (Bon/Modéré/Mauvais)
   - Catégories vitesse (Lente/Normale/Rapide)
   - Feature: `speed_traffic_product` (multiplication, pas division)
4. **Sortie** :
   - MySQL: table `mobility_processed` (schéma ci-dessous)
   - CSV: `mobility_data_processed_winsorize.csv`

## Schéma MySQL
sql
 CREATE TABLE mobility_processed (
    id INT AUTO_INCREMENT PRIMARY KEY,
    route_id VARCHAR(10),
    timestamp DATETIME,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    speed_kmh DECIMAL(5,2),
    traffic_density DECIMAL(3,2),
    air_quality_index SMALLINT,
    weather VARCHAR(20),
    hour TINYINT,
    day_of_week TINYINT,
    month TINYINT,
    is_weekend BOOLEAN,
    aqi_category VARCHAR(15),
    speed_category VARCHAR(10),
    traffic_category VARCHAR(10),
    weather_encoded TINYINT,
    speed_traffic_product DECIMAL(8,4),
    traffic_aqi_flag BOOLEAN,
    is_rush_hour BOOLEAN,
    time_of_day VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


