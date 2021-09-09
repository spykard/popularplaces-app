''' Query Google's PopularTimes in circles, given latitute and longtitude positions and retrieve data for places/stores '''
import configparser
import populartimes

# Config Parsing
config = configparser.ConfigParser()
config.read('config/config.ini')

api_key = config['Settings']['api_key']
mode = eval(config['Settings']['mode'])

if (mode == 1):
    # Get Data by ID
    place_id = config['Settings']['place_id']
    data = populartimes.get_id(api_key=api_key, place_id=place_id)
    data = [data]

elif (mode == 2):
    # Get Data by Circular Location
    types = config['Settings']['types'].split(",")
    p1 = eval(config['Settings']['p1'])
    p2 = eval(config['Settings']['p2'])
    radius = eval(config['Settings']['radius'])
    all_places = eval(config['Settings']['all_places'])

    data = populartimes.get(api_key=api_key, types=types, p1=p1, p2=p2, n_threads=20, radius=radius, all_places=all_places)


for place in data:
    print(place['name'])
    print(place['address'])
    print(place['types'])
    print(str(place['rating']) + " (" + str(place['rating_n']) + ")")
    if "current_popularity" in place:
        print(place['current_popularity'])
    else:
        print("N/A")
    print(place['populartimes'])
    if "time_spent" in place:
        print(place['time_spent'])
    else:
        print("N/A")
    print()
print(len(data))