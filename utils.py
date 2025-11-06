from geopy.distance import geodesic

def within_distance(lat1, lon1, lat2, lon2, radius_km):
    distance = geodesic((lat1, lon1), (lat2, lon2)).km
    return distance <= radius_km
