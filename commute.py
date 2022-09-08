import WazeRouteCalculator
import json
from flask import Flask


"""
Example format of a trips.json file:

[
    {
        "name": "via E Street",
        "region": "US",
        "legs": [
            {
                "from": "1600 Pennsylvania Avenue, Washington, DC",
                "to": "38.89605228888852, -77.04600646263067"
            },
            {
                "from": "38.89605228888852, -77.04600646263067",
                "to": "3700 O Street NW, Washington, DC"
            }
        ]
    },
    {
        "name": "via Constitution Ave",
        "region": "US",
        "legs": [
            {
                "from": "1600 Pennsylvania Avenue, Washington, DC",
                "to": "38.892148495805515, -77.04938525793273"
            },
            {
                "from": "38.892148495805515, -77.04938525793273",
                "to": "3700 O Street NW, Washington, DC"
            }
        ]
    }
]

"""


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/trips')
def trips():
    with open("trips.json") as f:
        trips = json.load(f)

    costs = ""

    for trip in trips:
        totalTime, totalDistance = processTrip(trip)
        tripName = trip['name']
        costs += f'trip cost of "{tripName}" is {totalTime} minutes and {totalDistance} miles<BR>'
    return costs


def km2miles( km ):
    return km * 0.621371


def processTrip( trip ):
    totalTime = totalDistance = 0.0
    region = trip['region']
    for leg in trip['legs']:
        fromAddress = leg['from']
        toAddress = leg['to']
        route = WazeRouteCalculator.WazeRouteCalculator(fromAddress, toAddress, region)
        routeTime, routeDistance = route.calc_route_info()
        # print( f'trip leg costs {routeTime} minutes and {routeDistance} miles')
        totalTime += routeTime
        totalDistance += routeDistance
    return totalTime, totalDistance


def main():

    app.run(host='127.0.0.1', port=8080, debug=True)

    with open("trips.json") as f:
        trips = json.load(f)

    for trip in trips:
        totalTime, totalDistance = processTrip(trip)
        tripName = trip['name']
        print( f'trip cost of "{tripName}" is {totalTime} minutes and {totalDistance} miles' )


if __name__ == "__main__":
    exit(main())
