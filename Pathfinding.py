import heapq
from math import radians, sin, cos, sqrt, atan2


"""Represents a tourist attraction.
"""
class Attraction:
    def __init__(self, attraction, name, latitude, longitude, cost, heuristic, parent=None):
        self.attraction = attraction
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent

    """Represents the A* heuristic of f(n) = g(n) + h(n), where g(n) is the cost from the start attraction to a given
       attraction, and h(n) represents the estimated heuristic from the given attraction to the end attraction.
    """
    def total_cost(self):
        return self.cost + self.heuristic

    """Custom definition to implement the functionality of the "<" operator on the Attraction class.
    """
    def __lt__(self, other):
        return self.total_cost() < other.total_cost()


"""Represents the Haversine Distance between two attractions.

:param lat1: The latitude value of the first attraction
:param lon2: The longitude value of the first attraction
:param lat2: The latitude value of the second attraction
:param lon2: The longitude value of the second attraction

:returns: The Haversine Distance between the two attractions (in km)
"""
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0  # radius of the Earth in kilometers
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


"""Performs the A* algorithm search to find a path from a start attraction to an end attraction, through a graph of other tourist attractions.

:param start_attraction: The attraction to start at
:param end_attraction: The attraction to end at
:param graph: A NetworkX Graph representing all possible tourist attractions

:returns: An optimal path from the start to end attraction
"""
def a_star(start_attraction, end_attraction, graph):
    # Convert the start and end attraction into equivalent Attraction class objects
    start_node = Attraction(start_attraction, start_attraction[0], start_attraction[2], start_attraction[3], 0, haversine_distance(start_attraction[2], start_attraction[3], end_attraction[2], end_attraction[3]))
    end_node = Attraction(end_attraction, end_attraction[0], end_attraction[2], end_attraction[3], 0, 0)

    # Represents a priority queue of (total path cost, current tourist attraction, current optimal path)
    paths_list = [(start_node.total_cost(), start_node, [start_node.attraction])]

    # Keep track of already visited tourist attractions
    visited = set()

    while paths_list:
        # Get the lowest weighted path
        (total_cost, current_node, path) = heapq.heappop(paths_list)

        # Return the resulting optimal path
        if current_node.latitude == end_node.latitude and current_node.longitude == end_node.longitude:
            return path

        # Add the current tourist attraction to visited if it's not already added, and skip it otherwise
        if (current_node.latitude, current_node.longitude) not in visited:
            visited.add((current_node.latitude, current_node.longitude))
        else:
            continue

        # Matches a Graph Node to an Attraction class object
        search_node = None

        for node, attributes in graph.nodes(data=True):
            if graph.nodes[node]['attraction'] == current_node.attraction:
                search_node = node

        # Expand neighbors
        for neighbor in graph.neighbors(search_node):
            # Extract Graph Node attribute values
            attraction = graph.nodes[neighbor]['attraction']
            name = graph.nodes[neighbor]['attraction'][0]
            latitude = graph.nodes[neighbor]['attraction'][2]
            longitude = graph.nodes[neighbor]['attraction'][3]
            cost = haversine_distance(start_node.latitude, start_node.longitude, latitude, longitude)  # g(n)
            heuristic = haversine_distance(latitude, longitude, end_node.latitude, end_node.longitude)  # h(n)
            parent = current_node

            # Construct a matching Attraction class object
            neighbor_attraction = Attraction(attraction, name, latitude, longitude, cost, heuristic, parent)
            heapq.heappush(paths_list, (neighbor_attraction.total_cost(), neighbor_attraction, path + [neighbor_attraction.attraction]))

    return None
