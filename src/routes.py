from src.keys import api_key
import requests
import json


class Routes:
    def __init__(self):
        self.response = None
        self.travel_distance = None
        self.travel_time = None

    def calculate_distance_between_points(self):
        travel_distance = round(self.response['routes'][0]['distanceMeters'] / 1609)
        return travel_distance

    def calculate_traffic_between_points(self):
        travel_time = self.response['routes'][0]['duration']
        if travel_time[-1].isalpha():
            travel_time = travel_time[:-1]
        travel_time = round(int(travel_time) / 60)
        return travel_time

    def calculate_route_between_points(self, origin_coordinates, destination_coordinates):
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
                        "latitude": destination_coordinates[0],
                        "longitude": destination_coordinates[1]
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
        self.travel_distance = self.calculate_distance_between_points()
        if self.calculate_traffic_between_points() >= 60:
            self.travel_time = round(self.calculate_traffic_between_points()/60, 2)
            return "hours"
        else:
            self.travel_time = round(self.calculate_traffic_between_points(), 2)
            return "minutes"