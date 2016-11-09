import googlemaps
gmaps = googlemaps.Client(key='AIzaSyAD5me0qtJi7VplTBRiqVjaIeE07ENXlk0')
geocode_result = gmaps.geocode('850 3rd Ave. New York, NY 10022')
print geocode_result
print geocode_result[0]['geometry']['location']['lat']
print geocode_result[0]['geometry']['location']['lng']


