import WazeRouteCalculator
import json


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

    with open("trips.json") as f:
        trips = json.load(f)

    for trip in trips:
        totalTime, totalDistance = processTrip(trip)
        tripName = trip['name']
        print( f'trip cost of "{tripName}" is {totalTime} minutes and {totalDistance} miles' )


if __name__ == "__main__":
    exit(main())
