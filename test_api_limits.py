from OSMPythonTools.overpass import Nominatim
from OSMPythonTools.overpass import Overpass
from concurrent import futures
import time
import random
import os


# -- Functions --
def delete_last_cache_item(original_path, cache_path):
    os.chdir(cache_path)
    files = sorted(os.listdir(cache_path), key=os.path.getctime)

    print("Last cache item was created at: " + time.ctime(os.path.getmtime(files[-1])) + ", and will be deleted")
    os.remove(os.path.join(os.getcwd(), files[-1]))
    os.chdir(original_path)

def run_query(location):
    nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/', userAgent=str(random.getrandbits(32)), cacheDir='cache', waitBetweenQueries=0)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/nominatim.md
    start = time.time()
    data = nominatim.query(location, onlyCached=False, shallow=False, params={'limit': 1})  # Always loads from file if exists and there are also 2 additional parameters, 'onlyCached' and 'shallow'
    print(data)
    end = time.time()
    print("Execution Time:", end-start)

    delete_last_cache_item(original_path, cache_path) 

# -- Initialize --
locations = ["Kalavrita", "Kriti", "Xalkida", "Livadia", "Andros", "Skopelos", "Trikala", "Tripoli", "Lamia", "Kastoria"]
#random_selection = random.choice(locations)
original_path = os.getcwd()
cache_path = os.path.join(os.getcwd(), 'cache')

# -- Main --
#nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/', userAgent='Testing', cacheDir='cache', waitBetweenQueries=0)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/nominatim.md
#overpass = Overpass(endpoint='http://overpass-api.de/api/', userAgent='Testing', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/overpass.md

with futures.ThreadPoolExecutor(max_workers=8) as executor:
    future_executor = {executor.submit(run_query, location): location for location in locations}
    for future in futures.as_completed(future_executor, timeout=None):
        try:
            print()
        except Exception as e:
            print("Error:", e) 

# start = time.time()
# for location in locations:
#     run_query(location)

# end = time.time()
# print("Execution Time:", end-start)

# Debug
# for result in dataJSON:
#     print(result["display_name"])
#     print(result["lat"], result["lon"])
#     print("osm_type:", result["osm_type"])
#     print("class:", result["class"])
#     print("type:", result["type"])
#     print("importance:", result["importance"])
#     print()
