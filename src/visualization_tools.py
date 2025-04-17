import pandas as pd
import folium
from folium.plugins import HeatMap
pd.set_option('display.max_colwidth', 125)


class VisualizationTools:


    def create_data_table(cls, places_list):
        df = pd.DataFrame(places_list, columns=['Places', 'Coordinates'])
        df.set_index('Places', inplace=True)
        return df

    def create_map_object(cls, closest_place_coordinates, origin_coordinates_list, places_list_coordinates):
        map_center = closest_place_coordinates[0], closest_place_coordinates[1]
        places_map = folium.Map(location=map_center, zoom_start=12)
        poi_coordinates = [closest_place_coordinates]
        places_map = cls.create_markers(poi_coordinates, 'red', places_map)
        places_map = cls.create_markers(origin_coordinates_list, 'black', places_map)
        places_map = cls.create_heatmap(places_list_coordinates, places_map)
        cls.save_map(places_map)

    def create_markers(cls, coordinates_list, icon_color, output_map):
        for lat, lon in coordinates_list:
            folium.Marker([lat, lon], icon=folium.Icon(color=icon_color)).add_to(output_map)
        return output_map

    def create_heatmap(cls, coordinates_list, output_map):
        HeatMap(coordinates_list).add_to(output_map)
        return output_map

    def save_map(cls, output_map):
        output_map.save("map.html")
        return output_map
