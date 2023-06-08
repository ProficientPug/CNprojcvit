import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas import GeoDataFrame

import matplotlib.pyplot as plt

df = pd.read_csv(r"X:\New folder\dataset.csv", delimiter=',', skiprows=0, low_memory=False,encoding='unicode_escape')

geometry = [Point(xyz) for xyz in zip(df['Longitude'], df['Latitude'],df['Altitude'])]
gdf = GeoDataFrame(df, geometry=geometry) 
print(gdf)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
base = world.plot(color='white', edgecolor='black')
gdf.plot(ax=base, marker='o', color='red', markersize=5)

plt.show()