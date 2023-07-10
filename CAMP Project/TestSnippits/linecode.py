import folium

# Create a map
m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

# Define the coordinates of the two points
point1 = [51.4700, -0.4543]
point2 = [40.6895, -74.1745]

# Create a line between the two points
line = folium.PolyLine(locations=[point1, point2], color='blue')
line.add_to(m)

# Calculate the distance between the two points
distance = 1234.56  # Replace with your actual distance calculation

# Calculate the midpoint coordinates
midpoint = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]

# Add the distance value next to the line
folium.Marker(
    location=midpoint,
    icon=folium.DivIcon(
        icon_size=(150, 36),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12pt; font-weight: bold;">{:.2f} km</div>'.format(distance)
    )
).add_to(m)

# Save the map as an HTML file
m.save('map.html')
