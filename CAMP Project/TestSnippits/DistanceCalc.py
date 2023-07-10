import math

def euclidean_distance(lat1, lon1, alt1, lat2, lon2, alt2):
    # Convert latitude and longitude to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Earth's radius in kilometers
    earth_radius = 6371

    # Convert altitude from feet to meters
    alt1_m = alt1 * 0.3048
    alt2_m = alt2 * 0.3048

    # Calculate the horizontal (latitude-longitude) distance
    distance_ll = math.acos(math.sin(lat1_rad) * math.sin(lat2_rad) +
                            math.cos(lat1_rad) * math.cos(lat2_rad) *
                            math.cos(lon2_rad - lon1_rad)) * earth_radius

    # Calculate the vertical (altitude) distance in meters
    distance_alt = abs(alt2_m - alt1_m)

    # Calculate the combined distance using the Euclidean formula
    distance_combined = math.sqrt(distance_ll**2 + distance_alt**2)

    return distance_combined

# Heathrow Airport (LHR) coordinates
lat1 = 51.4700
lon1 = -0.4543
alt1 = 81.73

# Newark Liberty International Airport (EWR) coordinates
lat2 = 40.6895
lon2 = -74.1745
alt2 = 8.72

# Calculate the combined distance
distance_combined = euclidean_distance(lat1, lon1, alt1, lat2, lon2, alt2)

print("Combined Distance: {:.2f} kilometers".format(distance_combined))