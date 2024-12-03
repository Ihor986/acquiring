from geo_data import GeoData
from work_class import WorkClass, CLMS
import pandas as pd
from google_data import GoogleMapsApiData
from free_source_data import FreeSourceData
from datetime import datetime
import time

start = datetime.now()
print(f'start: {start.strftime("%X")}')
clms = CLMS()
# api_data_class = GoogleMapsApiData()
api_data_class = FreeSourceData()



branches = pd.read_csv('D:\\резюме\\райф\\acquiring_data\\input_csv\\branches_ukr.csv', sep=';', index_col=False)
terminals = pd.read_csv('D:\\резюме\\райф\\acquiring_data\\input_csv\\terminals_ukr.csv', sep=';', index_col=False, nrows=20)
address_df = pd.read_csv('D:\\резюме\\райф\\acquiring_data\\input_csv\\address_df.csv', sep=';', index_col=False)
# nearest_df = pd.read_csv('D:\\резюме\\райф\\acquiring_data\\input_csv\\nearest_df.csv', sep=';', index_col=False)
# address_df = None
nearest_df = None

geo_data:GeoData = GeoData(api_data_class)
workclass = WorkClass(clms=clms, branches=branches, terminals=terminals, geo_data=geo_data, addres_df=address_df, nearest_df=nearest_df)

workclass.add_branches_coordinates()
workclass.add_terminals_coordinates()
workclass.add_nearest_branch(100, 10)
workclass.add_nearest_path_branch()
workclass.visualize_branches_and_terminals()

workclass.map.save('D:\\резюме\\райф\\acquiring_data\\result\\html\\my_map_test.html')
workclass.terminals.to_csv('D:\\резюме\\райф\\acquiring_data\\result\\csv\\terminals_test.csv', sep=';', index=False)
# workclass.address_df.to_csv('D:\\резюме\\райф\\acquiring_data\\result\\csv\\address_df_test.csv', sep=';', index=False)
# workclass.nearest_df.to_csv('D:\\резюме\\райф\\acquiring_data\\result\\csv\\nearest_df_test.csv', sep=';', index=False)

print(workclass.branches)
print(workclass.terminals)
# print(workclass.address_df)
# print(workclass.nearest_df)

count_google_requests = api_data_class.count_requests if isinstance(api_data_class, GoogleMapsApiData) else 0
print(f'{count_google_requests=}')
print((datetime.now()-start))


































# unique_addresses_branches_list = branches['address'].str.lower().unique().tolist()
# unique_addresses_terminals_list = terminals['address'].str.lower().unique().tolist()

# addrs = {}

# for addr in tuple(unique_addresses_branches_list + unique_addresses_terminals_list):
#     print(addr)
#     addrs[addr] = get_coordinates_from_geopy(addr)
    
# print(addrs)

# terminals[['lat', 'lng', 'adrs']] = terminals['address'].str.lower().apply(lambda x: pd.Series(addrs.get(x)))
# branches[['lat', 'lng', 'adrs']] = branches['address'].str.lower().apply(lambda x: pd.Series(addrs.get(x)))



# branches.to_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\branches3.csv', sep=';')
# terminals.to_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\terminals3.csv', sep=';')

# branches = pd.read_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\branches2.csv', sep=';')
# terminals = pd.read_csv('D:\\резюме\\райф\\testSpark\\pos_branch\\terminals2.csv', sep=';', nrows=10)

# print(branches)
# print(terminals)


# Отримуємо координати
# branches['coordinates'] = branches['address'].apply(get_coordinates_from_geopy)
# terminals['coordinates'] = terminals['address'].apply(get_coordinates_from_geopy)


# Дані
# branches = pd.DataFrame({
#     'номер': [1, 2],
#     'адреса': ['вул. Бориса Грінченка, 9, Київ', 'вул. Саксаганського, 121, Київ'],
#     'місто': ['Київ', 'Київ']
    
# })

# terminals = pd.DataFrame({
#     'номер': [101, 102, 103],
#     'адреса': ['вул. Хрещатик, 22, Київ', 'вул. Лесі Українки, 7, Київ', 'вул. Володимирська, 50, Київ'],
#     'місто': ['Київ', 'Київ', 'Київ']
# })

# # Створюємо граф міста
# city_graph = ox.graph_from_place("Київ, Україна", network_type="drive")

# # Функція для обчислення відстаней
# def calculate_distance(term_coord, branch_coords):
#     try:
#         term_node = ox.nearest_nodes(city_graph, term_coord[1], term_coord[0])
#         branch_nodes = [
#             (ox.nearest_nodes(city_graph, coord[1], coord[0]), branch_id)
#             for branch_id, coord in branch_coords
#         ]
#         distances = {}
#         for branch_node, branch_id in branch_nodes:
#             try:
#                 distance = nx.shortest_path_length(
#                     city_graph, term_node, branch_node, weight="length"
#                 )
#                 distances[branch_id] = distance
#             except nx.NetworkXNoPath:
#                 distances[branch_id] = float('inf')        
#         return sorted(distances.items(), key=lambda x: x[1])[:2]
#     except Exception as e:
#         print(f"Помилка: {e}")
#         return []

# # Обчислюємо для кожного термінала
# terminals['найближчі1'] = terminals.apply(
#     lambda row: calculate_distance(
#         row['координати'],
#         branches[['номер', 'координати']].values
#     )[0], axis=1
# )
# terminals['найближчі2'] = terminals.apply(
#     lambda row: calculate_distance(
#         row['координати'],
#         branches[['номер', 'координати']].values
#     )[1], axis=1
# )

# # Результат
# print(terminals)










