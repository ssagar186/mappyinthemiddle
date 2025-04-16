import pandas as pd
import folium
from folium.plugins import HeatMap
pd.set_option('display.max_colwidth', 125)


class VisualizationTools:
    def visualize_table(cls, places_list):
        df = pd.DataFrame(places_list, columns=['Places', 'Coordinates'])
        df.set_index('Places', inplace=True)
        print(df)
    def visualize_coordinates(cls, closest_place_coordinates, coordinates_list, places_list_coordinates):
        map_center = closest_place_coordinates[0], closest_place_coordinates[1]
        my_map = folium.Map(location=map_center, zoom_start=12)
        coordinates = [closest_place_coordinates]
        for lat, lon in coordinates:
            folium.Marker([lat, lon], icon=folium.Icon(color='red')).add_to(my_map)
        for lat, lon in coordinates_list:
            folium.Marker([lat, lon], icon=folium.Icon(color='black')).add_to(my_map)
        HeatMap(places_list_coordinates).add_to(my_map)
        my_map.save("map.html")