import geopy


class LocationFinder:
    def __init__(self, midpoint, point_of_interest, coordinates_list):
        self.places_list_coordinates = None
        self.closest_place = None
        self.closest_place_coordinates = None
        self.places_list = None
        self.location = None
        self.coordinates = None
        self.midpoint = midpoint
        self.coordinates_list = coordinates_list
        self.poi = point_of_interest
        self.centroid = None
        self.representative_point = None

    def find_places_nearby_list(self):
        geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        query = f"{self.poi} near {self.midpoint[0]}, {self.midpoint[1]}"
        self.places_list = geolocate.geocode(query, exactly_one=False, limit=10)
        if self.places_list:
            for place in self.places_list:
                return [(place.address, place.latitude, place.longitude)]
        else:
            return []

    def extract_coordinates_from_places_list(self):
        places_list_coordinates = []
        for place in self.places_list:
            coordinates = place.latitude, place.longitude
            places_list_coordinates.append(coordinates)
        self.places_list_coordinates = places_list_coordinates
        return self.places_list_coordinates

    def find_closest_place(self):
        self.closest_place = self.find_places_nearby_list()
        self.closest_place_coordinates = (self.closest_place[0][1], self.closest_place[0][2])
        if self.closest_place:
            return {
                "midpoint": self.midpoint,
                "places": self.closest_place
            }
        else:
            return "No places found near midpoint"