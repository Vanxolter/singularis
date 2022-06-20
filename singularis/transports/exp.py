import http.client

conn = http.client.HTTPSConnection("aerodatabox.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "9cef4caf6cmsh10e822fccf92ed4p142d32jsndf25b4bb0113",
    'X-RapidAPI-Host': "aerodatabox.p.rapidapi.com"
    }

conn.request("GET", "/flights/airports/icao/EHAM/2021-10-04T20:00/2021-10-05T08:00?withLeg=true&withCancelled=true&withCodeshared=true&withCargo=true&withPrivate=true&withLocation=false", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))