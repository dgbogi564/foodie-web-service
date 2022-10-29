import requests

# 2. Passing some input
def get_nearby_restaurants(server, address):
    request = requests.get(server, params={'address': address})
    print(request.text)


if __name__ == "__main__":
    get_nearby_restaurants('http://127.0.0.1:5000/restaurants',
                           None)
