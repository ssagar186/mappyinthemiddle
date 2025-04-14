import geopy
from shapely.geometry import Polygon, LineString, Point
import folium
import pandas as pd
pd.set_option('display.max_colwidth', 125)

class AddressCheck:
    def __init__(self):
        self.location = None
        self.addresses = []
        self.address = None

    def lookup_address(self):
        geolocator = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        self.location = geolocator.geocode(self.address)
        print(f"Validated Address: {self.location.address}")
        return self.location.address

    def validate_input(self):
        while True:
            option = input("Is this the correct address?").lower()
            if option in ['yes', 'y', '1']:
                return True
            elif option in ['no', 'n', '2']:
                return False
            else:
                print("Invalid input.")

    def address_input(self):
        while True:
            self.address = input("Please enter an address (or type 'done' to finish): ")
            if self.address.lower() == 'done':
                break
            try:
                self.address = self.lookup_address()
                if self.validate_input():
                    self.addresses.append(self.address)
                else:
                    self.address = input("Please reenter the address:")
                    if self.address.lower() == 'done':
                        break
                    self.address = self.lookup_address()
                    if self.validate_input():
                        self.addresses.append(self.address)
            except AttributeError:
                print(f'Address not found')


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
            #print(f'self.coordinates:{self.coordinates}')
            if not self.coordinates:
                return f"Could not find coordinates for {address}"
            self.coordinates_list.append(self.coordinates)
        return self.coordinates_list


class CalculateCenter:
    def __init__(self, coordinates_list):
        self.centroid = None
        self.representative_point = None
        self.coordinates = None
        self.coordinates_list = coordinates_list
        self.average_latitude = None
        self.average_longitude = None
        self.midpoint = None
        self.places_list = []

    def get_midpoint(self):
        if len(self.coordinates_list) < 3:
            self.midpoint = self.get_average_lat_long()
        elif len(self.coordinates_list) > 2:
            self.midpoint = self.calculate_centroid()
            if self.centroid:
                pass
            else:
                self.midpoint = self.calculate_representative_point()
        return self.midpoint

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
    def __init__(self, midpoint, point_of_interest):
        self.location = None
        self.coordinates = None
        self.midpoint = midpoint
        self.coordinates_list = []
        self.poi = point_of_interest
        self.centroid = None
        self.representative_point = None

    def find_places_nearby(self):
        geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        query = f"{self.poi} near {self.midpoint[0]}, {self.midpoint[1]}"
        self.places_list = geolocate.geocode(query, exactly_one=False, limit=10)
        #print(f"List of Places: {self.places_list}")
        if self.places_list:
            for place in self.places_list:
                return [(place.address, place.latitude, place.longitude)]
        else:
            return []

    def find_meeting_places(self):
        closest_place = self.find_places_nearby()
        print(f"closest_place:{closest_place}")
        closest_place_coordinates = (closest_place[0][1], closest_place[0][2])
        #print(f"closest_place_coordinates:{closest_place_coordinates}")
        self.visualize_coordinates(closest_place_coordinates)
        self.visualize_table()
        if closest_place:
            return {
                "midpoint": self.midpoint,
                "places": closest_place
            }
        else:
            return "No places found near midpoint"

    def visualize_table(self):
        df = pd.DataFrame(self.places_list, columns=['Place', 'Coordinates'])
        df.set_index('Place', inplace=True)
        print(df)

    def visualize_coordinates(self, coordinates):
        map_center = coordinates[0], coordinates[1]
        my_map = folium.Map(location=map_center, zoom_start=12)
        coordinates = [coordinates]
        for lat, lon in coordinates:
            folium.Marker([lat, lon]).add_to(my_map)
        my_map.save("map.html")


if __name__ == '__main__':
    address_check = AddressCheck()
    address_check.address_input()
    addresses_list = address_check.addresses
    coordinate_finder = CoordinateFinder(*address_check.addresses)
    coordinate_finder.update_coordinates_list()
    calculate_center = CalculateCenter(coordinate_finder.coordinates_list)
    POI = "Restaurants"
    calculate_center.get_midpoint()
    location_finder = LocationFinder(calculate_center.midpoint, POI)
    location_finder.find_meeting_places()
