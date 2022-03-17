# Importing the Nominatim geocoder class
from geopy.geocoders import Nominatim

# address we need to geocode
loc = 'Minsk'

# making an instance of Nominatim class
geolocator = Nominatim(user_agent="my_request")

# applying geocode method to get the location
location = geolocator.geocode(loc)

# printing address and coordinates
print(location.address)
print((location.latitude, location.longitude))