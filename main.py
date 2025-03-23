import geopy
from shapely.geometry import Polygon
import folium

def calculate_centroid(polygon_points):
    polygon = Polygon(polygon_points)
    centroid = polygon.centroid
    return centroid.x, centroid.y


def get_coordinates(address):
    geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
    location = geolocate.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None


def find_places_nearby(midpoint, radius=5000):
    geolocate = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
    query = f"restaurants near {midpoint[0]}, {midpoint[1]}"
    places = geolocate.geocode(query, exactly_one=False, limit=5)
    print(f"places: {places}")
    if places:
        for place in places:
            return [(place.address, place.latitude, place.longitude)]
    else:
        return []


def get_average_latitude(coordinates_list):
    total_latitude = 0
    for coordinate in coordinates_list:
        total_latitude += coordinate[0]  # The latitude is the first value in each coordinate pair
    average_latitude = total_latitude / len(coordinates_list)
    return average_latitude


def get_average_longitude(coordinates_list):
    total_longitude = 0
    for coordinate in coordinates_list:
        total_longitude += coordinate[1]
    average_longitude = total_longitude / len(coordinates_list)
    return average_longitude


def find_meeting_places_average(*addresses):
    coordinates_list = []
    for address in addresses:
        coordinates = get_coordinates(address)
        if not coordinates:
            return f"Could not find coordinates for {address}"
        coordinates_list.append(coordinates)
        # print(f"Coordinates for {address}: {coordinates}")
    average_latitude = get_average_latitude(coordinates_list)
    average_longitude = get_average_longitude(coordinates_list)
    print(f"average latitude: {average_latitude}, average longitude: {average_longitude}")
    midpoint = (average_latitude, average_longitude)
    nearby_places = find_places_nearby(midpoint)
    closest_place = (nearby_places[0][1],nearby_places[0][2])
    visualize_coordinates(closest_place)
    if nearby_places:
        return {
            "midpoint": midpoint,
            "places": nearby_places
        }
    else:
        return "No places found near midpoint"


def find_meeting_places_central(*addresses):
    coordinates_list = []
    for address in addresses:
        coordinates = get_coordinates(address)
        if not coordinates:
            return f"Could not find coordinates for {address}"
        coordinates_list.append(coordinates)
        print(f"Coordinates for {address}: {coordinates}")
    polygon_points = coordinates_list
    centroid = calculate_centroid(polygon_points)
    print(f"The centroid of the polygon is: {centroid}")
    midpoint = centroid

    nearby_places = find_places_nearby(midpoint)
    closest_place = (nearby_places[0][1], nearby_places[0][2])
    visualize_coordinates(closest_place)
    if nearby_places:
        return {
            "midpoint": midpoint,
            "places": nearby_places
        }
    else:
        return "No places found near midpoint"


def lookup_address(address):
    geolocator = geopy.Nominatim(user_agent="mappy_in_the_middle", timeout=10)
    location = geolocator.geocode(address)
    print(f"Validated Address: {location.address}")
    return location.address


def convert_address_to_cartesian(address):
    pass

def visualize_coordinates(coordinates):

    map_center = coordinates[0], coordinates[1]
    my_map = folium.Map(location=map_center, zoom_start=12)
    coordinates = [coordinates]
    for lat, lon in coordinates:
        folium.Marker([lat, lon]).add_to(my_map)
    my_map.save("map.html")


if __name__ == '__main__':
    addresses = []
    while True:
        address = input("Please enter an address (or type 'done' to finish): ")
        if address.lower() == 'done':
            break
        try:
            address = lookup_address(address)
            addresses.append(address)
        except AttributeError:
            print(f'Address not found')
    if len(addresses) < 4:
        result = find_meeting_places_average(*addresses)
    else:
        result = find_meeting_places_central(*addresses)
