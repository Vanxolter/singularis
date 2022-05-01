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

import requests

apiKey = input("API Key: ")
apiUrl = "https://aeroapi.flightaware.com/aeroapi/"

airport = 'KSFO'
payload = {'max_pages': 2}
auth_header = {'x-apikey':apiKey}

response = requests.get(apiUrl + f"airports/{airport}/flights",
    params=payload, headers=auth_header)

if response.status_code == 200:
    print(response.json())
else:
    print("Error executing request")
