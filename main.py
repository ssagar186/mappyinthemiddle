from src.address_check import AddressCheck
from src.calculate_center import CalculateCenter
from src.coordinate_finder import CoordinateFinder
from src.location_finder import LocationFinder
from src.visualization_tools import VisualizationTools


if __name__ == '__main__':
    address_check = AddressCheck()
    address_check.user_input()
    coordinate_finder = CoordinateFinder(*address_check.addresses)
    coordinate_finder.update_coordinates_list()
    calculate_center = CalculateCenter(coordinate_finder.coordinates_list)
    POI = "Restaurants"
    calculate_center.get_midpoint()
    location_finder = LocationFinder(calculate_center.midpoint, POI, coordinate_finder.coordinates_list)
    location_finder.find_meeting_places()
    location_finder.extract_coordinates_from_places_list()
    visualization_tools = VisualizationTools()
    visualization_tools.visualize_table(location_finder.places_list)
    visualization_tools.visualize_coordinates(location_finder.closest_place_coordinates, location_finder.coordinates_list, location_finder.places_list_coordinates)
