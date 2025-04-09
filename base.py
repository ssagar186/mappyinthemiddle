import geopy
from shapely.geometry import Polygon, LineString, Point
import folium


class CoordinateFinder:
    def __init__(self, *addresses):
        self.location = None
        self.addresses = addresses
        self.coordinates = None
        self.coordinates_list = []


    def get_coordinates(self, address):
        geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        self.location = geolocate.geocode(address)
        return self.location.latitude, self.location.longitude

    def update_coordinates_list(self):
        self.coordinates_list = []
        for address in self.addresses:
            self.coordinates = self.get_coordinates(address)
            print(f'self.coordinates:{self.coordinates}')
            if not self.coordinates:
                return f"Could not find coordinates for {address}"
            self.coordinates_list.append(self.coordinates)
        return self.coordinates_list

class CalculateCenter:
    def __init__(self, coordinates_list):
        self.coordinates = None
        self.coordinates_list = coordinates_list
        self.average_latitude = None
        self.average_longitude = None

    def get_average_lat_long(self):
        total_latitude = 0
        for coordinate in self.coordinates_list:
            total_latitude += coordinate[0]
        self.average_latitude = total_latitude / len(self.coordinates_list)
        total_longitude = 0
        for coordinate in self.coordinates_list:
            total_longitude += coordinate[1]
        self.average_longitude = total_longitude / len(self.coordinates_list)
        return self.average_latitude, self.average_longitude

    def calculate_centroid(self):
        polygon = Polygon(self.coordinates_list)
        centroid = polygon.centroid
        self.centroid = centroid
        return self.centroid.x, self.centroid.y

    def calculate_representative_point(self):
        polygon = Polygon(self.coordinates_list)
        representative_point = polygon.representative_point()
        self.representative_point = representative_point
        return self.representative_point.x, self.representative_point.y

class LocationFinder:
    def __init__(self, midpoint, POI):
        self.location = None
        self.coordinates = None
        self.midpoint = midpoint
        self.coordinates_list = []
        self.poi = POI
        self.centroid = None
        self.representative_point = None

    def find_places_nearby(self):
        geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        query = f"{self.poi} near {self.midpoint[0]}, {self.midpoint[1]}"
        # query = f"parks near {self.midpoint[0]}, {self.midpoint[1]}"
        places = geolocate.geocode(query, exactly_one=False, limit=10)
        print(f"places: {places}")
        if places:
            for place in places:
                return [(place.address, place.latitude, place.longitude)]
        else:
            return []

    def find_meeting_places(self):
        nearby_places = self.find_places_nearby()
        print(f"nearby_places:{nearby_places}")
        closest_place = (nearby_places[0][1], nearby_places[0][2])
        self.visualize_coordinates(closest_place)
        if nearby_places:
            return {
                "midpoint": self.midpoint,
                "places": nearby_places
            }
        else:
            return "No places found near midpoint"

    def visualize_coordinates(self, coordinates):
        map_center = coordinates[0], coordinates[1]
        my_map = folium.Map(location=map_center, zoom_start=12)
        coordinates = [coordinates]
        for lat, lon in coordinates:
            folium.Marker([lat, lon]).add_to(my_map)
        my_map.save("map.html")


def lookup_address(address):
    geolocator = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
    location = geolocator.geocode(address)
    print(f"Validated Address: {location.address}")
    return location.address


def validate_input():
    while True:
        option = input("Is this the correct address?").lower()
        if option in ['yes', 'y', '1']:
            return True
        elif option in ['no', 'n', '2']:
            return False
        else:
            print("Invalid input.")


if __name__ == '__main__':
    addresses = []
    while True:
        address = input("Please enter an address (or type 'done' to finish): ")
        if address.lower() == 'done':
            break
        try:
            address = lookup_address(address)
            if validate_input():
                addresses.append(address)
            else:
                address = input("Please reenter the address:")
                if address.lower() == 'done':
                    break
                address = lookup_address(address)
                if validate_input():
                    addresses.append(address)
        except AttributeError:
            print(f'Address not found')
    coordinate_finder = CoordinateFinder(*addresses)
    coordinates_list = coordinate_finder.update_coordinates_list()
    calculate_center = CalculateCenter(coordinates_list)
    POI = "Restaurants"
    midpoint = ""
    if len(addresses) < 3:
        latitude, longitude = calculate_center.get_average_lat_long()
        midpoint = latitude, longitude
    else:
        centroid = calculate_center.calculate_centroid()
        representative_point = calculate_center.calculate_representative_point()
        if centroid:
            midpoint = centroid
        elif representative_point:
            midpoint = representative_point
    location_finder = LocationFinder(midpoint, POI)
    result = location_finder.find_meeting_places()