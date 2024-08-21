import math

def euclidean_distance(easting1, northing1, easting2, northing2):
    return math.sqrt((easting2 - easting1) ** 2 + (northing2 - northing1) ** 2)

def is_within_radius(easting1, northing1, easting2, northing2, radius=5):
    distance = euclidean_distance(easting1, northing1, easting2, northing2)
    return distance <= radius
#
# def haversine(lat1, lon1, lat2, lon2):
#     # Convert latitude and longitude from degrees to radians
#     lat1 = math.radians(lat1)
#     lon1 = math.radians(lon1)
#     lat2 = math.radians(lat2)
#     lon2 = math.radians(lon2)
#
#     # Haversine formula
#     dlat = lat2 - lat1
#     dlon = lon2 - lon1
#     a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
#     c = 2 * math.asin(math.sqrt(a))
#
#     # Radius of earth in meters (mean radius)
#     R = 6371000
#
#     # Distance in meters
#     distance = R * c
#
#     return distance
#
# def is_within_radius(lat1, lon1, lat2, lon2, radius=5):
#     distance = haversine(lat1, lon1, lat2, lon2)
#     return distance <= radius
