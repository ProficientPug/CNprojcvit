import folium

# Create a map centered on a specific location
map = folium.Map( zoom_start=10)

# Create a feature group for the pin markers
pin_group = folium.FeatureGroup()

# Define a custom JavaScript callback function
callback = """
function toggleMarkerVisibility(e) {
    var marker = e.target;
    if (marker.options.opacity == 1) {
        marker.setOpacity(0);
    } else {
        marker.setOpacity(1);
    }
}
"""

# Add the custom JavaScript callback to the map
folium.Map.add_child(map, folium.Element(callback))

# Add the pin marker with the custom JavaScript callback and tooltip
pin_marker = folium.Marker(
    [0, 0],
    tooltip='Click to show/hide',
    icon=folium.Icon(color='red'),
    options={'click': callback}
)
pin_marker.add_to(pin_group)
pin_marker.add_child(folium.Popup('Pin Marker'))

# Add the feature group to the map
pin_group.add_to(map)

# Display the map
map.save("map.html")
