from OSMPythonTools.overpass import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder
import time
import random

location = ["Patras", "Ioannina", "Corfu"]
selection = random.choice(location)	

nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/', userAgent='Testing', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/nominatim.md
overpass = Overpass(endpoint='http://overpass-api.de/api/', userAgent='Testing', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/overpass.md

for i in range(0,10):
    start = time.time()
    
    data = nominatim.query(selection, onlyCached=False, shallow=False, params={'limit': 10}, wkt=True)  # Always loads from file if exists and there are also 2 additional parameters, 'onlyCachced' and 'shallow'
    dataJSON = data.toJSON()

    end = time.time()

    # for result in dataJSON:
    #     print(result["display_name"])
    #     print(result["lat"], result["lon"])
    #     print("osm_type:", result["osm_type"])
    #     print("class:", result["class"])
    #     print("type:", result["type"])
    #     print("importance:", result["importance"])
    #     print()

    print("Execution Time: ", end-start)