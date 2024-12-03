import math
import requests
from typing import Optional
from geopy.geocoders import Nominatim
from geopy.location import Location
import osmnx as ox
import networkx as nx
from models.i_data_class import IApiData
import matplotlib.pyplot as plt
import json
import pandas as pd

class FreeSourceData(IApiData):
    
    WALK_MODE = 'walk'
    DRIVE_MODE = 'drive'
    
    def __init__(self, nearest_nodes_cache: Optional[pd.DataFrame] = None) -> None: # , place, mode # self._city_graph = ox.graph_from_place(place, network_type=mode)
        print('__init__ FreeSourceData ... ')
        self._geolocator = Nominatim(user_agent="location-matcher")
        self._city_graph: nx.Graph|None = self._create_graph()
        self._nearest_nodes_cache = self._init_nodes_cache(nearest_nodes_cache)
        
    def _init_nodes_cache(self, nearest_nodes_cache: Optional[pd.DataFrame] = None):
        if nearest_nodes_cache is None:
            cache_columns = ["lat", "lng", "nearest_node"]
            nearest_nodes_cache = pd.DataFrame(columns=cache_columns)
        return nearest_nodes_cache
        
    def _create_graph(self):
        # graphs = [
            
        #     # ox.load_graphml(filepath="Kyiv_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Ternopil_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Cherkasy_Oblast_graph.graphml"),
            
        #     # ox.load_graphml(filepath="Kirovohrad_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Zakarpattia_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Volyn_Oblast_graph.graphml"),
            
        #     # ox.load_graphml(filepath="Vinnytsia_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Sumy_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Chernihiv_Oblast_graph.graphml"),
            
        #     # ox.load_graphml(filepath="Kherson_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Kharkiv_Oblast_graph.graphml"),
            
        #     # ox.load_graphml(filepath="Poltava_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Lviv_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Chernivtsi_Oblast_graph.graphml"), 
            
        #     # ox.load_graphml(filepath="Хмельницька_область_graph.graphml"), 
        #     # ox.load_graphml(filepath="Запорізька_область_graph.graphml"), 
        #     # ox.load_graphml(filepath="Rivne_Oblast_graph.graphml"), 
            
        #     # ox.load_graphml(filepath="Zhytomyr_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Mykolaiv_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Ivano-Frankivsk_Oblast_graph.graphml"), 
        #     # ox.load_graphml(filepath="Dnipropetrovsk_Oblast_graph.graphml")
        #     ox.load_graphml(filepath="city_graph.graphml")
        #     ] 
                
        # combined_graph = nx.compose_all(graphs)
        # return ox.load_graphml(filepath="D:\\резюме\\райф\\acquiring_data\\graphml\\Dnipropetrovsk_Oblast_graph.graphml") # None #combined_graph
        return None
        
        
     # Функція для отримання координат
    def get_coordinates(self, address: str):
        lat, lng, adrs = None, None, None
        location = self._geolocator.geocode(address)
        if isinstance(location, Location):
            lat = location.latitude
            lng = location.longitude
            adrs = location.address
        return lat, lng, adrs

        
    def get_distances_matrix_path(self, term_coord, branch_coords):
        closest_branch_id, closest_distance, closest_coords = None, float('inf'), None
        # try:
        #     term_node = ox.nearest_nodes(self._city_graph, term_coord[1], term_coord[0])
        #     print(term_node)
            
        #     branch_ids = [branch_id for branch_id, _ in branch_coords]
        #     branch_coords_list = [(coord[1], coord[0]) for _, coord in branch_coords]  # Змінюємо порядок для функції
        #     nearest_nodes = self._get_nearest_nodes(self._city_graph, branch_coords_list)# ox.nearest_nodes(self._city_graph, X=[coord[0] for coord in branch_coords_list], Y=[coord[1] for coord in branch_coords_list])
        #     branch_nodes = [(nearest_nodes[i], branch_ids[i], branch_coords[i][1]) for i in range(len(branch_ids))]
        #     distances = {}
        #     branch_coords_map = {}
            
        #     all_distances = nx.single_source_dijkstra_path_length(self._city_graph, term_node, weight="length")
        #     for branch_node, branch_id, coord in branch_nodes:
        #         distance_value = all_distances.get(branch_node, float('inf'))
        #         distances[branch_id] = distance_value
        #         branch_coords_map[branch_id] = coord

        #     if distances:
        #         closest_branch_id = min(distances, key=lambda x: distances[x])
        #         closest_distance = distances[closest_branch_id]
        #         closest_coords = branch_coords_map[closest_branch_id]
                
        #     return closest_branch_id, closest_distance, closest_coords
        
        # except Exception as e:
        #     print(f"Помилка: {e}")
        #     return closest_branch_id, closest_distance, closest_coords
        
        
    def _get_nearest_nodes(self, city_graph, branch_coords_list):
        results = []  # Результати для кожної координати
        uncached_coords = []  # Координати, яких немає в кеші

        # Перевірка кожної координати
        for coord in branch_coords_list:
            # Фільтруємо кеш, щоб знайти відповідну координату
            match = self._nearest_nodes_cache[
                (self._nearest_nodes_cache["lat"] == coord[0]) &
                (self._nearest_nodes_cache["lng"] == coord[1])
            ]
            
            if not match.empty:
                # Якщо знайдено, додаємо вузол із кешу
                results.append(match["nearest_node"].iloc[0])
            else:
                # Якщо немає в кеші, додаємо до списку для обробки
                uncached_coords.append(coord)

        # Якщо є координати, яких немає в кеші
        if uncached_coords:
            # Розділяємо широти та довготи
            X = [coord[0] for coord in uncached_coords]
            Y = [coord[1] for coord in uncached_coords]

            # Викликаємо `ox.nearest_nodes` для всіх нових координат
            new_nodes = ox.nearest_nodes(city_graph, X=X, Y=Y)

            # Створюємо DataFrame для нових записів
            new_cache_entries = pd.DataFrame({
                "lat": X,
                "lng": Y,
                "nearest_node": new_nodes
            })

            # Додаємо нові записи до кешу
            self._nearest_nodes_cache = pd.concat([self._nearest_nodes_cache, new_cache_entries], ignore_index=True)

            # Додаємо нові вузли до результатів
            results.extend(new_nodes)

        return results