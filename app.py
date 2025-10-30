import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

import os

# Load data
DATA_PATH = os.path.join(os.path.dirname(__file__), 'dataset.csv')
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"dataset.csv not found at {DATA_PATH}. Place the file in the project root or update the path.")

df = pd.read_csv(DATA_PATH, low_memory=False)
df['APPLICATIONSTARTDATE'] = pd.to_datetime(df['APPLICATIONSTARTDATE'], errors='coerce')
df['APPLICATIONENDDATE'] = pd.to_datetime(df['APPLICATIONENDDATE'], errors='coerce')
df['DURATION_DAYS'] = (df['APPLICATIONENDDATE'] - df['APPLICATIONSTARTDATE']).dt.days

# Sidebar filters
st.sidebar.title("Filters")
permit_type = st.sidebar.selectbox("Permit Type", df['APPLICATIONTYPE'].dropna().unique())
month = st.sidebar.selectbox("Start Month", df['APPLICATIONSTARTDATE'].dt.month_name().dropna().unique())

# Filtered data
filtered = df[
    (df['APPLICATIONTYPE'] == permit_type) &
    (df['APPLICATIONSTARTDATE'].dt.month_name() == month)
]

st.title("Chicago Permit Dashboard")
st.write(f"Showing {len(filtered)} permits for {permit_type} in {month}")

# Map
map_center = [41.8781, -87.6298]
m = folium.Map(location=map_center, zoom_start=11)
for _, row in filtered.dropna(subset=['LATITUDE', 'LONGITUDE']).head(100).iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=3,
        popup=row['APPLICATIONTYPE'],
        color='blue',
        fill=True
    ).add_to(m)
folium_static(m)

# Charts
st.subheader("Permit Duration Distribution")
st.bar_chart(filtered['DURATION_DAYS'].value_counts().sort_index())