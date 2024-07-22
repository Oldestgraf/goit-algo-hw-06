import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Створення графа для моделювання тролейбусної мережі міста Одеса
G = nx.Graph()

# Додавання вершин, що представляють вузлові станції  в місті
locations = ['вул. Архітекторська', 'Майдан Толбухіна', 'Аркадія', '25-ї Чапаєвської дивізії', 'Аеропорт',
             'Застава 1', 'ВАТ Олімп-коло', 'Майдан ім. Толстого', 'вул. Новосельського', 'Грецький майдан', 'Пересинський міст',
             'Залізничний вокзал', 'Куликове Поле', 'ЦПКіВ ім. Шевченка']
G.add_nodes_from(locations)

# Додавання ребер, що представляють транспортні маршрути між станціями
transport_routes = [
    ('вул. Архітекторська', 'Майдан Толбухіна'),
    ('Майдан Толбухіна', 'Застава 1'),
    ('вул. Архітекторська', 'Залізничний вокзал'),
    ('Аркадія', '25-ї Чапаєвської дивізії'),
    ('Аркадія', 'Грецький майдан'),
    ('25-ї Чапаєвської дивізії', 'Пересинський міст'),
    ('25-ї Чапаєвської дивізії', 'Грецький майдан'),
    ('Аеропорт', 'Застава 1'),
    ('Застава 1', 'ЦПКіВ ім. Шевченка'),
    ('ВАТ Олімп-коло', 'Залізничний вокзал'),
    ('Майдан ім. Толстого', 'Залізничний вокзал'),
    ('вул. Новосельського', 'Куликове Поле'),
    ('вул. Новосельського', 'ЦПКіВ ім. Шевченка'),
    ('Залізничний вокзал', 'Пересинський міст')
]
G.add_edges_from(transport_routes)

# Візуалізація графа
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightgreen", font_size=12, font_weight="bold")
plt.show()

# Аналіз графа
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())
degree_df = pd.DataFrame(degrees.items(), columns=['Location', 'Degree'])

print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")
print(degree_df)

# Алгоритми DFS і BFS
def dfs_path(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in set(graph.neighbors(vertex)) - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

def bfs_path(graph, start, goal):
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in set(graph.neighbors(vertex)) - set(path):
            if next == goal:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

# Приклади використання алгоритмів для знаходження шляху від 'Аеропорт' до 'Аркадія'
start_node = 'Аеропорт'
end_node = 'Аркадія'

dfs_paths = list(dfs_path(G, start_node, end_node))
bfs_paths = list(bfs_path(G, start_node, end_node))

print("\nDFS Paths:")
for path in dfs_paths:
    print(path)

print("\nBFS Paths:")
for path in bfs_paths:
    print(path)

# Порівняння результатів
print(f"\nNumber of DFS Paths: {len(dfs_paths)}")
print(f"Number of BFS Paths: {len(bfs_paths)}")