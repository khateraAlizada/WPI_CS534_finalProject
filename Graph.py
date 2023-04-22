import networkx as nx
from sklearn.cluster import KMeans

import Pathfinding

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


def create_graph(attractions, num_clusters=5):
    # Extract Longitude/Latitude into a separate array
    coordinates = [[attraction[2], attraction[3]] for attraction in attractions]

    # Group attractions into clusters using K-Means Clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(coordinates)
    cluster_centers = kmeans.cluster_centers_
    clusters = kmeans.labels_

    # Create a graph with nodes for each attraction
    graph = nx.Graph()
    for i in range(len(attractions)):
        graph.add_node(i, attraction=attractions[i], location=(attractions[i][2], attractions[i][3]), cluster=clusters[i])

    # Add respective attractions to their cluster
    for i in range(len(attractions)):
        # Create a list to store attractions in a given cluster if it hasn't already been created
        if 'attractions' not in graph.nodes[clusters[i]]:
            graph.nodes[clusters[i]]['attractions'] = []

        graph.nodes[clusters[i]]['attractions'].append(i)

    # Add edges between attractions in the same cluster
    for i in range(len(attractions)):
        for j in range(i + 1, len(attractions)):
            if clusters[i] == clusters[j]:
                attraction1 = attractions[i]
                attraction2 = attractions[j]
                distance = Pathfinding.haversine_distance(attraction1[2], attraction1[3], attraction2[2], attraction2[3])
                graph.add_edge(i, j, weight=distance)

    # Keep track of which attractions have already been connected to another cluster
    already_connected = []

    # Add edges between the closest attractions between nearby clusters
    for i in range(num_clusters):
        for j in range(i + 1, num_clusters):
            # Find the closest attraction in each cluster to the other cluster
            min_distance = float('inf')
            closest_attractions = None
            for attraction1_id in graph.nodes[i]['attractions']:
                attraction1 = attractions[attraction1_id]
                for attraction2_id in graph.nodes[j]['attractions']:
                    attraction2 = attractions[attraction2_id]
                    distance = Pathfinding.haversine_distance(attraction1[2], attraction1[3], attraction2[2], attraction2[3])
                    if distance < min_distance:
                        min_distance = distance
                        closest_attractions = (attraction1_id, attraction2_id)

            # Add an edge between the closest attractions
            if closest_attractions[0] not in already_connected or closest_attractions[1] not in already_connected:
                graph.add_edge(closest_attractions[0], closest_attractions[1], weight=min_distance)
                already_connected.append(closest_attractions[0])
                already_connected.append(closest_attractions[1])

    return graph


# Debugging purposes: for getting a visual of the graph itself
def visualize_graph(graph, save_path=None):
    pos = {}
    labels = {}

    # Add positions and labels for attraction nodes
    for node in graph.nodes:
        attraction = graph.nodes[node]['attraction']
        pos[node] = (attraction[3], attraction[2])  # Flip coordinates for proper display
        labels[node] = f'{attraction[0]} (Cluster {graph.nodes[node]["cluster"]})'

    # Draw edges between attractions within each cluster
    attraction_edges = []
    for node in graph.nodes:
        for neighbor in graph.neighbors(node):
            if neighbor > node:
                attraction_edges.append((node, neighbor))

    nx.draw_networkx_edges(graph, pos, edgelist=attraction_edges)

    # Draw nodes for attractions
    node_colors = [graph.nodes[node]['cluster'] for node in graph.nodes]
    cmap = plt.get_cmap('viridis', len(set(node_colors)))
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=50, cmap=cmap)

    # Add labels for attractions
    nx.draw_networkx_labels(graph, pos, labels=labels)

    # Set the size of the figure
    plt.gcf().set_size_inches(48, 32)

    # Show plot
    plt.axis('off')

    if save_path is not None:
        plt.savefig(save_path)
    else:
        plt.show()



# Debugging purposes: for seeing the actual attractions in each resulting cluster
def print_clusters(graph):
    # Print all nodes and their attributes
    print("Nodes:")
    for node, attributes in graph.nodes(data=True):
        print(f"Node {node}: {attributes}")

    # Print all edges and their attributes
    print("Edges:")
    for edge in graph.edges(data=True):
        print(f"Edge {edge[0]} - {edge[1]}: {edge[2]}")

