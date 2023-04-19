import math
import heapq


def print_path(path):  # Custom path output formatting
    print("Path: ", end="")

    for i in range(0, len(path) - 1):
        print(path[i], end=" -> ")
    print(path[-1])


class SimpleProblemSolvingAgent:
    """Initializes a SimpleProblemSolvingAgent (SPSA) Object.

    :param map_graph: Undirected Graph representing the given map of Romania
    :param map_locations: Dictionary containing the Cartesian coordinates of cities on the Romania map
    :param start: The given start city
    :param goal: The Destination city
    :returns: None
    """

    def __init__(self, map_graph, map_locations, start, goal):
        self.map_Graph = map_graph
        self.map_locations = map_locations
        self.start = start
        self.goal = goal

    """Calculates the straight-line distance from the start city to the goal city.

    :param start: The given start city
    :param goal: The given destination city
    :returns: The straight-line distance between the given cities.
    """

    def straight_line_heuristic(self, start, goal):
        x1 = self.map_locations[start][0]
        y1 = self.map_locations[start][1]
        x2 = self.map_locations[goal][0]
        y2 = self.map_locations[goal][1]
        return math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2))  # Pythagorean Theorem

    """Pathfinding algorithm using both Greedy Best-First Search and A* Search.

    :param search_type: The algorithm to be performed
    :returns: An array containing the solution path
    """

    def search(self, search_type):
        paths_list = [(0, self.start, [self.start])]  # Keep track of paths
        visited_cities = set()  # Keep track of visited cities

        while paths_list:
            (weight, currCity, path) = heapq.heappop(paths_list)  # Get the lowest weighted path

            if currCity not in visited_cities:  # New city
                visited_cities.add(currCity)
            else:  # Already visited
                continue

            if currCity == self.goal:  # Destination city has been reached
                print("Total Cost is: " + str(self.calculate_path_cost(path)))
                print_path(path)
                return

            for neighbor in self.map_Graph.get(currCity).keys():
                if search_type == "Greedy Best First Search":
                    weight = self.straight_line_heuristic(neighbor, self.goal)  # h(n)
                elif search_type == "A* Search":
                    weight = self.straight_line_heuristic(self.start, neighbor) + self.straight_line_heuristic(neighbor,
                                                                                                               self.goal)  # g(n) + h(n)
                heapq.heappush(paths_list, (weight, neighbor, path + [neighbor]))  # Push updated path back into heap
        return None

    """Calculates the given path's distance

    :param path: An array representing the path
    :return: The total distance traveled
    """

    def calculate_path_cost(self, path):
        cost = 0

        for i in range(0, len(path) - 1):
            cost += self.map_Graph.get(path[i], path[i + 1])
        return cost
