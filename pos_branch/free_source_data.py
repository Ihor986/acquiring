import math
import requests
from typing import Optional
from geopy.geocoders import Nominatim
from geopy.location import Location
import osmnx as ox
import networkx as nx
from i_data_class import IApiData
import matplotlib.pyplot as plt
import json

class FreeSourceData(IApiData):
    
    WALK_MODE = 'walk'
    DRIVE_MODE = 'drive'
    
    def __init__(self) -> None: # , place, mode # self._city_graph = ox.graph_from_place(place, network_type=mode)
        print('__init__ FreeSourceData ... ')
        self._geolocator = Nominatim(user_agent="location-matcher")
        self._city_graph: nx.Graph = self._create_graph()
        
    def _create_graph(self):
        graphs = [
            # ox.load_graphml(filepath="Zhytomyr_Oblast_graph.graphml"), city_graph
            ox.load_graphml(filepath="Dnipropetrovsk_Oblast_graph.graphml")
            ]
        combined_graph = nx.compose_all(graphs)
        return combined_graph

        
        
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
        try:
            term_node = ox.nearest_nodes(self._city_graph, term_coord[1], term_coord[0])
            
            branch_ids = [branch_id for branch_id, _ in branch_coords]
            branch_coords_list = [(coord[1], coord[0]) for _, coord in branch_coords]  # Змінюємо порядок для функції
            nearest_nodes = ox.nearest_nodes(self._city_graph, X=[coord[0] for coord in branch_coords_list], Y=[coord[1] for coord in branch_coords_list])
            branch_nodes = [(nearest_nodes[i], branch_ids[i], branch_coords[i][1]) for i in range(len(branch_ids))]
            
            distances = {}
            branch_coords_map = {}
            
            all_distances = nx.single_source_dijkstra_path_length(self._city_graph, term_node, weight="length")
            for branch_node, branch_id, coord in branch_nodes:
                distance_value = all_distances.get(branch_node, float('inf'))
                distances[branch_id] = distance_value
                branch_coords_map[branch_id] = coord

            if distances:
                closest_branch_id = min(distances, key=lambda x: distances[x])
                closest_distance = distances[closest_branch_id]
                closest_coords = branch_coords_map[closest_branch_id]
                
            return closest_branch_id, closest_distance, closest_coords
        
        except Exception as e:
            print(f"Помилка: {e}")
            return closest_branch_id, closest_distance, closest_coords