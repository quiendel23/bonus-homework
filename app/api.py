import requests
from os import environ


headers = {
	"X-RapidAPI-Key": environ["RAPID_API_KEY"],
	"X-RapidAPI-Host": environ["RAPID_API_HOST"],
}
def list_cities(min_population, max_population):
    url = "https://wtf-geo-db.p.rapidapi.com/v1/geo/cities"
    querystring = {"minPopulation":str(min_population),"maxPopulation":str(max_population)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

def locate_nearby_cities(city_name, radius):
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities/"+city_name+"/nearbyCities"
    querystring = {"radius":str(radius)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()

if __name__ == "__main__":
	import time
	print(list_cities(100, 10000))
	time.sleep(1)
	print(locate_nearby_cities("Q60", 10))
