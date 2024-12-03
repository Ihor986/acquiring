from typing import Optional
from geo_data import GeoData
import pandas as pd
import folium
import ast
import time
import json

class WorkClass:
    
    def __init__(
        self, 
        branches, 
        terminals, 
        geo_data, 
        addres_df: Optional[pd.DataFrame] = None, 
        nearest_df: Optional[pd.DataFrame] = None
        ) -> None:
        print('__init__ WorkClass ... ')
        self.start_time = time.time()
        self._nearest_path_num: int = 0
        self._coordinates_num: int = 0
        
        self._map: folium.Map = folium.Map()
        self._geo_data: GeoData = geo_data
        self._branches: pd.DataFrame = branches
        self._terminals: pd.DataFrame = terminals
        self._address_df: pd.DataFrame = self._init_address_df(addres_df)
        self._nearest_df: pd.DataFrame = self._init_neares_df(nearest_df)
        
        
    def _init_neares_df(self, nearest_df: pd.DataFrame | None = None) -> pd.DataFrame:
        
        if nearest_df is None:
            nearest_df = pd.DataFrame(columns=['lat', 'lng', 'close_coordinates', 'closest_path_branch', 'distance_path', 'closest_path_coordinates'])
        return nearest_df
        
    
    def _init_address_df(self, address_df: pd.DataFrame | None = None) -> pd.DataFrame:
        
        if address_df is None:
            address_df = pd.DataFrame(columns=['address', 'lat', 'lng', 'adrs'])
        return address_df       
    
    @property
    def geo_data(self):
        return self._geo_data
    
    @property
    def branches(self):
        return self._branches
    
    @property
    def nearest_df(self):
        return self._nearest_df
    
    @property
    def address_df(self):
        return self._address_df
    
    @property
    def terminals(self):
        return self._terminals
    
    @property
    def map(self):
        return self._map
    
    def add_terminals_coordinates(self) -> None:
        self._terminals[['lat', 'lng', 'adrs']] = (
            self._terminals.apply(lambda x: pd.Series(self._add_coordinates(x)), axis=1)
            )
        
    def add_branches_coordinates(self) -> None:
        self._branches[['lat', 'lng', 'adrs']] = (
            self._branches.apply(lambda x: pd.Series(self._add_coordinates(x)), axis=1)
            )
        
    def _add_coordinates(self, row: pd.Series): 
        
        address = str(row['address']).lower()
        cache_condition = self._address_df['address'] == address
        
        if cache_condition.any():
            cache_row = self._address_df[cache_condition].iloc[0]
            lat = cache_row['lat']
            lng = cache_row['lng']
            adrs = cache_row['adrs']
            
            self._coordinates_num += 1
            print(adrs,'\n', self._coordinates_num)
            return lat, lng, adrs
        
        lat, lng, adrs = self.geo_data.get_coordinates(address)
        new_cache_row = {
            'address': address,
            'lat': lat,
            'lng': lng,
            'adrs': adrs
        }
        self._address_df = pd.concat([self._address_df, pd.DataFrame([new_cache_row])], ignore_index=True)
        self._coordinates_num += 1
        print(adrs,'\n', self._coordinates_num)
        return lat, lng, adrs
        
        
    def add_nearest_branch(self, target_distance: int, target_branch_count: int):
        self._terminals[['nearest_id', 'distance', 'nearest_coord', 'close_points', 'close_coordinates']] = (
            self._terminals.apply(lambda row: pd.Series(self._find_nearest(row, target_distance, target_branch_count), dtype='str'), axis=1)
            )
        
    def _find_nearest(self, point: pd.Series, target_distance: int, target_branch_count: int):
        try:
            candidates = self._branches
            distances = candidates.apply(lambda row: self.geo_data.haversine(point['lat'], point['lng'], row['lat'], row['lng']), axis=1)
            min_idx = distances.idxmin()
            nearest_id = candidates.loc[min_idx, 'num']
            nearest_distance = distances[min_idx]

            close_points = {candidates.at[i, 'num']: dist for i, dist in distances.items() if dist < target_distance}
            
            close_points = dict(sorted(close_points.items(), key=lambda x: x[1])[:target_branch_count])

            close_coordinates = {
                num: [candidates[candidates['num'] == num].iloc[0]['lat'], candidates[candidates['num'] == num].iloc[0]['lng']]
                for num in close_points.keys()
            }
            
            return nearest_id, nearest_distance, close_points , close_coordinates, close_coordinates[nearest_id]
        
        except Exception as e:
            print('_find_nearest: \n', e)
            return None, None, {}, {}
    
            
    def add_nearest_path_branch(self):
        self._nearest_df
        self._terminals[['closest_path_branch', 'distance_path', 'closest_path_coordinates']] = (
            self._terminals.apply(lambda row: pd.Series(self._add_nearest_path_branch(row)), axis=1)
            )
    
            
    def _add_nearest_path_branch(self, row): 
        
        self._nearest_path_num += 1
        
        cache_condition = (
            (self._nearest_df['lat'].astype(str) == str(row['lat'])) & (self._nearest_df['lng'].astype(str) == str(row['lng'])) & 
            (self._nearest_df['close_coordinates'].astype(str) == str(row['close_coordinates']))
            )
        
        if cache_condition.any():
            cache_row = self._nearest_df[cache_condition].iloc[0]
            closest_branch = cache_row['closest_path_branch']
            distance = cache_row['distance_path']
            closest_path_coordinates = cache_row['closest_path_coordinates']
            print(f"it's cash {self._nearest_path_num}", f"розрахованоза за {round((time.time() - self.start_time),0)} секунд")
            self.start_time = time.time()
            return (closest_branch, distance, closest_path_coordinates)

        try:
            close_coordinates = json.loads(f"{row['close_coordinates']}".replace("'", '"'))
        except:
            close_coordinates = {}
            
        trminal_coords = (row['lat'], row['lng'])
        
        branch_coords_list = list([key, value] for key, value in close_coordinates.items())
        closest_branch, distance, closest_path_coordinates = self.geo_data.get_distances_matrix_path(trminal_coords, branch_coords_list)
        values = (closest_branch, distance, closest_path_coordinates)
        new_cache_row = {
            'lat': row['lat'],
            'lng': row['lng'],
            'close_coordinates': row['close_coordinates'],
            'closest_path_branch': closest_branch,
            'distance_path': distance,
            'closest_path_coordinates': closest_path_coordinates
        }
        self._nearest_df = pd.concat([self._nearest_df, pd.DataFrame([new_cache_row])], ignore_index=True)
        print(f"it's not cash {self._nearest_path_num}", f"розрахованоза за {time.time() - self.start_time} секунд")
        self.start_time = time.time()
        return values
    
    def finalize_columns(self):
        self._terminals = pd.merge(self.terminals, self.branches, left_on="nearest_id", right_on="num",  how="left", suffixes=("", "_branch"))
        self._terminals['tech_num'] = '1'
        print(self.terminals.columns)
    
    
    def visualize_branches_and_terminals(self, closest_coordinates:str = 'closest_path_coordinates'):

        # Центр карти — середні координати всіх точок
        avg_lat = (self.branches["lat"].mean() + self.terminals["lat"].mean()) / 2
        avg_lng = (self.branches["lng"].mean() + self.terminals["lng"].mean()) / 2
        m = folium.Map(location=[avg_lat, avg_lng], zoom_start=12)

        # Додаємо термінали на мапу
        for _, terminal in self.terminals.iterrows():
            
            try:
                closest_branch_coords = json.loads(f"{terminal[closest_coordinates]}")
            except:
                closest_branch_coords = terminal[closest_coordinates]
                print(terminal[closest_coordinates])
                
            try:
                if isinstance(closest_branch_coords, list) and len(closest_branch_coords) == 2: 
                    folium.PolyLine(
                        locations=[
                            [terminal["lat"], terminal["lng"]],  # Координати термінала
                            [closest_branch_coords[0], closest_branch_coords[1]],  # Координати найближчого бранча
                        ],
                        color="green",
                        weight=2,
                    ).add_to(m)
                
                folium.CircleMarker(
                    location=[terminal["lat"], terminal["lng"]],
                    popup=f"Terminal: {terminal['num']}",
                    radius=3.0,
                    color="red",
                    fill=True,
                    fill_opacity=0.6,
                ).add_to(m)
            except Exception as e:
                print(e)
                
        # Додаємо бранчі на мапу
        for _, branch in self.branches.iterrows():
            try:
                folium.CircleMarker(
                    location=[branch["lat"], branch["lng"]],
                    popup=f"{branch['name']},\n {branch['num']}",
                    radius=6.0,
                    fill_color="yellow",
                    color="black",
                    fill=True,
                    fill_opacity=1,
                ).add_to(m)
            except Exception as e:
                print(e)    
            
        self._map = m
        