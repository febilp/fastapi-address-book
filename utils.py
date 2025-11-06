"""
utils.py
---------
Utility functions for geolocation and distance calculations.
Includes logging to monitor geodesic computations.
"""


from geopy.distance import geodesic
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def within_distance(lat1: float, lon1: float, lat2: float, lon2: float, radius_km: float) -> bool:
    """
    Determine whether two geographic points are within a specified distance.

    Args:
        lat1 (float): Latitude of the first point.
        lon1 (float): Longitude of the first point.
        lat2 (float): Latitude of the second point.
        lon2 (float): Longitude of the second point.
        radius_km (float): Maximum distance in kilometers to compare.

    Returns:
        bool: True if the distance between the points is within radius_km, else False.
    """

    # Calculate the geodesic distance between two points (in kilometers)
    distance = geodesic((lat1, lon1), (lat2, lon2)).km
    logger.debug(f"Distance between ({lat1}, {lon1}) and ({lat2}, {lon2}): {distance:.2f} km")

    # Return True if distance is less than or equal to the allowed radius
    return distance <= radius_km
