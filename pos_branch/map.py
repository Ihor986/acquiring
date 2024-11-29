import osmnx as ox
import networkx as nx

# regions_districts = {
#     "Вінницька": [
#         "Вінницький",
#         "Гайсинський",
#         "Жмеринський",
#         "Калинівський",
#         "Козятинський",
#         "Літинський",
#         "Могилів-Подільський",
#         "Тиврівський",
#         "Томашпільський",
#         "Хмільницький",
#         "Черкаський",
#         "Шаргородський"
#     ],
#     "Волинська": [
#         "Володимир-Волинський",
#         "Горохівський",
#         "Іваничівський",
#         "Ківерцівський",
#         "Локачинський",
#         "Луцький",
#         "Маневицький",
#         "Ратнівський",
#         "Рожищенський",
#         "Шацький"
#     ]
#     # "Дніпропетровська": [
#     #     "Апостолівський",
#     #     "Дніпровський",
#     #     "Криворізький",
#     #     "Марганецький",
#     #     "Нікопольський",
#     #     "Новомосковський",
#     #     "Петропавлівський",
#     #     "Синельниківський",
#     #     "Томаківський",
#     #     "Царичанський",
#     #     "Широківський"
#     # ],
#     # "Донецька": [
#     #     "Волноваський",
#     #     "Горлівський",
#     #     "Дебальцевський",
#     #     "Донецький",
#     #     "Краматорський",
#     #     "Маріупольський",
#     #     "Мирноградський",
#     #     "Слов'янський",
#     #     "Торецький",
#     #     "Шахтарський"
#     # ],
#     # "Житомирська": [
#     #     "Бердичівський",
#     #     "Житомирський",
#     #     "Коростишівський",
#     #     "Любарський",
#     #     "Малинський",
#     #     "Новоград-Волинський",
#     #     "Овруцький",
#     #     "Романівський",
#     #     "Чуднівський"
#     # ],
#     # "Закарпатська": [
#     #     "Берегівський",
#     #     "Виноградівський",
#     #     "Іршавський",
#     #     "Міжгірський",
#     #     "Мукачівський",
#     #     "Рахівський",
#     #     "Свалявський",
#     #     "Тячівський",
#     #     "Ужгородський"
#     # ],
#     # "Запорізька": [
#     #     "Бердянський",
#     #     "Василівський",
#     #     "Гуляйпільський",
#     #     "Запорізький",
#     #     "Кам'янсько-Дніпровський",
#     #     "Мелітопольський",
#     #     "Пологи",
#     #     "Токмацький",
#     #     "Чарівненський"
#     # ],
#     # "Івано-Франківська": [
#     #     "Галицький",
#     #     "Долинський",
#     #     "Коломийський",
#     #     "Косівський",
#     #     "Рогатинський",
#     #     "Снятинський",
#     #     "Тисменицький",
#     #     "Тлумацький"
#     # ],
#     # "Київська": [
#     #     "Броварський",
#     #     "Боярський",
#     #     "Васильківський",
#     #     "Вишгородський",
#     #     "Іванківський",
#     #     "Обухівський",
#     #     "Переяслав-Хмельницький",
#     #     "Фастівський",
#     #     "Яготинський"
#     # ],
#     # "Луганська": [
#     #     "Антрацитівський",
#     #     "Слов'яносербський",
#     #     "Троїцький",
#     #     "Щастинський",
#     #     "Лисичанський",
#     #     "Старобільський",
#     #     "Сватівський",
#     #     "Новопсковський"
#     # ],
#     # "Львівська": [
#     #     "Бродівський",
#     #     "Дрогобицький",
#     #     "Золочівський",
#     #     "Комарнівський",
#     #     "Львівський",
#     #     "Миколаївський",
#     #     "Самбірський",
#     #     "Стрийський",
#     #     "Турківський",
#     #     "Червоноградський"
#     # ],
#     # "Миколаївська": [
#     #     "Баштанський",
#     #     "Врадіївський",
#     #     "Первомайський",
#     #     "Очаківський",
#     #     "Миколаївський",
#     #     "Снігурівський",
#     #     "Южноукраїнський"
#     # ],
#     # "Одеська": [
#     #     "Білгород-Дністровський",
#     #     "Ізмаїльський",
#     #     "Овідіопольський",
#     #     "Ренійський",
#     #     "Татарбунарський",
#     #     "Теплодарський",
#     #     "Ширяївський"
#     # ],
#     # "Полтавська": [
#     #     "Гадяцький",
#     #     "Глобинський",
#     #     "Кременчуцький",
#     #     "Лубенський",
#     #     "Миргородський",
#     #     "Полтавський",
#     #     "Хорольський",
#     #     "Чорнухинський"
#     # ],
#     # "Рівненська": [
#     #     "Березнівський",
#     #     "Володимирецький",
#     #     "Гощанський",
#     #     "Дубровицький",
#     #     "Зарічненський",
#     #     "Рівненський",
#     #     "Сарненський"
#     # ],
#     # "Сумська": [
#     #     "Білопільський",
#     #     "Глухівський",
#     #     "Конотопський",
#     #     "Краснопільський",
#     #     "Охтирський",
#     #     "Роменський",
#     #     "Сумський",
#     #     "Тростянецький",
#     #     "Шосткинський"
#     # ],
#     # "Тернопільська": [
#     #     "Бережанський",
#     #     "Борщівський",
#     #     "Гусятинський",
#     #     "Кременецький",
#     #     "Тернопільський",
#     #     "Чортківський"
#     # ],
#     # "Харківська": [
#     #     "Балаклійський",
#     #     "Вовчанський",
#     #     "Дергачівський",
#     #     "Зміївський",
#     #     "Ізюмський",
#     #     "Красноградський",
#     #     "Лозівський",
#     #     "Харківський",
#     #     "Чугуївський"
#     # ],
#     # "Херсонська": [
#     #     "Генічеський",
#     #     "Каланчакський",
#     #     "Новотроїцький",
#     #     "Скадовський",
#     #     "Цюрупинський",
#     #     "Херсонський"
#     # ],
#     # "Хмельницька": [
#     #     "Білогірський",
#     #     "Деражнянський",
#     #     "Красилівський",
#     #     "Летичівський",
#     #     "Шепетівський",
#     #     "Хмельницький",
#     #     "Чемеровецький"
#     # ],
#     # "Черкаська": [
#     #     "Білозірський",
#     #     "Звенигородський",
#     #     "Канівський",
#     #     "Корсунь-Шевченківський",
#     #     "Смілянський",
#     #     "Уманський",
#     #     "Черкаський",
#     #     "Шполянський"
#     # ],
#     # "Чернівецька": [
#     #     "Вижницький",
#     #     "Герцаївський",
#     #     "Кіцманський",
#     #     "Новоселицький",
#     #     "Сторожинецький",
#     #     "Чернівецький"
#     # ],
#     # "Чернігівська": [
#     #     "Бахмацький",
#     #     "Березнянський",
#     #     "Городнянський",
#     #     "Корюківський",
#     #     "Ніжинський",
#     #     "Новгород-Сіверський",
#     #     "Семенівський",
#     #     "Сосницький",
#     #     "Чернігівський"
#     # ]
# }


# def download_region_graph(region, district):
#     place = f"{district}, {region}, Україна"
#     print(f"Завантаження графа для {place}...")
#     graph = ox.graph_from_place(place, network_type='walk')
#     return graph

# # Список для збереження графів
# all_graphs = []
# skiped = []

# # Завантаження графів для всіх районів
# for region, districts in regions_districts.items():
#     for district in districts:
#         try:
#             graph = download_region_graph(region, district)
#             all_graphs.append(graph)
#             print( f"{district}, {region}, Ukraine downloaded" )
#         except:
#             skiped.append(f"{district}, {region}, Ukraine")
#             print( f"{district}, {region}, Ukraine canseled" )
            
# print(skiped)

# # Об'єднання всіх графів
# combined_graph = nx.compose_all(all_graphs)

# # Збереження об'єднаного графа
# ox.save_graphml(combined_graph, "combined_ukraine_graph.graphml")









# Визначення назв усіх областей України
regions = ['Kyiv Oblast', 'Ivano-Frankivsk Oblast', 'Khmelnitskyi Oblast', 'Lviv Oblast',
'Odesa Oblast', 'Poltava Oblast', 'Rivne Oblast', 'Zaporizhzhia Oblast']


# [
#     "Kyiv Oblast", "Cherkasy Oblast", "Chernihiv Oblast", "Chernivtsi Oblast",
#     "Dnipropetrovsk Oblast", "Donetsk Oblast", "Ivano-Frankivsk Oblast", 
#     "Kharkiv Oblast", "Kherson Oblast", "Khmelnitskyi Oblast", 
#     "Lviv Oblast", "Mykolaiv Oblast", "Odesa Oblast", "Poltava Oblast", 
#     "Rivne Oblast", "Sumy Oblast", "Ternopil Oblast", "Vinnytsia Oblast", 
#     "Volyn Oblast", "Zakarpattia Oblast", "Zaporizhzhia Oblast", 
#     "Zhytomyr Oblast", "Kirovohrad Oblast", "Luhansk Oblast", "Ternopil Oblast"
# ]

# Ініціалізація списку графів
graphs = []

# Завантаження графів для кожної області
for region in regions:
    try:
        graph = ox.graph_from_place(region + ", Ukraine", network_type="walk")
        # graphs.append(graph)
        ox.save_graphml(graph, filepath=f"{region.replace(' ', '_')}_graph.graphml")
        print(f"Граф для {region} успішно завантажено.")
    except Exception as e:
        graphs.append(region)
        print(f"Не вдалося завантажити граф для {region}: {e}")
        
print(graphs)

# ['Kyiv Oblast', 'Ivano-Frankivsk Oblast', 'Khmelnitskyi Oblast', 'Lviv Oblast',
# 'Odesa Oblast', 'Poltava Oblast', 'Rivne Oblast', 'Zaporizhzhia Oblast']

# # Об'єднання всіх графів в один
# combined_graph = nx.compose_all(graphs)

# ox.save_graphml(combined_graph, filepath="combined_graph.graphml")