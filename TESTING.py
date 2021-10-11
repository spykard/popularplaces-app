# Setup Tip: https://stackoverflow.com/a/64069120
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass, overpassQueryBuilder

# https://stackoverflow.com/q/52236655
nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/', userAgent='Popular Places', cacheDir='cache')  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/nominatim.md
data = nominatim.query("Patras", onlyCached=False, shallow=False, params={'limit': 10})  # Always loads from file if exists and there are also 2 additional parameters, 'onlyCachced' and 'shallow'
dataJSON = data.toJSON()

if not dataJSON:
        print("RETURN FROM THE FUNCTION")

# Areas: By convention the area id can be calculated from an existing OSM way by adding 2400000000 to its OSM id, or in case of a relation by adding 3600000000 respectively. 
# Note that area creation is subject to some extraction rules, i.e. not all ways/relations have an area counterpart (notably those that are tagged with
# area=no, and most multipolygons and that don’t have a defined name=* will not be part of areas).

# If 'Relation' (could also use 'Way' if needed) in top 3, select that result
final_selection = None
count = 0
for result in dataJSON:
        if count < 3 and result["importance"] >= 0.25:
                if result["osm_type"] == "relation":
                        final_selection = result
                        break

                # Debug
                # print(result["display_name"])
                # print(result["lat"], result["lon"])
                # print("osm_type:", result["osm_type"])
                # print("class:", result["class"])
                # print("type:", result["type"])
                # print("importance:", result["importance"])
                # print()
        else:
                break
        count += 1

if final_selection != None:
        osm_id = final_selection["osm_id"]
        area_id = osm_id + 3600000000
        lat = final_selection["lat"]
        lon = final_selection["lon"]

# Else Recurse Upwards using the Overpass API
else:
        # Recurse Up: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_up_.28.3C.29 or https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_.28n.2C_w.2C_r.2C_bn.2C_bw.2C_br.29
        recurseFirstQuery =     '''  
                                (node(%s);
                                <;
                                );
                                out center;
                                out body;
                                ''' % dataJSON[0]["osm_id"]

        overpass = Overpass(endpoint='http://overpass-api.de/api/', userAgent='Popular Places', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/overpass.md
        data = overpass.query(recurseFirstQuery, timeout=10, onlyCached=False, shallow=False)

        # Debug
        # print("Total number of Found Elements:", len(data.elements()))  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/element.md

        # admin_level information per Country: https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative#admin_level.3D.2A_Country_specific_values
        # we will utilize results in the range of 3-11, selecting the highest number

        if not data.elements():
                print("RETURN FROM THE FUNCTION")

        max_level = 2
        for result in data.elements():
                if 'admin_level' in result.tags():
                        current_level = int(result.tag('admin_level'))
                        current_type = result.type()
                        if current_level > max_level and current_type != 'node':
                                final_selection = result
                                max_level = current_level

                # Debug                
                # print(result.tags())
                # print(result.type())
                # print(result.id())
                # print(result.lat(), result.lon())
                # print(result.centerLat(), result.centerLon())
                # print()

        # Debug
        # print(final_selection.tags())
        # print(final_selection.type())
        # print(final_selection.id())
        # print(final_selection.lat(), final_selection.lon())
        # print(final_selection.centerLat(), final_selection.centerLon())
        # print()   

        osm_id = final_selection.id()
        if final_selection.type() == 'way':
            area_id = osm_id + 2400000000
        elif final_selection.type() == 'relation':
            area_id = osm_id + 3600000000 
        if final_selection.centerLat():
                lat = final_selection.centerLat()
                lon = final_selection.centerLon()
        elif final_selection.lat():   
                lat = final_selection.lat()
                lon = final_selection.lon()
        else:
                lat = dataJSON[0]["lat"]                       
                lon = dataJSON[0]["lon"]                       

print(osm_id)
print(area_id)
print(lat)

# Final Step
finalQuery =   '''  
                area(%s)->.searchArea;
                (
                node["amenity"="bar"](area.searchArea);
                );
                out body;
                ''' % area_id

data = overpass.query(finalQuery, timeout=10, onlyCached=False, shallow=False)

# Debug
print("Total number of Found Elements:", len(data.elements()))  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/element.md

for result in data.elements():
        # Debug                
        print(result.tags())
        print(result.type())
        print(result.id())
        print(result.lat(), result.lon())
        print(result.centerLat(), result.centerLon())
        print()

# -- NOTES --
# Patras bbox: (21.719416,38.238575,21.768314,38.278166)
# Overpass API example:

# 'area[name="Vienna"]->.searchArea;(node["tourism"="museum"](area.searchArea);way["tourism"="museum"](area.searchArea);relation["tourism"="museum"](area.searchArea););'

#   '''(
#   node["amenity"="parking"](21.719416,38.238575,21.768314,38.278166);
#   way["amenity"="parking"](21.719416,38.238575,21.768314,38.278166);
#   );'''

#   '''
#   area[name="London"][admin_level=6][boundary=administrative]->.londonarea;
#   rel(pivot.londonarea);
#   '''

#   ''' rel["name"="Noues de Sienne"](46.081,-5.438,50.121,0.439); '''  # This API Wrapper is unable to output certain types of resultsets such as rel/areas

#   ''' node["name"="Berlin"]; '''

#    '''
#    area(%s)->.searchArea;
#    (
#    node["amenity"="bar"](area.searchArea);
#    );
#    out body;
#    ''' % area_id
# --

# -- ALTERNATIVE NOMINATIM API - NOT THAT GOOD --
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