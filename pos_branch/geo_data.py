import math
from i_data_class import IApiData

class GeoData:
    
    def __init__(self, api_data_class) -> None:
        print('__init__ GeoData ... ')
        self.api_data_class: IApiData = api_data_class
    
    def get_coordinates(self, address: str):
        return self.api_data_class.get_coordinates(address)
    
    def get_distances_matrix_path(self, terminal_coords, branch_coords_list):
        return self.api_data_class.get_distances_matrix_path(terminal_coords, branch_coords_list)   
        
    def haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Метод для визначення відстані між точками на кулі R = 6371.0
        Args:
            lat1 (float): latitude першої точки
            lon1 (float): longitude першої точки
            lat2 (float): latitude другої точки
            lon2 (float): longitude другої точки

        Returns:
            float: Відстань в км
        """
        # Радіус Землі в кілометрах
        R = 6371.0

        # Перевести градуси в радіани
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Різниця між широтами та довготами
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Формула Хаверсина
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # Відстань в км
        distance = R * c
        return distance



