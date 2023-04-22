import requests

import Graph
import Pathfinding


def main():
    # Google Maps API setup
    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': 'tourist attractions in London',  # TODO: Obtain the city from user input
        'type': 'tourist_attraction',
        'key': 'AIzaSyCHVwZYSee6FofPyTYNwGnEap6nGe-D24s'  # TODO: Need to put your own API key here for the program to work!!!
    }

    # Send the API request and parse the response
    results = []
    while len(results) < 100:
        response = requests.get(endpoint, params=params)
        data = response.json()
        results.extend(data['results'])
        if 'next_page_token' in data:
            next_page_token = data['next_page_token']
            params['pagetoken'] = next_page_token
        else:
            break

    # List to store the tourist attractions retrieved from Google Maps API
    locations = []

    # Print the name, address, and location of each attraction
    for result in results:
        name = result['name']
        address = result['formatted_address']
        location = result['geometry']['location']
        lat, lng = location['lat'], location['lng']

        # Append the tourist attraction as a tuple
        locations.append((name, address, lat, lng))

    # TODO: Can be deleted later; only for testing purposes

    # Seems that from the time this project was started to now, Public Garden's data from Google Maps API seems to have changed slightly
    # start_attraction = ('Public Garden', '4 Charles St, Boston, MA 02116, United States', 42.35462039999999, -71.070785)
    # start_attraction = ('Public Garden', 'Boston, MA 02116, United States', 42.3540639, -71.0700921)
    # end_attraction = ('Fenway Park', '4 Jersey St, Boston, MA 02215, United States', 42.3466764, -71.0972178)

    # start_attraction = ('Bunker Hill Monument', 'Monument Sq, Charlestown, MA 02129, United States', 42.3763541, -71.0607764)
    # end_attraction = ("Boston Children's Museum", '308 Congress St, Boston, MA 02210, United States', 42.3519736, -71.04968389999999)

    # Absolute random ass attraction guesses for London
    start_attraction = locations[0]
    end_attraction = locations[5]

    # Create a NetworkX Graph
    loc_graph = Graph.create_graph(locations)

    # TODO: Can be deleted; only for testing purposes
    # print("Is it connected?")
    # print(nx.is_connected(loc_graph))

    # TODO: Can be deleted; only for testing purposes
    # Graph.visualize_graph(loc_graph, save_path='graph.png')
    # Graph.print_graph(loc_graph)

    path = Pathfinding.a_star(start_attraction, end_attraction, loc_graph)
    print(path)  # TODO: Path will be used in later code to draw the path on an actual map


if __name__ == "__main__":
    main()
