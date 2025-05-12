from src.keys import api_key
import requests
import json


class Routes:
    def __init__(self, midpoint):
        self.midpoint = midpoint

    def calculate_distance_to_midpoint(self):
        travel_distance = round(self.response['routes'][0]['distanceMeters'] / 1609)
        return travel_distance

    def calculate_traffic_to_midpoint(self):
        travel_time = self.response['routes'][0]['duration']
        if travel_time[-1].isalpha():
            travel_time = travel_time[:-1]
        travel_time = round(int(travel_time) / 60)
        return travel_time

    def calculate_route_to_midpoint(self, origin_coordinates):
        url = "https://routes.googleapis.com/directions/v2:computeRoutes"
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": api_key,
            "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
        }

        payload = {
            "origin": {
                "location": {
                    "latLng": {
                        "latitude": origin_coordinates[0],
                        "longitude": origin_coordinates[1]
                    }
                }
            },
            "destination": {
                "location": {
                    "latLng": {
                        "latitude": self.midpoint[0],
                        "longitude": self.midpoint[1]
                    }
                }
            },
            "travelMode": "DRIVE",
            "routingPreference": "TRAFFIC_AWARE",
            "computeAlternativeRoutes": False,
            "routeModifiers": {
                "avoidTolls": False,
                "avoidHighways": False,
                "avoidFerries": False
            },
            "languageCode": "en-US",
            "units": "IMPERIAL"
        }

        self.response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.response = self.response.json()
        return self.response