from geo_data import GeoData
from work_class import WorkClass
import pandas as pd
from google_data import GoogleMapsApiData
from free_source_data import FreeSourceData
from datetime import datetime
import time

start = datetime.now()
print(f'start: {start.strftime("%X")}')

# api_data_class = GoogleMapsApiData(GoogleMapsApiData.WALK_MODE)
# api_data_class = FreeSourceData()

columns_to_read=['lat', 'lng', 'close_coordinates', 'closest_path_branch', 'distance_path', 'closest_path_coordinates']
# branches = pd.read_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\branches_ukr_co.csv', sep=';')
terminals = pd.read_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\terminals_from_res.csv', sep=';', usecols=columns_to_read).drop_duplicates()
terminals.to_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\nearest_df.csv', sep=';', index=False)
print(terminals)


