import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuration de la page
st.set_page_config(page_title="Dashboard Mobilité Urbaine", layout="wide")

# --- CHARGEMENT DES DONNÉES ---
# Remplacer par : df = pd.read_csv("votre_fichier.csv")
@st.cache_data
def load_data():
    # Simulation de données pour l'exemple
    import numpy as np
    data = {
        'route_id': np.random.randint(1, 10, 1000),
        'timestamp': pd.date_range(start='2023-01-01', periods=1000, freq='H'),
        'latitude': np.random.uniform(48.85, 48.86, 1000),
        'longitude': np.random.uniform(2.33, 2.35, 1000),
        'speed_kmh': np.random.uniform(10, 50, 1000),
        'traffic_density': np.random.uniform(0, 100, 1000),
        'air_quality_index': np.random.uniform(20, 150, 1000),
        'weather': np.random.choice(['Dégagé', 'Pluie', 'Brouillard'], 1000),
        'hour': np.random.randint(0, 24, 1000),
        'day_of_week': np.random.choice(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'], 1000),
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR (FILTRES) ---
st.sidebar.header("🔍 Filtres Interactifs")
selected_hour = st.sidebar.slider("Heure de la journée", 0, 23, (0, 23))
selected_day = st.sidebar.multiselect("Jour de la semaine", df['day_of_week'].unique(), default=df['day_of_week'].unique())
selected_weather = st.sidebar.multiselect("Météo", df['weather'].unique(), default=df['weather'].unique())

# Filtrage du dataset
filtered_df = df[
    (df['hour'].between(selected_hour[0], selected_hour[1])) &
    (df['day_of_week'].isin(selected_day)) &
    (df['weather'].isin(selected_weather))
]

# --- TITRE DU DASHBOARD ---
st.title("🚦 Analyse de la Mobilité Urbaine et Environnementale")
st.markdown("---")

# --- SECTION 1 : ANALYSE DES CORRÉLATIONS ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔗 Corrélations Variables Clés")
    corr = filtered_df[['speed_kmh', 'traffic_density', 'air_quality_index']].corr()
    fig_corr = px.imshow(corr, text_auto=True, color_continuous_scale='RdBu_r', aspect="auto")
    st.plotly_chart(fig_corr, use_container_width=True)

with col2:
    st.subheader("📉 Densité vs Qualité de l'Air")
    fig_scatter = px.scatter(filtered_df, x="traffic_density", y="air_quality_index", 
                             color="speed_kmh", hover_data=['hour'],
                             color_continuous_scale="Viridis", 
                             labels={'traffic_density': 'Densité Trafic', 'air_quality_index': 'Indice Qualité Air'})
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- SECTION 2 : TENDANCES TEMPORELLES ---
st.markdown("---")
col3, col4 = st.columns(2)

with col3:
    st.subheader("🕒 Vitesse Moyenne par Heure")
    hourly_speed = filtered_df.groupby('hour')['speed_kmh'].mean().reset_index()
    fig_line = px.line(hourly_speed, x='hour', y='speed_kmh', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with col4:
    st.subheader("📅 Densité Trafic par Jour")
    day_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    daily_traffic = filtered_df.groupby('day_of_week')['traffic_density'].mean().reindex(day_order).reset_index()
    fig_bar = px.bar(daily_traffic, x='day_of_week', y='traffic_density', color='traffic_density')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- SECTION 3 : CARTOGRAPHIE ---
st.markdown("---")
st.subheader("🗺️ Cartographie des Zones Critiques")
# Création d'une colonne de statut pour la carte
filtered_df['status'] = filtered_df.apply(lambda row: 'Dense/Lent' if (row['traffic_density'] > 70 and row['speed_kmh'] < 20) else 'Normal', axis=1)

fig_map = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", 
                            color="traffic_density", size="air_quality_index",
                            color_continuous_scale=px.colors.cyclical.IceFire, 
                            size_max=15, zoom=13,
                            mapbox_style="carto-positron",
                            title="Densité (Couleur) et Pollution (Taille)")
st.plotly_chart(fig_map, use_container_width=True)