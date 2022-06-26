import requests

url = "https://countriesnow.space/api/v0.1/countries/capital"

payload = {"country":"nigeria"}
headers = {}

response = requests.request("POST", url, headers=headers, data=payload)
res =response.json()
cap = [res['data']['capital']]
print(cap)