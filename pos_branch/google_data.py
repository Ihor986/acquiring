from typing import Union
from i_data_class import IApiData
import requests


class GoogleMapsApiData(IApiData):
    
    WALK_MODE = 'walking'
    DRIVE_MODE = 'driving'
    
    def __init__(self, requests_limit: Union[int, float] = float('inf')) -> None:
        print('__init__ GoogleMapsApiData ... ')
        self._api_key: str = '...'
        self._mode: str = self.WALK_MODE
        
        self._count_requests: int = 0
        self._count_requests_limit: Union[int, float] = requests_limit
        
    @property
    def count_requests(self):
        return self._count_requests
        
        
    def get_coordinates(self, address: str) -> tuple:
        
        if self._count_requests >= self._count_requests_limit:
            raise Exception("Requests limit")

        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "key": self._api_key
        }
        
        response = requests.get(base_url, params=params)
        self._count_requests += 1
        data = response.json()
        
        try:
            lat = data.get("results")[0].get("geometry").get("location").get("lat")
            lng = data.get("results")[0].get("geometry").get("location").get("lng")
            adrs = data.get("results")[0].get("formatted_address")
        except:
            lat, lng, adrs = None, None, None
            
        return (lat, lng, adrs)
    
    
    def get_distances_matrix_path(self, terminal_coords, branch_coords_list):
        closest_branch_id, closest_distance, closest_coords = None, float('inf'), None
        distances_matrix = self._get_distance_matrix(terminal_coords, [coord for _, coord in branch_coords_list])
        if distances_matrix is None:
            return closest_branch_id, closest_distance, closest_coords
        
        distances: dict = {}
        branch_coords_map = {}

        for i, dist_data in enumerate(distances_matrix):
            try:
                distance_value = dist_data.get("distance").get("value")
                branch_id, branch_coords = branch_coords_list[i]
                distances[branch_id] = distance_value
                branch_coords_map[branch_id] = branch_coords
            except:
                print('ex1')
                # return closest_branch_id, closest_distance, closest_coords

        if distances:
            closest_branch_id = min(distances, key=lambda x: distances[x])
            closest_distance = distances[closest_branch_id]
            closest_coords = branch_coords_map[closest_branch_id]

        return closest_branch_id, closest_distance, closest_coords

    def _get_distance_matrix(self, terminal_coords, branch_coords_list):
        
        origins = f"{terminal_coords[0]},{terminal_coords[1]}"
        destinations = "|".join([f"{coords[0]},{coords[1]}" for coords in branch_coords_list])

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origins,
            "destinations": destinations,
            "key": self._api_key,
            "mode": self._mode
        }

        response = requests.get(url, params=params)
        matrix_data = response.json()

        try:
            return matrix_data.get("rows")[0].get("elements")
        except:
            print('ex2')
            return None
    