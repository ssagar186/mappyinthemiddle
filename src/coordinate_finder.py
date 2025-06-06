import geopy


class CoordinateFinder:
    def __init__(self, *addresses):
        self.location = None
        self.addresses = addresses
        self.coordinates = None
        self.origin_coordinates_list = []

    def get_coordinates_from_address(self, address):
        geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
        self.location = geolocate.geocode(address)
        return self.location.latitude, self.location.longitude

    def update_coordinates_list(self):
        self.origin_coordinates_list = []
        for address in self.addresses:
            self.coordinates = self.get_coordinates_from_address(address)
            #print(f'self.coordinates:{self.coordinates}')
            if not self.coordinates:
                return f"Could not find coordinates for {address}"
            self.origin_coordinates_list.append(self.coordinates)
        return self.origin_coordinates_list