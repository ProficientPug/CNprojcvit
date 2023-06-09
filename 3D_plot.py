import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Import Axes3D from mpl_toolkits.mplot3d instead of mpl_toolkits.basemap
import pandas as pd

# Read CSV file
data = pd.read_csv(r"X:\New folder\Cn-project\dataset.csv")

# Extract latitude, longitude, and altitude values
latitudes = data['Latitude']
longitudes = data['Longitude']
altitudes = data['Altitude']

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot latitude, longitude, and altitude
ax.scatter(longitudes, latitudes, altitudes)

# Set plot labels
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_zlabel('Altitude')

# Show the plot
plt.show()