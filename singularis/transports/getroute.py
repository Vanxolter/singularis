import requests
import polyline
from main.models import RouteCoordinates

import logging

logger = logging.getLogger(__name__)


def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
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
    loc = f"{pickup_lon},{pickup_lat};{air_lat_1},{air_long_1};{air_lat_2},{air_long_2};{dropoff_lon},{dropoff_lat}"
    logger.info(f"My URL - http://router.project-osrm.org/route/v1/driving/{loc}?overview=simplified")
    r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{loc}?overview=full") # overview: simplified упрощает линию маршрута, full - отображает высокоточный маршрут
    if r.status_code!= 200:
        return {}
    res = r.json()

    logger.info(f"My start_point - {res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]}")
    logger.info(f"My airport_1 - {res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]}")
    logger.info(f"My airport_2 - {res['waypoints'][2]['location'][1], res['waypoints'][2]['location'][0]}")
    logger.info(f"My end_point - {res['waypoints'][3]['location'][1], res['waypoints'][3]['location'][0]}")

    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    airport_1 = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    airport_2 = [res['waypoints'][2]['location'][1], res['waypoints'][2]['location'][0]]
    end_point = [res['waypoints'][3]['location'][1], res['waypoints'][3]['location'][0]]



    distance = res['routes'][0]['distance']
    logger.info(f"My distance - {res['routes'][0]['distance']}")

    out = {'route' :routes,
           'start_point' :start_point,
           'airport_1': airport_1,
           'airport_2': airport_2,
           'end_point' :end_point,
           'distance' :distance
           }

    return out