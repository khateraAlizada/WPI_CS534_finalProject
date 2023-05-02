import requests

import Graph
import Pathfinding
import Graph
import Pathfinding
import folium



def main():
    print("\nWelcome to the Touring Popular Tourist Attractions application!\n")
    # TODO: Add more output giving description of the application

    chosen_city = input("Please enter the desired city: ")  # TODO: Add error handling for wrong input types

    # Google Maps Places API setup
    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': 'tourist attractions in ' + chosen_city,
        'type': 'tourist_attraction',
        'key': ''  # TODO: Need to put your own API key here for the program to work!!!
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

    while True:
        start_attraction = input("\nChoose an attraction that you want to start your route at (enter !attractions to bring up the list of attractions again): ")

        if start_attraction == "!attractions":
            print_attractions(attractions, chosen_city)
            continue

        if valid_attraction(attractions, start_attraction):
            start_attraction = find_attraction(attractions, start_attraction)
            break
        else:
            print("Couldn't not find the end attraction. Please try again.")

    while True:
        end_attraction = input("\nChoose an attraction that you want to end your route at (enter !attractions to bring up the list of attractions again): ")

        if end_attraction == "!attractions":
            print_attractions(attractions, chosen_city)
            continue

        if valid_attraction(attractions, end_attraction):
            end_attraction = find_attraction(attractions, end_attraction)
            break
        else:
            print("Couldn't not find the end attraction. Please try again.")

    chosen_attractions = []

    chosen_attraction = input("Next, enter the attractions that interest you. (type !all to select all attractions, and !attractions to bring up the list of attractions again. Type !done to finish): ")

    while chosen_attraction != "!done":
        if chosen_attraction == "!attractions":
            print_attractions(attractions, chosen_city)
        elif chosen_attraction == "!all":
            chosen_attractions = attractions
            break  # Break out since there's nothing more to add
        elif chosen_attraction == "!list":
            print_chosen_attractions(start_attraction, end_attraction, chosen_attractions)
        elif valid_attraction(attractions, chosen_attraction):
            chosen_attractions.append(find_attraction(attractions, chosen_attraction))  # TODO: Need to add check that it isn't the selected start/end attraction
        else:
            print("Valid input not detected. Try again!")
        chosen_attraction = input(
            "Next, enter the attractions that interest you. (type !all to select all attractions, and !attractions to bring up the list of attractions again. Type !done to finish): ")

    # Create a NetworkX Graph
    loc_graph = Graph.create_graph(chosen_attractions)

    # Testing if the resulting graph is a connected graph
    # print("Is it connected?")
    # print(nx.is_connected(loc_graph))

    # Helper functions for visualizing the resulting attraction graph
    # Graph.visualize_graph(loc_graph, save_path='graph.png')
    # Graph.print_graph(loc_graph)

    path = Pathfinding.a_star(start_attraction, end_attraction, loc_graph)
    print(path)  # TODO: Path will be used in later code to draw the path on an actual map

    #############################
    # Gives one line
    # Create a map object centered at the first attraction with all the attractions
    map_center = (start_attraction[2], start_attraction[3])
    m = folium.Map(location=map_center, zoom_start=13)

    # Add markers for each attraction
    for attraction in attractions:
        name, address, lat, lng = attraction
        popup_text = f'{name}\n{address}'
        folium.Marker(location=(lat, lng), popup=popup_text).add_to(m)

    # # Add a polyline for the path, this will add lines
    # path_points = []
    # for attraction in path:
    #     name, address, lat, lng = attraction
    #     path_points.append((lat, lng))
    # folium.PolyLine(path_points, color='red').add_to(m)

    # Display the map
    m.save('map2.html')
    m
    # end of one line
    ##############################################

    import googlemaps
    import datetime
    from datetime import timedelta

    # Define your Google Maps API key

    gmaps = googlemaps.Client(key='')

    # The function path_to_locations modifies the path to a format that can be used in directions api
    def path_to_locations(path):
        locations = []
        for place in path:
            location_str = f"{place[0]}, {place[1]}, {place[2]}, {place[3]}"
            locations.append(location_str)
        return locations

    locations = path_to_locations(path)
    print(locations)

    # We could also use list of longitude and latitude
    # to display paths
    # get_lonlat creates gets longitude and latitude.
    def get_lonlat(locations):
        lonlat = []
        for location in locations:
            latlon_str = location.split(', ')[-2:]
            latlon = tuple(float(coord) for coord in latlon_str)
            lonlat.append(latlon)
        return lonlat

    lonlatTuples = get_lonlat(locations)
    print(lonlatTuples)
    #

    origin = locations[0]
    destination = locations[-1]

    #waypoints = lonlatTuples,

    results = gmaps.directions(origin=locations[0],
                               destination=locations[-1],
                               waypoints=locations,
                               optimize_waypoints=True,
                               departure_time=datetime.datetime.now() + timedelta(hours=1))

    print("direction result")
    print(results)

    marker_points = []
    waypoints = []

    # extract the location points from the previous directions function

    for leg in results[0]["legs"]:
        leg_start_loc = leg["start_location"]
        marker_points.append(f'{leg_start_loc["lat"]},{leg_start_loc["lng"]}')
        for step in leg["steps"]:
            end_loc = step["end_location"]
            waypoints.append(f'{end_loc["lat"]},{end_loc["lng"]}')
    last_stop = results[0]["legs"][-1]["end_location"]
    marker_points.append(f'{last_stop["lat"]},{last_stop["lng"]}')

    markers = ["color:blue|size:mid|label:" + chr(65 + i) + "|"
               + r for i, r in enumerate(marker_points)]
    print("markers")
    print(markers)
    print("marker points")
    print(marker_points)
    print("way points")
    print(waypoints)
    # center=waypoints[0],
    result_map = gmaps.static_map(
        center="Faneuil Hall Marketplace, Boston, MA",
        scale=2,
        zoom=14,
        size=[640, 640],
        format="jpg",
        maptype="roadmap",
        markers=markers,
        path="color:0x0000ff|weight:2|" + "|".join(waypoints))

    with open("bostonlonlat.jpg", "wb") as img:
        for chunk in result_map:
            img.write(chunk)


"""Prints all the tourist attractions for a given city.

:param attractions: the complete list of attractions
:param chosen_city: the city chosen by the user

:returns: void
"""
def print_attractions(attractions, chosen_city):
    print(f"Showing all tourist attractions for: {chosen_city}\n")

    for attraction in attractions:
        print(f"{attraction[0]}, Address: {attraction[1]}")


"""Prints all the other selected tourist attractions that the user is interested in.

:param start_attraction: the chosen start attraction
:param end_attraction: the chosen end attraction
:param chosen_attractions: the other attractions currently chosen

:returns: void
"""
def print_chosen_attractions(start_attraction, end_attraction, chosen_attractions):
    print(f"\nChosen start attraction: {start_attraction[0]}")
    print(f"Chosen end attraction: {end_attraction[0]}\n")

    print("Other interested attractions: ")
    for attraction in chosen_attractions:
        print(f"{attraction[0]}")


"""Checks if an inputted attraction actually exists for a given city.

:param attractions: the complete list of attractions
:param target_attraction: the attraction inputted by the user

:returns: boolean representing if a matching attraction was found
"""
def valid_attraction(attractions, target_attraction):  # TODO: Could be merged with find_attraction()
    for attraction in attractions:
        if attraction[0] == target_attraction:
            return True
    return False


"""Returns the attraction tuple object from the list of all attractions.

:param attractions: the complete list of attractions
:param target_attraction: the attraction inputted by the user

:returns: the matching attraction tuple, or None
"""
def find_attraction(attractions, target_attraction):  # TODO: Could be merged with valid_attraction()
    for attraction in attractions:
        if attraction[0] == target_attraction:
            return attraction
    return None


if __name__ == "__main__":
    main()
