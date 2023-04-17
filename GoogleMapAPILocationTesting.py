import requests
import Pathfinding


def main():
    # Set the API endpoint and parameters
    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': 'tourist attractions in Boston',
        'type': 'tourist_attraction',
        'key': ''  # Need to put API key here to work!!!
    }

    # Send the API request and parse the response
    results = []
    next_page_token = ' '
    while len(results) < 100:
        response = requests.get(endpoint, params=params)
        data = response.json()
        results.extend(data['results'])
        if 'next_page_token' in data:
            next_page_token = data['next_page_token']
            params['pagetoken'] = next_page_token
        else:
            break

    #locations = []

    locations = [['Public Garden', '4 Charles St, Boston, MA 02116, United States', 42.35462039999999, -71.070785], ['Boston Tea Party Ships & Museum', '306 Congress St, Boston, MA 02210, United States', 42.3521821, -71.0512911], ['Fenway Park', '4 Jersey St, Boston, MA 02215, United States', 42.3466764, -71.0972178]]

    # Print the name, address, and location of each attraction
    for result in results:
        name = result['name']
        address = result['formatted_address']
        location = result['geometry']['location']
        lat, lng = location['lat'], location['lng']
        # print(f'{name}, {address}, ({lat}, {lng})') TODO Commented out for now; prints the reformatted location from GMaps API result

        locations.append([name, address, lat, lng])

    print(locations)

    start_attraction = ['Public Garden', '4 Charles St, Boston, MA 02116, United States', 42.35462039999999, -71.070785]
    end_attraction = ['Fenway Park', '4 Jersey St, Boston, MA 02215, United States', 42.3466764, -71.0972178]

    path = Pathfinding.a_star(start_attraction, end_attraction, locations)
    print(path)


if __name__ == "__main__":
    main()
