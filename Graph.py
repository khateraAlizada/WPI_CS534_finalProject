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

    # Create a graph with nodes for each cluster
    graph = nx.Graph()
    for i in range(num_clusters):
        graph.add_node(i, location=cluster_centers[i], cluster=i)

    # Add respective attractions to their cluster
    for i in range(len(attractions)):
        # Get the Haversine Distances from a given attraction to all other clusters
        distances = [Pathfinding.haversine_distance(attractions[i][2], attractions[i][3], cluster_centers[j][0], cluster_centers[j][1]) for j in range(num_clusters)]

        # Determine the cluster it's a part of (aka the closest cluster)
        closest_cluster = min(range(num_clusters), key=lambda j: distances[j])

        # Create a list to store attractions in a given cluster if it hasn't already been created
        if 'attractions' not in graph.nodes[closest_cluster]:
            graph.nodes[closest_cluster]['attractions'] = []

        graph.nodes[closest_cluster]['attractions'].append(attractions[i])

    # Add edges between attractions in the same cluster
    for i in range(len(attractions)):
        for j in range(i + 1, len(attractions)):
            if clusters[i] == clusters[j]:
                attraction1 = attractions[i]
                attraction2 = attractions[j]
                distance = Pathfinding.haversine_distance(attraction1[2], attraction1[3], attraction2[2], attraction2[3])
                graph.add_edge(clusters[i], clusters[j], weight=distance)

    # Add edges between the clusters themselves
    for i in range(num_clusters):
        for j in range(i + 1, num_clusters):
            distance = Pathfinding.haversine_distance(cluster_centers[i][0], cluster_centers[i][1], cluster_centers[j][0], cluster_centers[j][1])
            graph.add_edge(i, j, weight=distance)

    return graph


# Debugging purposes: for getting a visual of the graph itself
def visualize_graph(graph, save_path=None):
    pos = {}
    labels = {}

    # Add positions and labels for cluster nodes
    for node in graph.nodes:
        pos[node] = graph.nodes[node]['location']
        labels[node] = f'Cluster {node}'

    # Add positions and labels for attraction nodes
    for node in graph.nodes:
        if 'attractions' in graph.nodes[node]:
            attractions = graph.nodes[node]['attractions']
            for i, attraction in enumerate(attractions):
                pos[f'{node}.{i}'] = (attraction[3], attraction[2])  # Flip coordinates for proper display
                labels[f'{node}.{i}'] = f'{attraction[0]}'

    # Draw edges between clusters
    cluster_edges = [(u, v) for u, v in graph.edges if
                     'attractions' not in graph.nodes[u] or 'attractions' not in graph.nodes[v]]
    cluster_edges = [(u, v) for u, v in graph.edges if
                     ('attractions' not in graph.nodes[u] and 'attractions' not in graph.nodes[v])
                     or ('attractions' in graph.nodes[u] and 'attractions' not in graph.nodes[v])
                     or ('attractions' not in graph.nodes[u] and 'attractions' in graph.nodes[v])]

    nx.draw_networkx_edges(graph, pos, edgelist=cluster_edges)

    # Draw edges between attractions within each cluster
    for node in graph.nodes:
        if 'attractions' in graph.nodes[node]:
            attractions = graph.nodes[node]['attractions']
            attraction_edges = [(f'{node}.{i}', f'{node}.{j}') for i in range(len(attractions)) for j in
                                range(i + 1, len(attractions))]
            nx.draw_networkx_edges(graph, pos, edgelist=attraction_edges)

    # Draw nodes for clusters and attractions
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=[node for node in graph.nodes if 'attractions' not in graph.nodes[node]],
                           node_color='b')
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=[f'{node}.{i}' for node in graph.nodes if 'attractions' in graph.nodes[node] for i
                                     in range(len(graph.nodes[node]['attractions']))], node_color='r', node_size=50)

    # Add labels for clusters and attractions
    nx.draw_networkx_labels(graph, pos, labels=labels)

    # Set the size of the figure
    plt.gcf().set_size_inches(48, 32)

    # Show plot
    plt.axis('off')
    plt.show()  # TODO Note that this doesn't work if matlab plt uses 'Agg', which is needed to save the graph.png properly (doesn't really matter either way cause this is just for debugging)

    if save_path is not None:
        plt.gcf().set_size_inches(48, 32)
        plt.savefig(save_path, bbox_inches='tight')


# Debugging purposes: for seeing the actual attractions in each resulting cluster
def print_clusters(graph):
    clusters = set(nx.get_node_attributes(graph, 'cluster').values())
    for cluster in clusters:
        print("Cluster " + str(cluster) + ": ")

        nodes = [n for n, d in graph.nodes(data=True) if d['cluster'] == cluster]
        attractions = []
        for node in nodes:
            attractions += graph.nodes[node]['attractions']
        print("Attractions: " + str(attractions))

        edges = [e for e in graph.edges() if e[0] in nodes and e[1] in nodes]
        print(f"Edges: {edges}")
