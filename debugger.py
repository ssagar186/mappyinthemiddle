from src.address_check import AddressCheck
from src.calculate_center import CalculateCenter
from src.coordinate_finder import CoordinateFinder
from src.location_finder import LocationFinder
from src.visualization_tools import VisualizationTools
import src.parameters as config


if __name__ == '__main__':
    midpoint = (33.8042708, -84.5370442)
    coordinates_list = [(33.7489924, -84.3902644), (33.8595492, -84.683824)]
    poi = "parking"
    location_finder = LocationFinder(midpoint, poi, coordinates_list)
    location_finder.find_closest_place()
    location_finder.extract_coordinates_from_places_list()
    visualization_tools = VisualizationTools()
    df = visualization_tools.create_data_table(location_finder.places_list)
    print(df)
    visualization_tools.create_map_object(location_finder.closest_place_coordinates, location_finder.coordinates_list, location_finder.places_list_coordinates)

4