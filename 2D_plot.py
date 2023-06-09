import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopandas import GeoDataFrame

import matplotlib.pyplot as plt

df = pd.read_csv(r"X:\New folder\Cn-project\dataset.csv", delimiter=',', skiprows=0, low_memory=False,encoding='unicode_escape')

geometry = [Point(xyz) for xyz in zip(df['Longitude'], df['Latitude'],df['Altitude'])]
airports = {'LHR': [0.4543,51.4700], 'EWR': [-74.1686,40.6925]}
airport_geometry = [Point(coords) for coords in airports.values()]
airport_gdf = GeoDataFrame(data=list(airports.keys()), geometry=airport_geometry, columns=['Airport'])
gdf = GeoDataFrame(df, geometry=geometry) 
print(gdf)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
base = world.plot(color='white', edgecolor='black')
gdf.plot(ax=base, marker='o', color='red', markersize=5)
airport_gdf.plot(ax = base,marker = 's',color = 'blue',markersize = 10,)
plt.show()