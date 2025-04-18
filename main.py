from src.address_check import AddressCheck
from src.calculate_center import CalculateCenter
from src.coordinate_finder import CoordinateFinder
from src.location_finder import LocationFinder
from src.visualization_tools import MapMaker
from src.visualization_tools import DataFormatting
import src.parameters as config


if __name__ == '__main__':
    address_check = AddressCheck()
    address_check.user_input()
    coordinate_finder = CoordinateFinder(*address_check.addresses)
    coordinate_finder.update_coordinates_list()
    calculate_center = CalculateCenter(coordinate_finder.coordinates_list)
    calculate_center.get_midpoint()
    location_finder = LocationFinder(calculate_center.midpoint, config.poi, coordinate_finder.coordinates_list)
    location_finder.find_closest_place()
    location_finder.extract_coordinates_from_places_list()
    data_formatting = DataFormatting(location_finder.places_list)
    data_formatting.print_data_table()
    places_map = MapMaker.create_map_object(location_finder.closest_place_coordinates)
    places_map = MapMaker.construct_map(places_map, location_finder.closest_place_coordinates,
                                        location_finder.coordinates_list,
                                        location_finder.places_list_coordinates)
    MapMaker.save_map(places_map)

