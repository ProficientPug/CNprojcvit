import folium

# Create a map centered on the specified location
map = folium.Map(location=[51.393644, -14.5025405], zoom_start=10)

# Add a marker for the latitude and longitude
folium.Marker([51.393644, -14.5025405]).add_to(map)

# Display the map
map.save("map.html")
