from math import radians, sin, cos, sqrt, atan2


class Node:
    def __init__(self, name, longitude, latitude, cost, heuristic, parent=None):
        self.name = name
        self.longitude = longitude
        self.latitude = latitude
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent

    def total_cost(self):
        return self.cost + self.heuristic


# Haversine Formula
def distance_between_points(lat1, lon1, lat2, lon2):
    R = 6371.0  # radius of the Earth in kilometers
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def heuristic_cost_estimate(location, goal_location):
    lon1 = float(location[2])
    lat1 = float(location[3])
    lon2 = float(goal_location[2])
    lat2 = float(goal_location[3])

    return distance_between_points(lat1, lon1, lat2, lon2)


def a_star(start_attraction, end_attraction, attractions):
    start_node = Node(start_attraction[0], start_attraction[2], start_attraction[3], 0, heuristic_cost_estimate(start_attraction, end_attraction))
    open_set = [start_node]
    visited = []

    while open_set:
        current_node = min(open_set, key=lambda x: x.total_cost())
        open_set.remove(current_node)

        if current_node.name == end_attraction[0] and len(visited) == len(attractions):
            path = []
            while current_node:
                path.append(current_node.name)
                current_node = current_node.parent
            return list(reversed(path))

        visited.append(current_node)

        for attraction in attractions:
            if attraction[0] == current_node.name or attraction in [node.name for node in visited]:
                continue

            cost = current_node.cost + distance_between_points(current_node.latitude, current_node.longitude, float(attraction[2]), float(attraction[3]))
            heuristic = heuristic_cost_estimate(attraction, end_attraction)
            new_node = Node(attraction[0], attraction[2], attraction[3], cost, heuristic, current_node)

            if any(node.name == new_node.name and node.total_cost() <= new_node.total_cost() for node in open_set):
                continue

            open_set.append(new_node)

    return None
