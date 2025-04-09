import geopy
from shapely.geometry import Polygon, LineString, Point
import folium


class LocationFinder:
    def __init__(self, *addresses):
        self.average_longitude = None
        self.average_latitude = None
        self.location = None
        self.addresses = addresses
        self.coordinates = None
        self.midpoint = None
        self.coordinates_list = []
        self.poi = 'Restaurants'
        self.update_coordinates_list()

    def get_coordinates(self, address):
        geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        self.location = geolocate.geocode(address)
        return self.location.latitude, self.location.longitude

    def update_coordinates_list(self):
        self.coordinates_list = []
        for address in self.addresses:
            self.coordinates = self.get_coordinates(address)
            if not self.coordinates:
                return f"Could not find coordinates for {address}"
            self.coordinates_list.append(self.coordinates)
            print(f"Coordinates for {address}: {self.coordinates}")
            return self.coordinates_list

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

    def get_average_latitude(self):
        total_latitude = 0
        for coordinate in self.coordinates_list:
            total_latitude += coordinate[0]
        self.average_latitude = total_latitude / len(self.coordinates_list)
        return self.average_latitude

    def get_average_longitude(self):
        total_longitude = 0
        for coordinate in self.coordinates_list:
            total_longitude += coordinate[1]
        self.average_longitude = total_longitude / len(self.coordinates_list)
        return self.average_longitude

    def calculate_centroid(self, polygon_points):
        polygon = Polygon(polygon_points)
        centroid = polygon.centroid
        return centroid.x, centroid.y

    def calculate_representative_point(self, polygon_points):
        polygon = Polygon(polygon_points)
        representative_point = polygon.representative_point()
        return representative_point.x, representative_point.y

    def find_meeting_places_average(self):
        average_latitude = self.get_average_latitude()
        average_longitude = self.get_average_longitude()
        print(f"average latitude: {average_latitude}, average longitude: {average_longitude}")
        self.midpoint = (average_latitude, average_longitude)
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

    def find_meeting_places_central(self=None):
        polygon_points = self.coordinates_list
        centroid = self.calculate_centroid(polygon_points)
        representative_center = self.calculate_representative_point(polygon_points)
        print(f"representative_center:{representative_center}")
        print(f"The centroid of the polygon is: {centroid}")
        try:
            self.midpoint = centroid
        except IndexError:
            self.midpoint = representative_center
        nearby_places = self.find_places_nearby()
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
    location_finder = LocationFinder(*addresses)
    if len(addresses) < 3:
        result = location_finder.find_meeting_places_average()
    else:
        # result = find_meeting_places_average(*addresses)
        result = location_finder.find_meeting_places_central()
