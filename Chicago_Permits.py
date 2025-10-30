import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import matplotlib.pyplot as plt
import seaborn as sns
import io

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Chicago Permits Dashboard",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# LOAD DATA
# -------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

st.title("🏙️ Chicago Permits Data Dashboard")
st.caption("An interactive data visualization app built with Streamlit, Pandas, and Folium")

# -------------------------------
# SIDEBAR FILTERS
# -------------------------------
st.sidebar.header("🔍 Filter Data")
app_type = st.sidebar.selectbox(
    "Select Application Type:",
    options=["All"] + sorted(df["APPLICATIONTYPE"].dropna().unique().tolist())
)
status = st.sidebar.selectbox(
    "Select Application Status:",
    options=["All"] + sorted(df["APPLICATIONSTATUS"].dropna().unique().tolist())
)

# Apply filters
filtered_df = df.copy()
if app_type != "All":
    filtered_df = filtered_df[filtered_df["APPLICATIONTYPE"] == app_type]
if status != "All":
    filtered_df = filtered_df[filtered_df["APPLICATIONSTATUS"] == status]

st.write(f"### Showing {len(filtered_df)} records after filtering")

# -------------------------------
# METRICS
# -------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Permits", len(df))
col2.metric("Active Permits", len(df[df["APPLICATIONSTATUS"] == "ACTIVE"]))
col3.metric("Finalized Permits", len(df[df["APPLICATIONSTATUS"] == "FINALIZED"]))

# -------------------------------
# DATASET SUMMARY INFO
# -------------------------------
st.subheader("📈 Dataset Summary Info")
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())

# -------------------------------
# VISUALS
# -------------------------------
st.subheader("📊 Permit Distribution by Application Type")
plt.figure(figsize=(10, 4))
sns.countplot(y="APPLICATIONTYPE", data=df, order=df["APPLICATIONTYPE"].value_counts().index)
st.pyplot(plt)

# -------------------------------
# MAP VISUALIZATION (INTERACTIVE)
# -------------------------------
st.subheader("🗺️ Permit Locations in Chicago")

# Clean coordinate data
filtered_df = filtered_df.dropna(subset=["LATITUDE", "LONGITUDE"])

if not filtered_df.empty:
    m = folium.Map(location=[filtered_df["LATITUDE"].mean(), filtered_df["LONGITUDE"].mean()],
                   zoom_start=10, tiles="CartoDB positron")
    for _, row in filtered_df.head(500).iterrows():  # show only first 500 for performance
        folium.CircleMarker(
            location=[row["LATITUDE"], row["LONGITUDE"]],
            radius=3,
            popup=row["APPLICATIONTYPE"],
            color="blue",
            fill=True,
            fill_opacity=0.6
        ).add_to(m)
    folium_static(m)
else:
    st.warning("No location data available for selected filters.")

# -------------------------------
# DATA PREVIEW
# -------------------------------
st.subheader("🔢 Data Preview")
st.dataframe(filtered_df.head(50))

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("**Built by [Sumit Chaurasiya](https://github.com/sumit-chaurasiya-04)** | Powered by Streamlit 🚀")
