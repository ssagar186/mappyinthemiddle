from src.address_check import AddressCheck
from src.calculate_center import CalculateCenter
from src.coordinate_finder import CoordinateFinder
from src.location_finder import LocationFinder
from src.visualization_tools import MapMaker
from src.visualization_tools import DataFormatting
from src.frontend_tools import FrontEndTools
import src.parameters as config


if __name__ == '__main__':
    midpoint = (33.8042708, -84.5370442)
    coordinates_list = [(33.7489924, -84.3902644), (33.8595492, -84.683824)]
    front_end_tools = FrontEndTools()
    front_end_tools.create_front_end()
    poi = "parking"
    location_finder = LocationFinder(midpoint, poi, coordinates_list)
    location_finder.find_closest_place()
    location_finder.extract_coordinates_from_places_list()
    data_formatting = DataFormatting(location_finder.places_list)
    data_formatting.create_data_table()
    data_formatting.print_data_table()
    places_map = MapMaker.create_map_object(location_finder.closest_place_coordinates)
    places_map = MapMaker.construct_map(places_map, location_finder.closest_place_coordinates,
                                        location_finder.coordinates_list,
                                        location_finder.places_list_coordinates)
    MapMaker.save_map(places_map)