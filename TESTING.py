# Setup Tip: https://stackoverflow.com/a/64069120
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

# https://stackoverflow.com/q/52236655
nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/', userAgent='Example App', cacheDir='cache')  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/nominatim.md
data = nominatim.query("Ioannina", params={'limit': 10})
dataJSON = data.toJSON()

# By convention the area id can be calculated from an existing OSM way by adding 2400000000 to its OSM id, or in case of a relation by adding 3600000000 respectively. 
# Note that area creation is subject to some extraction rules, i.e. not all ways/relations have an area counterpart (notably those that are tagged with
# area=no, and most multipolygons and that don’t have a defined name=* will not be part of areas).

for result in dataJSON:
        print(result["display_name"])
        print(result["lat"], result["lon"])
        print("osm_type:", result["osm_type"])
        print("class:", result["class"])
        print("type:", result["type"])
        print("importance:", result["importance"])
        print()


id = dataJSON[0]["osm_id"]
id2 = data.areaId()

print(id)
print(id2)

# Recurse Up: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_up_.28.3C.29 or https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_.28n.2C_w.2C_r.2C_bn.2C_bw.2C_br.29
recurseFirstQuery =     '''  
                        (node(%s);
                        <;
                        );

                        out body;
                        ''' % id

overpass = Overpass(endpoint='http://overpass-api.de/api/', userAgent='Example App', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/overpass.md
data = overpass.query(recurseFirstQuery, timeout=10)

print(len(data.elements()))  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/element.md

# admin_level information per Country: https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative#admin_level.3D.2A_Country_specific_values
# I WILL USE FROM 3 TO 11, looking for the highest number

for result in data.elements():
        print(result.tags())
        print(result.type())
        print(result.id())
        print()
quit()


#query = overpassQueryBuilder(elementType=['way', 'relation'], selector='"highway"="bus_stop"', out='body')  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/overpass.md

quit()
area_id = int(data[0].raw.get("osm_id")) + 3600000000
print(int(data[0].raw.get("osm_id")))






# Patras bbox: (21.719416,38.238575,21.768314,38.278166)

temp = 'area[name="Vienna"]->.searchArea;(node["tourism"="museum"](area.searchArea);way["tourism"="museum"](area.searchArea);relation["tourism"="museum"](area.searchArea););'

temp = '''(
    node["amenity"="parking"](21.719416,38.238575,21.768314,38.278166);
    way["amenity"="parking"](21.719416,38.238575,21.768314,38.278166);
        );'''

temp = '''
area[name="London"][admin_level=6][boundary=administrative]->.londonarea;
rel(pivot.londonarea);
        '''

temp2 = ''' rel["name"="Noues de Sienne"](46.081,-5.438,50.121,0.439); '''  # This API Wrapper is unable to output certain types of resultsets such as rel/areas

temp = ''' node["name"="Berlin"]; '''

# temp2 = """
#     area(%s)->.searchArea;
#     (
#       node["amenity"="bar"](area.searchArea);
#     );
#     out body;
#     """ % area_id

















# -- NOMINATIM API - NOT THAT GOOD --
# from geopy.geocoders import Nominatim
# geolocator = Nominatim(timeout=10, domain='nominatim.openstreetmap.org', user_agent="testing-right-now")
# data = geolocator.geocode("Patras", limit=10, exactly_one=False) 

# for location in data:
#         print(location.address)
#         print(location.latitude, location.longitude)
#         print("osm:", location.raw.get("osm_type"))
#         print("class:", location.raw.get("class"))
#         print("type:", location.raw.get("type"))
#         print("importance:", location.raw.get("importance"))
#         print(location.raw)
#         print()
# --

# -- OVERPASS API #2 - SEMI-BROKEN --
# import overpass
# api = overpass.API(endpoint='https://overpass.openstreetmap.ru/api/interpreter', timeout=25)

# response = api.get(temp, verbosity='body')
# store = response["features"]

# print(len(store))
# for result in store:
#         print(result["id"])
#         print(result["geometry"])        
#         print(result["properties"])
#         print()
# --