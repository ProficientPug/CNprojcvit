import csv,math,folium,random

#Variables
rc=[] #Read csv List
dl=[] #distance list
planenolist=[]
rowlist=[]
# Heathrow Airport (LHR) coordinates
LHR=["LHR",1530270000.000000000000,81.73,51.4700,-0.4543] #Alt Lat Long
# Newark Liberty International Airport (EWR) coordinates
EWR=["EWR",1530270000.000000000000,8.72,40.6895,-74.1745] #Alt Lat Long

#functions
def TRLD(distance): #Transimssion rate list Data
    TRL=[[1,"red",500,31.895],[2,"orange",400,43.505],[3,"yellow",300,52.857],[4,"green",190,63.970],[5,"blue",90,77.071],[6,"pink",35,93.854],[7,"purple",5.56,119.130]] #Transmission Rate List
    for a in TRL:
        if distance>=a[2]:
            return a

def linemaker(P1=[],P2=[],distance=0,m=0):
    # Define the coordinates of the two points
    point1 = [P1[3],P1[4]]
    point2 = [P2[3],P2[4]]

    # Create a line between the two points
    line = folium.PolyLine(locations=[point1, point2], color=TRLD(distance)[1])
    line.add_to(m)

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
    return 0

def euclidean_distance(P1=[],P2=[]):
    # Convert latitude and longitude to radians
    lat1_rad = math.radians(P1[3])
    lon1_rad = math.radians(P1[4])
    lat2_rad = math.radians(P2[3])
    lon2_rad = math.radians(P2[4])
    # Earth's radius in kilometers
    earth_radius = 6371
    # Convert altitude from feet to meters
    alt1_m = P1[2] * 0.3048
    alt2_m = P2[2] * 0.3048
    #print(P1,P2)
    #print(f"Latitude (radians): {lat1_rad}, Longitude (radians): {lon1_rad}, Altitude: {alt1_m}")
    #cleprint(f"Latitude (radians): {lat2_rad}, Longitude (radians): {lon2_rad}, Altitude: {alt2_m}")
    # Calculate the horizontal (latitude-longitude) distance
    distance_ll = math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
                            math.cos(lat1_rad) * math.cos(lat2_rad) *
                            math.cos(lon2_rad - lon1_rad)) * earth_radius
    distance_alt = abs(alt2_m - alt1_m) # Calculate the vertical (altitude) distance in meters
    distance_combined = math.sqrt(distance_ll**2 + distance_alt**2) # Calculate the combined distance using the Euclidean formula

    return distance_combined

with open('data.csv', 'r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        nm=row[0].split() #numbermaker
        planenolist+=[nm[0]]
        rc.append([nm[0], float(nm[1]), float(nm[2]), float(nm[3]), float(nm[4])])
rc.append(LHR)
rc.append(EWR)
#print(rc)

#Distance list maker
for plane1 in rc:
    rowlist=[]
    for plane2 in rc:
        if plane1==plane2:
            rowlist+=[0]
        else:
            rowlist+=[euclidean_distance(plane1,plane2)]
    dl.append(rowlist)

#Csv writer
'''
with open('distance.csv', 'w', encoding='utf-8', newline='') as file:
    csv_writer = csv.writer(file)
    # Write each row from the nested list
    for row in dl:
        csv_writer.writerow(row)
'''

def dataopt(planeno=random.choice(planenolist)):
    if planeno in planenolist:
        planeindex=planenolist.index(planeno)
        map = folium.Map(location=[4.58947668e+01, -3.83144143e+01], zoom_start=5)
        folium.Marker([LHR[3], LHR[4]], tooltip='Heathrow airport (LHR)', icon=folium.Icon(icon="globe",color='red',icon_size=(50, 50))).add_to(map)
        folium.Marker([EWR[3], EWR[4]], tooltip='Newark Liberty International Airport (EWR)', icon=folium.Icon(icon="globe",color='red',icon_size=(50, 50))).add_to(map)
        folium.Marker([rc[planeindex][3], rc[planeindex][4]],tooltip=rc[planeindex][0],icon=folium.Icon(icon="plane" ,color='blue')).add_to(map)
        if dl[planeindex][149]< dl[planeindex][150]: #150 is LHR
            GroundStation=LHR
        else:
            GroundStation=EWR
        print(dl[planeindex][149])
        print(GroundStation)
        linemaker(rc[planeindex],GroundStation,min(dl[planeindex][149],dl[planeindex][150]),map)
        for a in planenolist:
            if a==planeno:
                continue
            







        map.save("map.html")
    

dataopt()