import pandas as pd

import os

DATA_PATH = os.path.join(os.path.dirname(__file__), 'dataset.csv')
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"dataset.csv not found at {DATA_PATH}. Place the file in the project root or update the path.")

df = pd.read_csv(DATA_PATH, low_memory=False)
df.info()
df.head()

#Clean and concvert date and columns
df['APPLICATIONSTARTDATE'] = pd.to_datetime(df['APPLICATIONSTARTDATE'], errors='coerce')

df['APPLICATIONENDDATE'] = pd.to_datetime(df['APPLICATIONENDDATE'], errors='coerce')

#Create new columns
df['DURATION_DAYS'] = (df['APPLICATIONENDDATE'] - df['APPLICATIONSTARTDATE']).dt.days
df['START_MONTH'] = (df['APPLICATIONSTARTDATE']).dt.month
df['START_YEAR'] = (df['APPLICATIONSTARTDATE']) .dt.year
df['WEEKDAY'] = (df['APPLICATIONSTARTDATE']).dt.day_name()

#Drop rows with missing essential dates
df = df.dropna(subset=['APPLICATIONSTARTDATE', 'APPLICATIONENDDATE'])

#Simple EDA Examples

import matplotlib.pyplot as plt

df['APPLICATIONTYPE'].value_counts().head(10).plot(kind='barh')
plt.title('Top 10 permit types')
plt.xlabel('Number of permits')
plt.ylabel('Permit Type')
plt.tight_layout()
plt.show()

#Monthly Permits Trends

df.groupby('START_MONTH').size().plot(kind='bar')
plt.title('Permits Issued by Month')
plt.xlabel('Month')
plt.ylabel('Number of Permits')
plt.tight_layout()
plt.show()

#Duration of Permits

df['DURATION_DAYS'].hist(bins=30)
plt.title('Permit Duration Distribution')
plt.xlabel('Days')
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()


#BONUS: Plot Permits on a Map

import folium

#Center map of Chicago
map_chicago = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

#Plot 100 permit points (for performance)
for _, row in df. dropna(subset=['LATITUDE','LONGITUDE']).head(100).iterrows():
    folium.CircleMarker(
        location = [row['LATITUDE'], row['LONGITUDE']],
        radius = 3,
        popup = row['APPLICATIONTYPE'],
        color = 'blue',
        fill = True
    ).add_to(map_chicago)

map_chicago.save('chicago-permits_map.html')
print("Map saved as chicago_permits_map.html")

df.describe().to_csv('summary_stats.csv')
