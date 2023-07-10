import csv
import math
import folium
import random

# Variables
rc = []  # Read csv List
dl = []  # Distance list
planenolist = []
map = folium.Map()
datapath=[]

# Heathrow Airport (LHR) coordinates
LHR = ["LHR", 1530270000.000000000000, 81.73, 51.4700, -0.4543]  # Alt Lat Long
# Newark Liberty International Airport (EWR) coordinates
EWR = ["EWR", 1530270000.000000000000, 8.72, 40.6895, -74.1745]  # Alt Lat Long

# Functions
def TRLD(distance):
    # Transmission Rate List Data
    TRL = [
        [1, "red", 500, 31.895],
        [2, "orange", 400, 43.505],
        [3, "yellow", 300, 52.857],
        [4, "green", 190, 63.970],
        [5, "blue", 90, 77.071],
        [6, "pink", 35, 93.854],
        [7, "purple", 5.56, 119.130]
    ]
    for a in TRL:
        if distance >= a[2]:
            return a
    return TRL[-1]


def markermaker(Marker=LHR, icontype="plane"):
    global map
    icon_color = 'red' if icontype == 'globe' else 'blue'
    icon = 'globe' if icontype == 'globe' else 'plane'
    folium.Marker(
        location=[Marker[3], Marker[4]],tooltip=Marker[0],icon=folium.Icon(icon=icon, color=icon_color, icon_size=(30, 30))).add_to(map)

def linemaker(P1=LHR, P2=EWR):
    global map
    # Define the coordinates of the two points
    
    point1 = [P1[3], P1[4]]
    point2 = [P2[3], P2[4]]

    # Create a line between the two points
    line = folium.PolyLine(locations=[point1, point2], color=TRLD(haversine_distance(P1, P2))[1])
    line.add_to(map)

    # Calculate the midpoint coordinates
    midpoint = [(point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2]

    # Add the distance value next to the line
    folium.Marker(
        location=midpoint,
        icon=folium.DivIcon(
            icon_size=(150, 36),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12pt; font-weight: bold;">{:.2f} km</div>'.format(haversine_distance(P1, P2))
        )
    ).add_to(map)

def haversine_distance(P1, P2):
    # Convert latitude and longitude to radians
    lat1_rad = math.radians(P1[3])
    lon1_rad = math.radians(P1[4])
    lat2_rad = math.radians(P2[3])
    lon2_rad = math.radians(P2[4])

    # Earth's radius in kilometers
    earth_radius = 6371.0

    # Calculate the differences between latitudes and longitudes
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Calculate the Haversine formula components
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Calculate the distance using the Haversine formula
    distance = earth_radius * c

    return distance

def readcsv():
    global rc,planenolist
    with open(r'X:\Rohith\CAMP Project\Main Code\data.csv', 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            nm = row[0].split()
            planenolist.append(nm[0])
            rc.append([nm[0], float(nm[1]), float(nm[2]), float(nm[3]), float(nm[4])])
    rc.append(LHR)
    rc.append(EWR)

readcsv()

def distancelistmaker():
    # Distance list maker
    global dl,rc
    for plane1 in rc:
        rowlist = []
        for plane2 in rc:
            if plane1 == plane2:
                rowlist.append(0)
            else:
                rowlist.append(haversine_distance(plane1, plane2))
        dl.append(rowlist)

distancelistmaker()

def max_data_flow(P1=random.choice(rc), P2=LHR):
    global rc, datapath, minimum_dist, dl
    minimum_dist=10000
    if datapath == []:
        datapath.append(P1)
    planetobeadded = []
    for plane in rc:
        if plane not in datapath:
            if haversine_distance(P1, plane)<minimum_dist:
                minimum_dist = haversine_distance(P1, plane)
                planetobeadded = plane
                print(minimum_dist,planetobeadded)    
    datapath.append(planetobeadded)
    if rc[-2] in datapath or rc[-1] in datapath:
        return datapath
    return max_data_flow(planetobeadded)

def dataopt(planeno=random.choice(planenolist)):
    if planeno in planenolist:
        planeindex = planenolist.index(planeno)
        # Create the ground_station dictionary
        ground_station = {}
        for i, plane in enumerate(rc):
            if i != planeindex:
                plane_name = plane[0]  # Extract the plane name
                if plane_name not in ground_station:
                    ground_station[plane_name] = []
                ground_station[plane_name].append(plane)

        GroundStation = LHR if dl[planeindex][149] < dl[planeindex][150] else EWR

        max_data = max_data_flow(ground_station, rc[planeindex][0])  # Use plane name instead of the plane

print(max_data_flow(rc[135]))
print()
print()
print("Starting airplane ",datapath[0])

def mapmaker():
    global datapath
    for a in range(len(datapath)-1):
        markermaker(datapath[a])
        linemaker(datapath[a],datapath[a+1])
    markermaker(datapath[-1])

mapmaker()
'''
for a in range(len(datapath)-1):
    mapmaker()
    map.save(f"map{a}.html")
    for b in range(a,len(datapath)):
        if haversine_distance(datapath[a], datapath[b])<haversine_distance(datapath[a], datapath[a+1]) or haversine_distance(P1, P2):
            print()




for a in rc:
    markermaker(a)
    for b in rc:
        if a!=b:
            linemaker(a,b)
map.save("Minimummap.html")'''