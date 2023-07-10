import csv
L=[]

import folium

# Create a map centered on the specified location
map = folium.Map(location=[4.58947668e+01, -3.83144143e+01], zoom_start=5)

folium.Marker([51.4700, -0.4543], tooltip='Heathrow airport (LHR)', icon=folium.Icon(icon="globe",color='red',icon_size=(50, 50))).add_to(map)
folium.Marker([40.6895, -74.1745], tooltip='Newark Liberty International Airport (EWR)', icon=folium.Icon(icon="globe",color='red',icon_size=(50, 50))).add_to(map)


# Open the CSV file
with open('data.csv', 'r', encoding='utf-8') as file:
    # Create a CSV reader
    csv_reader = csv.reader(file)

    # Read each row in the CSV file
    for row in csv_reader:
        # Access data in each row
        L=row[0].split()
        # Add a marker for the latitude and longitude
        folium.Marker([L[3], L[4]],tooltip=L[0],icon=folium.Icon(icon="plane" ,color='blue')).add_to(map)
# Display the map
map.save("Allplanes.html")