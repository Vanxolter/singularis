import requests
import polyline
from main.models import RouteCoordinates

import logging

logger = logging.getLogger(__name__)


def get_route_walk(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = f"{pickup_lon},{pickup_lat};{dropoff_lon},{dropoff_lat}"
    r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{loc}?overview=full")
    if r.status_code!= 200:
        return {}
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']

    out = {'route' :routes,
           'start_point' :start_point,
           'end_point' :end_point,
           'distance' :distance
           }

    return out


def get_route_car(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = f"{pickup_lon},{pickup_lat};{dropoff_lon},{dropoff_lat}"
    r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{loc}?overview=full")
    if r.status_code!= 200:
        return {}
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']

    out = {'route' :routes,
           'start_point' :start_point,
           'end_point' :end_point,
           'distance' :distance
           }

    return out


def get_route_fly(pickup_lon, pickup_lat, air_lat_1, air_long_1, air_lat_2, air_long_2, dropoff_lon, dropoff_lat):
    loc = [f'{pickup_lon},{pickup_lat};{air_lat_1},{air_long_1}', f'{air_lat_2},{air_long_2};{dropoff_lon},{dropoff_lat}']
    my_coord = []
    for i in loc:
        logger.info(f"My URL - http://router.project-osrm.org/route/v1/driving/{i}?overview=simplified&steps=true")
        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{i}?overview=full&steps=true") # overview: simplified упрощает линию маршрута, full - отображает высокоточный маршрут
        if r.status_code!= 200:
            return {}
        res = r.json()
        routes = polyline.decode(res['routes'][0]['geometry'])
        start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
        end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
        distance = res['routes'][0]['distance']
        steps = res['routes'][0]['legs'][0]['steps']

        logger.info(f"My distance!!!!!!!!!!!!!!1 - {steps}")

        my_coord.extend([routes, start_point, end_point, distance, steps])

    '''logger.info(f"My coord!!!!!!!!!!!!!!1 - {my_coord}")'''
    out = {'route1' :my_coord[0],
           'start_point1' :my_coord[1],
           'end_point1' :my_coord[2],
           'distance1':my_coord[3],
           'steps1': my_coord[4],
           'route3': my_coord[5],
           'start_point3': my_coord[6],
           'end_point3': my_coord[7],
           'distance3': my_coord[8],
           'steps3': my_coord[9],
           }

    return out