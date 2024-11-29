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
api_data_class = FreeSourceData()


branches = pd.read_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\branches_ukr_co.csv', sep=';')
terminals = pd.read_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\terminals_test.csv', sep=';')
print(terminals)
geo_data:GeoData = GeoData(api_data_class)
workclass = WorkClass(branches=branches, terminals=terminals, geo_data=geo_data)

workclass.visualize_branches_and_terminals()
workclass.map.save('my_map_from_res.html')

print((datetime.now()-start))