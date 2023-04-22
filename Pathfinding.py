import heapq
from math import radians, sin, cos, sqrt, atan2
import networkx as nx
from sklearn.cluster import KMeans


# Represents a tourist attraction location
class Node:
    def __init__(self, attraction, name, latitude, longitude, cost, heuristic, parent=None):
        self.attraction = attraction
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent

    def total_cost(self):
        return self.cost + self.heuristic


# Haversine Formula
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # radius of the Earth in kilometers
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def haversine_heuristic(location, goal_location):
    lat1 = float(location[2])
    lon1 = float(location[3])
    lat2 = float(goal_location[2])
    lon2 = float(goal_location[3])

    return haversine_distance(lat1, lon1, lat2, lon2)


def a_star(start_attraction, end_attraction, graph):
    start_node = Node(start_attraction, start_attraction[0], start_attraction[2], start_attraction[3], 0, haversine_distance(start_attraction[2], start_attraction[3], end_attraction[2], end_attraction[3]))
    end_node = Node(end_attraction, end_attraction[0], end_attraction[2], end_attraction[3], float('inf'), 0)
    paths_list = [(start_node.total_cost(), start_node)]  # priority queue of (total_cost, node)
    visited = set()

    while paths_list:
        _, current_node = heapq.heappop(paths_list)
        if current_node in visited:  # TODO thing cannot hash the attraction list; think of alternative
            continue
        if current_node.latitude == end_node.latitude and current_node.longitude == end_node.longitude:
            path = [current_node]
            while path[-1].parent is not None:
                path.append(path[-1].parent)
            return list(reversed([node.attraction for node in path]))

        visited.add(current_node)
        print("This is current node:")
        print(current_node.attraction)
        for neighbor in graph.neighbors(current_node):  # TODO Key Error; I think this has to be the full attraction array
            neighbor_node = Node(neighbor, neighbor[0], neighbor[2], neighbor[3], graph.edges[(current_node.latitude, current_node.longitude, neighbor[2], neighbor[3])]['weight'], haversine_distance(neighbor[2], neighbor[3], end_attraction[2], end_attraction[3]), current_node)
            heapq.heappush(paths_list, (neighbor_node.total_cost(), neighbor_node))

    return None
