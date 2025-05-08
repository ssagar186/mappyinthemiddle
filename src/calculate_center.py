from shapely.geometry import Polygon, LineString, Point


class CalculateCenter:
    def __init__(self, coordinates_list):
        self.centroid = None
        self.representative_point = None
        self.coordinates = None
        self.coordinates_list = coordinates_list
        self.average_latitude = None
        self.average_longitude = None
        self.midpoint = None
        self.places_list = []

    def get_midpoint(self):
        if len(self.coordinates_list) < 3:
            self.midpoint = self.get_average_lat_long()
        elif len(self.coordinates_list) > 2:
            self.midpoint = self.calculate_centroid()
            if self.centroid:
                pass
            else:
                self.midpoint = self.calculate_representative_point()
        return self.midpoint

    def get_average_lat_long(self):
        total_latitude = 0
        for coordinate in self.coordinates_list:
            total_latitude += coordinate[0]
        self.average_latitude = total_latitude / len(self.coordinates_list)
        total_longitude = 0
        for coordinate in self.coordinates_list:
            total_longitude += coordinate[1]
        self.average_longitude = total_longitude / len(self.coordinates_list)
        return self.average_latitude, self.average_longitude

    def calculate_centroid(self):
        polygon = Polygon(self.coordinates_list)
        centroid = polygon.centroid
        self.centroid = centroid
        return self.centroid.x, self.centroid.y

    def calculate_representative_point(self):
        polygon = Polygon(self.coordinates_list)
        representative_point = polygon.representative_point()
        self.representative_point = representative_point
        return self.representative_point.x, self.representative_point.y