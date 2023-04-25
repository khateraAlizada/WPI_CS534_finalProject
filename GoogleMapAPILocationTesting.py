import requests

import Graph
import Pathfinding


def main():
    print("Welcome to the Touring Popular Tourist Attractions application!")
    # TODO: Add more output giving description of the application

    chosen_city = input("Please enter the desired city: ")  # TODO: Add error handling for wrong input types

    # Google Maps Places API setup
    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': 'tourist attractions in ' + chosen_city,
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
    attractions = []

    # Print the name, address, and location of each attraction
    for result in results:
        name = result['name']
        address = result['formatted_address']
        location = result['geometry']['location']
        lat, lng = location['lat'], location['lng']

        # Append the tourist attraction as a tuple
        attractions.append((name, address, lat, lng))

    # Prints out all tourist attractions that were found for the user's desired city
    print_attractions(attractions, chosen_city)

    # TODO: Add error handling if a given city cannot be found
    while True:
        start_attraction = input("Choose an attraction that you want to start your route at (enter !attractions to bring up the list of attractions again): ")
        input_result = valid_input(attractions, start_attraction)

        if input_result != 0 and input_result == 1:
            print_attractions(attractions, chosen_city)
            break
        else:
            print("Couldn't not find the start attraction. Please try again (enter !attractions to bring up the list of attractions again): ")

    while True:
        end_attraction = input("Choose an attraction that you want to start your route at (enter !attractions to bring up the list of attractions again): ")
        input_result = valid_input(attractions, end_attraction)

        if input_result != 0 and input_result == 1:
            print_attractions(attractions, chosen_city)
            break
        else:
            print("Couldn't not find the start attraction. Please try again (enter !attractions to bring up the list of attractions again): ")

    # TODO: Actual attractions list should be whatever the user chooses from the full list of possible tourist attractions
    # Create a NetworkX Graph
    loc_graph = Graph.create_graph(attractions)

    # TODO: Can be deleted; only for testing purposes
    # print("Is it connected?")
    # print(nx.is_connected(loc_graph))

    # TODO: Can be deleted; only for testing purposes
    # Graph.visualize_graph(loc_graph, save_path='graph.png')
    # Graph.print_graph(loc_graph)

    path = Pathfinding.a_star(start_attraction, end_attraction, loc_graph)
    print(path)  # TODO: Path will be used in later code to draw the path on an actual map


def print_attractions(attractions, chosen_city):
    print(f"Showing all tourist attractions for: {chosen_city}\n")

    for attraction in attractions:
        print(f"{attraction[0]}, Address: {attraction[1]}")


def valid_attraction(attractions, target_attraction):  # TODO: This is not actually mapping the proper input and attraction
    for attraction in attractions:
        if attraction[0] == target_attraction:
            return True
    return False


def valid_input(attractions, input_message):  # TODO: Might be overcomplicating with the 3 different results
    if input_message.startswith("!"):
        return 1
    elif valid_attraction(attractions, input_message):
        return 2
    return 0


if __name__ == "__main__":
    main()
