import pandas as pd
import folium
from folium.plugins import HeatMap
pd.set_option('display.max_colwidth', 125)


class DataFormatting:
    def __init__(self, places_list):
        self.places_list = places_list
        self.df = None

    def create_data_table(self):
        df = pd.DataFrame(self.places_list, columns=['Places', 'Coordinates'])
        df.set_index('Places', inplace=True)
        self.df = df
        return self.df

    def print_data_table(self):
        print(self.df)

class MapMaker:
    @classmethod
    def print_data_table(cls, df):
        print(df)

    @classmethod
    def create_map_object(cls, closest_place_coordinates):
        map_center = closest_place_coordinates[0], closest_place_coordinates[1]
        output_map = folium.Map(location=map_center, zoom_start=12)
        return output_map

    @classmethod
    def construct_map(cls, places_map, closest_place_coordinates, origin_coordinates_list, places_list_coordinates, midpoint):
        poi_coordinates = [closest_place_coordinates]
        midpoint = [midpoint]
        cls.create_markers(poi_coordinates, 'red', places_map)
        places_map = cls.create_markers(poi_coordinates, 'green', places_map)
        places_map = cls.create_markers(origin_coordinates_list, 'red', places_map)
        places_map = cls.create_markers(midpoint, 'black', places_map)
        places_map = cls.create_heatmap(places_list_coordinates, places_map)
        return places_map

    @classmethod
    def create_markers(cls, coordinates_list, icon_color, output_map):
        for lat, lon in coordinates_list:
            folium.Marker([lat, lon], icon=folium.Icon(color=icon_color)).add_to(output_map)
        return output_map

    @classmethod
    def create_heatmap(cls, coordinates_list, output_map):
        HeatMap(coordinates_list).add_to(output_map)
        return output_map

    @classmethod
    def save_map(cls, output_map):
        output_map.save("map.html")
        return output_map
