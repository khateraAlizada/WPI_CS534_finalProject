import requests


def main():
    # Set the API endpoint and parameters
    endpoint = 'https://maps.googleapis.com/maps/api/place/textsearch/json'
    params = {
        'query': 'tourist attractions in Boston',
        'type': 'tourist_attraction',
        'key': 'API_KEY_GOES_HERE'
    }

    # Send the API request and parse the response
    results = []
    next_page_token = ''
    while len(results) < 100:
        response = requests.get(endpoint, params=params)
        data = response.json()
        results.extend(data['results'])
        if 'next_page_token' in data:
            next_page_token = data['next_page_token']
            params['pagetoken'] = next_page_token
        else:
            break

    # Print the name, address, and location of each attraction
    for result in results[:100]:
        name = result['name']
        address = result['formatted_address']
        location = result['geometry']['location']
        lat, lng = location['lat'], location['lng']
        print(f'{name}, {address}, ({lat}, {lng})')


if __name__ == "__main__":
    main()
