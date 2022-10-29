import flask
import requests

geocodio_endpoint = 'https://api.geocod.io/v1.7/geocode'
geocodio_key = '88373683367ca97da3dc8736c365d6a6d55d33d'

yelp_endpoint = 'https://api.yelp.com/v3/businesses/search'
yelp_key = 'GrOGJIzzj2K3kYou2LtF38GqyaDYhTWG94RBnf3djDQlAtHHOCfnGLRDMqg4V0ItTaYjHLsurDJJQcNf8DpnVhOA5lEnlIalJovsL1q-VeJjEtaKjrh8uDZrkD9cY3Yx'

# 1. Starting a RESTful web service
# 6. Fault tolerance
app = flask.Flask(__name__)


@app.route("/restaurants", methods=['GET', 'POST'])
def restaurants():
    address = flask.request.args.get('address')
    if address is None:
        return flask.Response("[ERROR] No address received.", 400)

    # 3. Geocoding our address
    response = requests.get(geocodio_endpoint, params={'api_key': geocodio_key, 'q': address})
    if response.status_code != 200:
        return flask.Response(f"[ERROR] Geocodio endpoint request failed: {response.status_code}.", 500)
    location = response.json()['results'][0]['location']
    latitude, longitude = location['lat'], location['lng']

    # 4. Finding nearby restaurants
    response = requests.get(yelp_endpoint,
                            headers={'Authorization': f'bearer {yelp_key}'},
                            params={'longitude': longitude, 'latitude': latitude})
    if response.status_code != 200:
        return flask.Response(f"[ERROR] Yelp endpoint request failed: {response.status_code}.", 500)
    businesses = response.json()['businesses']

    # 5. Formatting client responses
    response = []
    for business in businesses:
        location = business['location']
        response.append({
            "name": business['name'],
            "address": ", ".join([location['address1'],
                                  location['city'],
                                  location['state'] + location['zip_code'],
                                  location['country']]),
            "rating": business['rating']
        })

    return flask.Response(response.__str__(), status=200, mimetype='application/json')


if __name__ == "__main__":
    app.run(debug=True)
