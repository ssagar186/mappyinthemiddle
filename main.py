from src.address_input_lookup import AddressInputLookup
from src.calculate_center import CalculateCenter
from src.coordinate_finder import CoordinateFinder
from src.location_finder import LocationFinder
from src.visualization_tools import MapMaker
from src.visualization_tools import DataFormatting
import src.parameters as config
from src.routes import Routes


if __name__ == '__main__':
    address_check = AddressInputLookup()
    address_check.user_input()
    coordinate_finder = CoordinateFinder(*address_check.addresses)
    coordinate_finder.update_coordinates_list()
    calculate_center = CalculateCenter(coordinate_finder.origin_coordinates_list)
    calculate_center.get_midpoint()
    location_finder = LocationFinder(calculate_center.midpoint, config.poi, coordinate_finder.origin_coordinates_list)
    location_finder.find_closest_place()
    location_finder.extract_coordinates_from_places_list()
    routes = Routes()
    for address in enumerate(location_finder.origin_coordinates_list):
        time_unit = routes.calculate_route_between_points(address[1], location_finder.midpoint)
        print(f'Distance from {address_check.addresses[(address[0])]} to the midpoint is {routes.travel_distance}mi. It will take {routes.travel_time} {time_unit} to get there.')
    data_formatting = DataFormatting(location_finder.places_list)
    data_formatting.create_data_table()
    data_formatting.print_data_table()
    places_map = MapMaker.create_map_object(location_finder.closest_place_coordinates)
    places_map = MapMaker.construct_map(places_map, location_finder.closest_place_coordinates,
                                        location_finder.origin_coordinates_list,
                                        location_finder.places_list_coordinates, location_finder.midpoint)
    MapMaker.save_map(places_map)

