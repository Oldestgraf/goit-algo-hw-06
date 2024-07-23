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

# Додавання ребер, що представляють транспортні маршрути між станціями з вагами (довжини маршрутів)
transport_routes = [
    ('вул. Архітекторська', 'Майдан Толбухіна', 5),
    ('Майдан Толбухіна', 'Застава 1', 3),
    ('вул. Архітекторська', 'Залізничний вокзал', 8),
    ('Аркадія', '25-ї Чапаєвської дивізії', 6),
    ('Аркадія', 'Грецький майдан', 4),
    ('25-ї Чапаєвської дивізії', 'Пересинський міст', 7),
    ('25-ї Чапаєвської дивізії', 'Грецький майдан', 5),
    ('Аеропорт', 'Застава 1', 6),
    ('Застава 1', 'ЦПКіВ ім. Шевченка', 8),
    ('ВАТ Олімп-коло', 'Залізничний вокзал', 4),
    ('Майдан ім. Толстого', 'Залізничний вокзал', 2),
    ('вул. Новосельського', 'Куликове Поле', 5),
    ('вул. Новосельського', 'ЦПКіВ ім. Шевченка', 7),
    ('Залізничний вокзал', 'Пересинський міст', 3)
]
G.add_weighted_edges_from(transport_routes)

# Візуалізація графа
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightgreen", font_size=12, font_weight="bold", edge_color='grey')
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.title("Trolleybus Network of Odessa with Weights")
plt.show()

# Аналіз графа
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
degrees = dict(G.degree())
degree_df = pd.DataFrame(degrees.items(), columns=['Location', 'Degree'])

print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {num_edges}")
print(degree_df)

# Реалізація алгоритму Дейкстри
def dijkstra(graph, start):
    # Ініціалізація відстаней та множини невідвіданих вершин
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0
    unvisited = list(graph.keys())

    while unvisited:
        # Знаходження вершини з найменшою відстанню серед невідвіданих
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        # Якщо поточна відстань є нескінченністю, то ми завершили роботу
        if distances[current_vertex] == float('infinity'):
            break

        for neighbor, weight in graph[current_vertex].items():
            distance = distances[current_vertex] + weight['weight']

            # Якщо нова відстань коротша, то оновлюємо найкоротший шлях
            if distance < distances[neighbor]:
                distances[neighbor] = distance

        # Видаляємо поточну вершину з множини невідвіданих
        unvisited.remove(current_vertex)

    return distances

# Функція для відновлення шляху з результатів алгоритму Дейкстри
def get_path(shortest_paths, start, goal):
    path = []
    current_node = goal
    while current_node != start:
        if current_node is None:
            return None
        path.append(current_node)
        next_node = shortest_paths[current_node][0]
        current_node = next_node
    path.append(start)
    path = path[::-1]
    return path

# Знаходження найкоротшого шляху від 'Аеропорт' до 'Аркадія'
start_node = 'Аеропорт'
end_node = 'Аркадія'
shortest_paths = dijkstra(nx.to_dict_of_dicts(G), start_node)
print("\nDijkstra Shortest Path from 'Аеропорт' to 'Аркадія':")
print(shortest_paths[end_node])

# Знаходження найкоротшого шляху між всіма вершинами графа
all_pairs_shortest_path = {}
for start in G.nodes:
    shortest_paths = dijkstra(nx.to_dict_of_dicts(G), start)
    all_pairs_shortest_path[start] = shortest_paths

print("\nDijkstra Shortest Paths between all pairs of nodes:")
for start in all_pairs_shortest_path:
    for end in all_pairs_shortest_path[start]:
        print(f"{start} -> {end}: {all_pairs_shortest_path[start][end]}")
