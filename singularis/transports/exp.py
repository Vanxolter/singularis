'''# Importing the Nominatim geocoder class
from geopy.geocoders import Nominatim

# address we need to geocode
loc = [53.9024716, 27.5618225]

# making an instance of Nominatim class
geolocator = Nominatim(user_agent="my_request")

# applying geocode method to get the location
location = geolocator.reverse(loc)

# printing address and coordinates
print(location.address)
print((location.latitude, location.longitude))'''

import my_keys
from my_keys import *
from amadeus import Client, ResponseError
from amadeus import Location

amadeus = Client(
    client_id=my_keys.AMADEUS_KEY,
    client_secret=my_keys.AMADEUS_SECRET_KEY
)

try:
    '''
    What's the airline name for the IATA code BA?
    '''
    response = amadeus.shopping.flight_offers_search.get(
    originLocationCode='MAD',
    destinationLocationCode='BOS',
    departureDate='2019-11-01',
    adults='1'
)
    print(response.data)
except ResponseError as error:
    raise error
