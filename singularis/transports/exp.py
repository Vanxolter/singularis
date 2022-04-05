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

from django.contrib.gis.db.models.functions import Distance



pnt = AustraliaCity.objects.get(name='Hobart').point
for city in AustraliaCity.objects.annotate(distance=Distance('point', pnt)):
    print(city.name, city.distance)