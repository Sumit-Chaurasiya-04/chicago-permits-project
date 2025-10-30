# Chicago Permit Project

A small Python data exploration and visualization project that analyzes building permit data for the City of Chicago. The project includes an exploratory script (`Chicago_Permits.py`) and an interactive Streamlit dashboard (`app.py`). Outputs include a simple Folium map (`chicago-permits_map.html`) and a CSV of summary statistics (`summary_stats.csv`).

Why this is resume‑worthy

- Real-world public dataset analysis with time-series and geospatial visualizations
- Built an interactive Streamlit dashboard and exported an interactive map
- Demonstrates data cleaning, EDA, and mapping skills useful for data science roles

Quick start

1. Create and activate a Python 3.8+ environment.

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

3. Run the exploratory script to produce the map and summary stats:

```powershell
python Chicago_Permits.py
```

4. Run the Streamlit dashboard:

```powershell
streamlit run app.py
```

Notes

- The project as-is reads `dataset.csv` from an absolute path (`F:/Sumit Python Programs/Project/dataset.csv`). Update the scripts to point to `dataset.csv` in the project root, or place the dataset at the same path.
- The repository includes `chicago-permits_map.html` and `summary_stats.csv` as example outputs.

Suggested resume blurb

"Built a data pipeline and interactive dashboard analyzing Chicago building permit records. Cleaned and processed time-series and geospatial data; produced an interactive Streamlit dashboard and Folium map demonstrating insights on permit types, monthly trends, and permit durations."
