import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
import streamlit as st
import streamlit.components.v1 as components

# --- Streamlit Page Setup ---
st.set_page_config(page_title="Chicago Permits Dashboard", layout="wide")
st.title("🏙️ Chicago Permits Data Visualization Dashboard")
st.markdown("Explore the dataset, charts, and interactive Folium map below.")

# --- Load Dataset ---
df = pd.read_csv("dataset.csv")
st.subheader("📊 Dataset Overview")
st.dataframe(df.head(20))

# --- Basic Info ---
st.subheader("📈 Dataset Summary Info")
buffer = []
df.info(buf=buffer)
info_str = "\n".join(buffer)
st.text(info_str)

# --- Visualization 1: Application Types ---
st.subheader("🔹 Application Type Distribution")
fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.countplot(data=df, x="APPLICATIONTYPE", order=df["APPLICATIONTYPE"].value_counts().index[:10])
plt.xticks(rotation=45)
st.pyplot(fig1)

# --- Visualization 2: Application Status ---
st.subheader("🔹 Application Status Counts")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.countplot(data=df, x="APPLICATIONSTATUS", order=df["APPLICATIONSTATUS"].value_counts().index[:10])
plt.xticks(rotation=45)
st.pyplot(fig2)

# --- Visualization 3: Work Type Description ---
st.subheader("🔹 Work Type Description Frequency")
fig3, ax3 = plt.subplots(figsize=(10, 4))
sns.countplot(data=df, x="WORKTYPEDESCRIPTION", order=df["WORKTYPEDESCRIPTION"].value_counts().index[:10])
plt.xticks(rotation=45)
st.pyplot(fig3)

# --- Map Section ---
st.subheader("🗺️ Chicago Permits Interactive Map")
st.markdown("Generating map... please wait ⏳")

# Create map (Folium)
m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
for _, row in df.dropna(subset=['LATITUDE', 'LONGITUDE']).head(500).iterrows():
    folium.CircleMarker(
        location=[row['LATITUDE'], row['LONGITUDE']],
        radius=2,
        color='blue',
        fill=True,
        fill_opacity=0.7
    ).add_to(m)

m.save("chicago_permits_map.html")

# --- Embed Map ---
with open("chicago_permits_map.html", "r", encoding="utf-8") as f:
    html_data = f.read()

components.html(html_data, height=600)

st.success("✅ Map successfully generated and displayed!")
