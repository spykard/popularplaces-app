# -*- encoding: utf-8 -*-
from app.home import blueprint
from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import login_required, current_user
from app import db, login_manager
from sqlalchemy import func, nullslast
from jinja2 import TemplateNotFound
from app.base.forms import EditProfileForm, EditSettingsForm, EditSettingsTurboForm, EditSettingsAdvancedForm, AddPlaceForm
from app.base.models import User, Place, Search, City, PlaceResult, PlaceGlobal, CrowdInput
from app.base.util import hash_pass
from OSMPythonTools.nominatim import Nominatim
from OSMPythonTools.overpass import Overpass
from datetime import datetime, timedelta
from random import randint
import populartimes
import json
import concurrent

@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:
        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )
    except TemplateNotFound:
        return render_template('errors/page-404.html'), 404
    
    except:
        return render_template('errors/page-500.html'), 500

@blueprint.route('/search-turbo', methods=['GET', 'POST'])
@login_required
def search_turbo():
    settings_form = EditSettingsTurboForm(request.form)
    if 'search' in request.form:
        # Read form data
        location = request.form['location'].title()
        type1 = request.form['type'].title()

        if request.form.get('save_places') == None:  # If checkboxed not checked, no POST data are sent
            save_places = False
        else:
            save_places = True

        # Validate Form Data
        if not settings_form.validate():
            return render_template( 'search-turbo.html', 
                                    segment='search-turbo',
                                    to_notify='true',
                                    msg='Input does not follow the Appropriate Form',
                                    error_dict=settings_form.errors,
                                    success=False,
                                    form=settings_form)

        # Write to DB
        current_user.settings_type1 = type1
        current_user.settings_save_places = save_places
        current_user.total_runs += 1
        if current_user.premium_enabled == False: current_user.free_runs_remaining -= 1
        db.session.commit()       

        # MAIN
        places, search = get_places_to_search_geocode(location, type1, save_places)  # Convert type to snake_case String

        if search:
            # Write Place Object to DB
            city_to = City.query.filter_by(name=location).first()
            if not city_to:
                insert_dict = dict([("name" , location)])
                city_to = City(**insert_dict)
                db.session.add(city_to)
                db.session.commit()     

            for place in places:
                placeglobal_to = db.session.query(PlaceGlobal).filter((PlaceGlobal.name == place[1]) & (PlaceGlobal.city_id == city_to.id)).first()
                if not placeglobal_to:
                    insert_dict = dict([("name" , place[1]), ("address" , place[2]), ("city_id" , city_to.id)])
                    placeglobal_to = PlaceGlobal(**insert_dict)
                    db.session.add(placeglobal_to)
                    db.session.commit()
                place[3] = placeglobal_to.id

                if save_places == True:
                    place_to = db.session.query(Place).filter((Place.name == place[1]) & (Place.city_id == city_to.id)).first()
                    if not place_to:                
                        insert_dict = dict([("name" , place[1]), ("address" , place[2]), ("type_p" , type1), ("user_id" , current_user.id), ("city_id" , city_to.id), ("global_id" , placeglobal_to.id)])
                        place_to = Place(**insert_dict)
                        db.session.add(place_to)
                        db.session.commit()  
                    place[0] = place_to.id
                else:
                    place[0] = 0  # Place ID is completely in this case      

            search_success, search_msg = search_populartimes(places, search["search"], search["current_time"], search["user_id"], search["name"])

            if search_success:
                message = json.dumps({"message": search_msg})    

                return redirect(url_for('home_blueprint.history', messages=search_msg))

            else:
                return render_template( 'search-turbo.html', 
                                segment='search-turbo',
                                msg='Search executed but returned the following Error: ' + search_msg, 
                                error_dict={},
                                success=False,
                                form=settings_form)   
        else:
            return render_template( 'search-turbo.html', 
                            segment='search-turbo',
                            msg='No Location with given name Found', 
                            error_dict={},
                            success=False,
                            form=settings_form)                                                  

    return render_template( 'search-turbo.html', 
                            segment='search-turbo',
                            error_dict={},
                            form=settings_form,
                            to_notify_premium=notify_premium())

@blueprint.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    settings_form = EditSettingsForm(request.form)
    if 'search' in request.form:
        # Read form data
        city = request.form['city'].title()
        type1 = request.form['type1']
        type2 = request.form['type2']
        if request.form.get('all_places') == None:  # If checkboxed not checked, no POST data are sent
            all_places = 0
        else:
            all_places = 1

        # Validate Form Data
        if not settings_form.validate():
            return render_template( 'search.html', 
                                    segment='search',
                                    to_notify='true',
                                    msg='Input does not follow the Appropriate Form',
                                    error_dict=settings_form.errors,
                                    success=False,
                                    form=settings_form,
                                    city=city,
                                    show_search_panel=True)

        # Write to DB
        current_user.settings_type1 = type1
        current_user.settings_type2 = type2
        current_user.settings_all_places = all_places
        current_user.total_runs += 1
        if current_user.premium_enabled == False: current_user.free_runs_remaining -= 1
        db.session.commit()  

        # Write Search Object to DB
        current_time = datetime.utcnow() + timedelta(hours=3)  # For some weird reason the Original form of the PopularTimes library seems to be UTC+3
        user_id = ("user_id", current_user.id)
        if type2 == "Choose...": type2 = ""
        name = ("name", current_time.strftime("%Y%m%d-%H%M%S.%f") + "-" + str(user_id[1]))
        insert_dict = dict([("city" , city), ("settings_type1" , type1), ("settings_type2" , type2), ("settings_all_places" , all_places), user_id, name, ("type" , 1)])
        search = Search(**insert_dict)
        db.session.add(search)
        db.session.commit()         

        # MAIN
        places = get_places_to_search(city, type1, type2, all_places)

        search_success, search_msg = search_populartimes(places, search, current_time, user_id, name)

        if search_success:
            message = json.dumps({"message": search_msg})    

            return redirect(url_for('home_blueprint.history', messages=search_msg))

        else:
            return render_template( 'search.html', 
                            segment='search',
                            msg='Search executed but returned the following Error: ' + search_msg, 
                            error_dict={},
                            success=False,
                            form=settings_form,
                            city=city,
                            show_search_panel=True)                                        

    # Load Cities
    cities = db.session.query(City).join(Place).filter((Place.user_id == current_user.id) | (Place.global_place == 1)).order_by(City.id.asc()).all() 
    cities_dicts = []
    
    for city in cities:    
        cities_count = db.session.query(func.count(Place.city_id)).join(City).filter(((Place.user_id == current_user.id) | (Place.global_place == 1)) & (City.name == city.name)).first()   
        cities_dicts.append({'name': city.name, 'description': city.description, 'image_link': city.image_link, 'count': cities_count[0]})

    return render_template( 'search.html', 
                            segment='search',
                            error_dict={},
                            form=settings_form,
                            to_notify_premium=notify_premium(),
                            cities=cities_dicts)

@blueprint.route('/search-advanced', methods=['GET', 'POST'])
@login_required
def search_advanced():
    settings_form = EditSettingsAdvancedForm(request.form)
    if 'search' in request.form:
        # Read form data
        api_key = request.form['api_key']
        p1 = request.form['p1']
        p2 = request.form['p2']
        radius = request.form['radius']
        type1 = request.form['type1']
        type2 = request.form['type2']
        if request.form.get('all_places') == None:  # If checkboxed not checked, no POST data are sent
            all_places = 0
        else:
            all_places = 1

        # Validate Form Data
        if not settings_form.validate():
            return render_template( 'search-advanced.html', 
                                    segment='search',
                                    to_notify='true',
                                    msg='Input does not follow the Appropriate Form',
                                    error_dict=settings_form.errors,
                                    success=False,
                                    form=settings_form)

        # Write to DB
        current_user.google_api_key = api_key
        current_user.settings_p1 = p1
        current_user.settings_p2 = p2
        current_user.settings_radius = radius
        current_user.settings_type1 = type1
        current_user.settings_type2 = type2
        current_user.settings_all_places = all_places
        if current_user.premium_enabled == False: current_user.free_runs_remaining = current_user.free_runs_remaining-1
        db.session.commit()            

        # Main
        search_success, search_msg = search_populartimes_advanced(api_key, p1, p2, radius, type1, type2, all_places)

        if search_success:
            return render_template( 'history.html', 
                            segment='history',
                            msg='Search executed successfully! - ID: ' + search_msg, 
                            error_dict={},
                            success=True)
        else:
            return render_template( 'search-advanced.html', 
                            segment='search',
                            msg='Search executed but returned the following Error: ' + search_msg, 
                            error_dict={},
                            success=False,
                            form=settings_form)                                        

    return render_template( 'search-advanced.html', 
                            segment='search',
                            error_dict={},
                            form=settings_form,
                            to_notify_premium=notify_premium())    

@blueprint.route('/history', methods=['GET', 'POST'])
@login_required
def history():
    # Get message parameters
    message = None
    if 'messages' in request.args:
        message = request.args['messages']

    # Get search history data
    searches = Search.query.filter_by(user_id=current_user.id).order_by(Search.name.desc()).all()
    searches_dicts = []
    
    for search in searches:     
        searches_dicts.append({'id': search.id, 'name': search.name[0:15], 'city': search.city, 'settings_type1': search.settings_type1, 'settings_type2': search.settings_type2, 'day': search.time.strftime("%A - %H Hour"), 'time': search.time})

    if message:
        return render_template( 'history.html', 
                                segment='history',
                                msg='Search executed successfully! - ID: ' + message, 
                                error_dict={},
                                success=True,                            
                                searches=searches_dicts)
    else:
        return render_template( 'history.html', 
                                segment='history',                      
                                searches=searches_dicts)        

@blueprint.route('/places', methods=['GET', 'POST'])
@login_required
def places():
    # Get message parameters
    parameter = None
    if 'add' in request.args:
        parameter = request.args['add']

    # Load Cities
    places = db.session.query(Place, City).join(City).filter((Place.user_id == current_user.id) | (Place.global_place == 1)).order_by(Place.id.asc()).all() 
    place_dicts = []
    count = 1
    for place in places:
        types = place[0].type_p
        # if place[0].type_p2: types += ", " + place[0].type_p2
        # if place[0].type_p3: types += ", " + place[0].type_p3
        place_dicts.append({'id': place[0].id, 'count': count, 'name': place[0].name, 'address': place[0].address, 'type': types,  'city': place[1].name, 'verification': place[0].verification, 'time': place[0].time.strftime("%Y-%m-%d")})
        count += 1

    add_place_form = AddPlaceForm(request.form)
    if 'name' in request.form:  # In this scenario we have not set a submit button, thus we check one of the input boxes' id

        # Read form data
        name = request.form['name']
        address = request.form['address']
        type_p = request.form['type_p']

        city = request.form['city'].title()
        typo_errors_fixlist1 = ("Patr", "Πατρ", "Πάτρ")
        typo_errors_fixlist2 = ("Athe", "Αθην", "Αθήν")
        typo_errors_fixlist3 = ("Κερκυ", "Κέρκυ")

        if city.startswith(typo_errors_fixlist1):
            city = "Patras"
        elif city.startswith(typo_errors_fixlist2):
            city = "Athens"
        elif city.startswith(typo_errors_fixlist3):
            city = "Corfu"

        type_p2 = None if request.form['type_p2'] == "Choose..." else request.form['type_p2']
        type_p3 = None if request.form['type_p3'] == "Choose..." else request.form['type_p3']      

        # Validate Form Data
        if not add_place_form.validate():
            return render_template( 'places.html', 
                                    segment='places',
                                    error_dict={},
                                    to_notify='true',
                                    success=False,
                                    form=add_place_form,
                                    places=place_dicts)

        # Write Place Object to DB
        city_to = City.query.filter_by(name=city).first()
        if not city_to:
            insert_dict = dict([("name" , city)])
            city_to = City(**insert_dict)
            db.session.add(city_to)
            db.session.commit()     

        placeglobal_to = db.session.query(PlaceGlobal).filter((PlaceGlobal.name == name) & (PlaceGlobal.city_id == city_to.id)).first()
        if not placeglobal_to:
            insert_dict = dict([("name" , name), ("address" , address), ("city_id" , city_to.id)])
            placeglobal_to = PlaceGlobal(**insert_dict)
            db.session.add(placeglobal_to)
            db.session.commit()                  

        insert_dict = dict([("name" , name), ("address" , address), ("type_p" , type_p), ("user_id" , current_user.id), ("city_id" , city_to.id), ("global_id" , placeglobal_to.id), ("type_p2", type_p2), ("type_p3", type_p3)])
        place_to = Place(**insert_dict)
        db.session.add(place_to)
        db.session.commit()

        # Load Cities
        places = db.session.query(Place, City).join(City).filter((Place.user_id == current_user.id) | (Place.global_place == 1)).order_by(Place.id.asc()).all() 
        place_dicts = []
        count = 1
        for place in places:
            types = place[0].type_p
            # if place[0].type_p2: types += ", " + place[0].type_p2
            # if place[0].type_p3: types += ", " + place[0].type_p3            
            place_dicts.append({'id': place[0].id, 'count': count, 'name': place[0].name, 'address': place[0].address, 'type': types,  'city': place[1].name, 'verification': place[0].verification, 'time': place[0].time.strftime("%Y-%m-%d")})
            count += 1

        return render_template( 'places.html', 
                        segment='places', 
                        error_dict={},
                        success=True,
                        form=add_place_form,
                        places=place_dicts)                                      

    return render_template( 'places.html', 
                            segment='places',
                            error_dict={},
                            parameter=parameter,
                            form=add_place_form,
                            places=place_dicts)

@blueprint.route('/page-user', methods=['GET', 'POST'])
@login_required
def page_user():
    profile_form = EditProfileForm(request.form)    
    if 'save' in request.form:

        # Read form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        city = request.form['city']
        country = request.form['country']
        zipcode = request.form['zipcode']
        about_me = request.form['about_me']

        # Validate Form Data
        if not profile_form.validate():
            return render_template( 'page-user.html', 
                                     segment='page-user',
                                     msg='Input does not follow the Appropriate Form',
                                     success=False,
                                     form=profile_form)

        # Check usename exists
        user = User.query.filter_by(username=username).first()
        if current_user.username != username and user:
            return render_template( 'page-user.html',
                                    segment='page-user',
                                    msg='Username already registered',
                                    success=False,
                                    form=profile_form)

        # Check email exists
        user = User.query.filter_by(email=email).first()
        if current_user.email != email and user:
            return render_template( 'page-user.html', 
                                    segment='page-user',
                                    msg='Email already registered', 
                                    success=False,
                                    form=profile_form)

        # Write to DB
        current_user.username = username
        if password:
            current_user.password = hash_pass( password ) # we need bytes here (not plain str)
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.address = address
        current_user.city = city
        current_user.country = country
        current_user.zipcode = zipcode
        current_user.about_me = about_me
        db.session.commit()

        return render_template( 'page-user.html', 
                        segment='page-user',
                        msg='Changes saved successfully!', 
                        success=True,
                        form=profile_form)

    return render_template( 'page-user.html', 
                            segment='page-user',
                            form=profile_form)

@blueprint.route('/get-place-results', methods=['POST'])
@login_required
def get_place_results():
    id = int(request.form['id'])
    place_results = db.session.query(PlaceResult, Search).join(Search).filter(Search.id == id).order_by(nullslast(PlaceResult.live_popularity.desc()), nullslast(PlaceResult.usual_popularity.desc())).all() 

    data = []
    #converter = lambda i : i or ''  # Convert None to empty string
    for place_result in place_results:
        popular_times = place_result[0].popular_times
        decoded = ""
        if popular_times != "null":
            load_data = json.loads(popular_times)
            for day in load_data:
                decoded += ' '.join([str(int) for int in day["data"]])
                decoded += (',')

        # Extra Global Data
        place_result_global = PlaceGlobal.query.filter_by(id=place_result[0].global_id).first()

        data.append({'name': place_result[0].name, 'address': place_result[0].address, 'global_id': place_result[0].global_id, 'rating': str(converter(place_result[0].rating)) + " (" + str(converter(place_result[0].rating_num)) + ")", 'popular_times': decoded,  'time_spent': converter(place_result[0].time_spent), 'usual_popularity': converter(place_result[0].usual_popularity), 'difference': converter(place_result[0].difference), 'live_popularity': converter(place_result[0].live_popularity), 'time': str(place_result[1].time), 'latitude': converter(place_result_global.latitude), 'longtitude': converter(place_result_global.longtitude)})        

    return jsonify(data)

@blueprint.route('/get-place-info', methods=['POST'])
@login_required
def get_place_info():
    search_name = request.form['name']
    search_city = request.form['city']
    place = populartimes.get_popular_times_by_crawl(name=search_name, address=search_city)
    if not place["place_address"]: abort(400)

    types = []
    for type_p in place["types"]:
        types.append(type_mapper(type_p[0], 2))

    data = []
    data.append({'name': place["place_name"], 'address': place["place_address"], 'types': types})

    return jsonify(data)    

@blueprint.route('/set-person-count', methods=['POST'])
@login_required
def set_person_count():
    id = request.form['id']
    input = request.form['input']

    insert_dict = dict([("user_id" , current_user.id), ("global_id" , id), ("input" , input)])
    search = CrowdInput(**insert_dict)
    db.session.add(search)
    db.session.commit()     

    return "true" 

@blueprint.route('/get-person-count', methods=['POST'])
@login_required
def get_person_count():
    id = request.form['id']

    if (int(id) != 0):
        crowd_input = db.session.query(func.avg(CrowdInput.input).label('average')).filter(CrowdInput.global_id == id).first()

        data = []
        for place in crowd_input:
            if (place):
                data.append({'count': place})
            else:
                data.append({'count': -1})

        return jsonify(data)            
    else:
        return jsonify([{'count': randint(13, 34)}])     

@blueprint.route('/get-search-map', methods=['POST'])
@login_required
def get_search_map():
    if current_user.is_authenticated:
        attempt_to_find_search_instance = db.session.query(Search).filter((Search.user_id == current_user.id) & (Search.time >= datetime.utcnow() - timedelta(seconds=1.5))).order_by(Search.time.desc()).first() 

        if attempt_to_find_search_instance:
            return jsonify([{'city': attempt_to_find_search_instance.city, 'search_lat': attempt_to_find_search_instance.settings_lat, 'search_lon': attempt_to_find_search_instance.settings_lon, 'search_wkt': attempt_to_find_search_instance.settings_wkt}]) 
        else:
            return "false"
    else:
        return "false" 

@blueprint.route('/delete-search', methods=['POST'])
@login_required
def delete_search():
    id = int(request.form['id'])
    if id == 0: abort(400)

    if current_user.is_authenticated:
        is_not_empty = db.session.query(Search).join(PlaceResult).filter(Search.id == id).first() 

        if is_not_empty:
            Search.query.filter_by(id=id).update({"user_id": None})          
        else:
            Search.query.filter_by(id=id).delete()

        db.session.commit() 
        return "true"
    else:
        return "false"  

@blueprint.route('/delete-place', methods=['POST'])
@login_required
def delete_place():
    id = int(request.form['id'])
    if current_user.is_authenticated:
        places = db.session.query(Place).filter((Place.id == id) & (Place.global_place == 1)).all()
        if len(places) > 0: abort(400)

        Place.query.filter_by(id=id).delete()          
        db.session.commit() 
        return "true"
    else:
        return "false"    


# --//----//----//----//----//----//----//----//--

@login_required
# Helper - Run the populartimes Implementation using mode #2
def search_populartimes(places, search, current_time, user_id, name):
    ''' Query Google's PopularTimes, using a crawler that takes name and address of a specific place as input '''
    # Perform the main Search in a Threaded fashion
    def main_search_threaded(place):
        # Debug
        # search_name = "Avli By Vouz"
        # search_address = "Pantanassis 17-29"
        # search_name = "Kynorodo"
        # search_address = "Korinthou 167, Patra 262 23"    
        search_name = place[1]
        search_address = place[2]
        output_dict = populartimes.get_popular_times_by_crawl(name=search_name, address=search_address)
        output_dict["id"] = place[0]
        output_dict["search_name"] = search_name
        output_dict["search_address"] = search_address
        output_dict["global_id"] = place[3]

        return output_dict            

    place_data = []

    # https://stackoverflow.com/a/61360215
    # https://stackoverflow.com/a/30495317
    # https://docs.python.org/3/library/concurrent.futures.html#threadpoolexecutor-example
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        future_to_url = {executor.submit(main_search_threaded, place): place for place in places}
        for future in concurrent.futures.as_completed(future_to_url, timeout=None):
            try:
                place_data.append(future.result())
            except Exception as e:
                return False, str(e)             

    for data in place_data:
        # Write Verification for Places to DB
        if data["place_address"]:
            if data["types"]:
                data["types"] = [item for sublist in data["types"] for item in sublist]  # https://stackoverflow.com/a/952952
            Place.query.filter_by(id=data["id"]).update({"verification": "True"})
            PlaceGlobal.query.filter_by(id=data["global_id"]).update({"name_verified": data["place_name"], "address_verified": data["place_address"], "latitude": float(data["latitude"]), "longtitude": float(data["longtitude"]), "type_verified": data["types"], "place_id": data["place_id"]})

            if data["populartimes"]:
                usual_popularity = ("usual_popularity", data["populartimes"][current_time.weekday()]["data"][current_time.hour])

                if data["current_popularity"]:
                    difference = ("difference", data["current_popularity"] - usual_popularity[1])
                else:
                    difference = ("difference", None)

                if data["time_spent"]:
                    time_spent = ("time_spent", '-'.join(map(str, data["time_spent"])))   
                else:
                    time_spent = ("time_spent", None)

            else:
                usual_popularity = ("usual_popularity", None)
                difference = ("difference", None)
                time_spent = ("time_spent", None)

        else:
            Place.query.filter_by(id=data["id"]).update({"verification": "False"}) 
            usual_popularity = ("usual_popularity", None)
            difference = ("difference", None)
            time_spent = ("time_spent", None)

        # db.session.commit() 

        # if "time_wait" not in data:
        #     data["time_wait"] = None

        # Write Data to DB
        insert_dict = dict([("rating" , data["rating"]), ("rating_num" , data["rating_n"]), ("popular_times" , json.dumps(data["populartimes"])), time_spent, user_id, ("search_id", search.id), ("name" , data["search_name"]), ("address" , data["search_address"]), ("live_popularity" , data["current_popularity"]), difference, ("global_id", data["global_id"]), usual_popularity])
        placeresult = PlaceResult(**insert_dict)
        db.session.add(placeresult)
        db.session.commit()

    return True, name[1]

@login_required
# Helper - Run the populartimes Implementation using mode #2
def search_populartimes_advanced(api_key, p1, p2, radius, type1, type2, all_places):
    ''' Query Google's PopularTimes in circles, given latitute and longtitude positions and retrieve data for places/stores '''

    p1_conv = eval("(" + p1 + ")")
    p2_conv = eval("(" + p2 + ")")
    radius_conv = int(radius)
    types_conv = type_mapper(type1, type2)  # In general, only one type may be specified (if more than one type is provided, all types following the first entry are ignored)
    all_places_conv = bool(all_places)

    for place_type in types_conv:
        # TODO
        print()

    # Write Search Object to DB
    user_id = ("user_id", current_user.id)
    name = ("name", datetime.now().strftime("%Y%m%d-%H%M%S.%f") + "-" + str(user_id[1]))
    if len(types_conv) < 2: type2 = ""
    insert_dict = dict([("google_api_key" , api_key), ("settings_p1" , p1), ("settings_p2" , p2), ("settings_radius" , radius), ("settings_type1" , type1), ("settings_type2" , type2), ("settings_all_places" , all_places), user_id, name, ("type" , 2)])
    search = Search(**insert_dict)
    db.session.add(search)
    db.session.commit()    

    return True, name[1]

@login_required
# Helper - Convert None to empty string
def converter(s):
    return '' if s is None else s

# Helper - Check whether user must be notified for Premium subscription Enabling
def notify_premium():
    if current_user.premium_enabled == True and current_user.premium_notified == False:
        to_notify = "true"
        current_user.premium_notified = True
        db.session.commit()        
    else:
        to_notify = "false"
    
    return to_notify

# Helper - Get the details of all the places that match the given Search Settings
def get_places_to_search(city, type1, type2, all_places):
    city_id = City.query.filter_by(name=city).first()
    if type2 != "Choose...":
        if all_places == 0:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & ((Place.type_p == type1) | (Place.type_p == type2)) & (Place.verification != "False")).order_by(Place.id.asc()).all()
        else:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & ((Place.type_p == type1) | (Place.type_p == type2))).order_by(Place.id.asc()).all()
    else:
        if all_places == 0:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & (Place.type_p == type1) & (Place.verification != "False")).order_by(Place.id.asc()).all()
        else:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & (Place.type_p == type1)).order_by(Place.id.asc()).all()            

    places_list = []
    for place in places:
        places_list.append((place.id, place.name, place.address, place.global_id))
    
    return places_list

# Helper - Geocode given the users Location and Type input and returns the details of all the matched places
def get_places_to_search_geocode(location, type1, save_places):
    ''' Perform the main Search in a Threaded fashion '''
    # Write Search Object to DB
    def write_search_object_to_DB(search_list, type1, save_places):        
        current_time = datetime.utcnow() + timedelta(hours=3)  # For some weird reason the Original form of the PopularTimes library seems to be UTC+3
        user_id = ("user_id", current_user.id)
        name = ("name", current_time.strftime("%Y%m%d-%H%M%S.%f") + "-" + str(user_id[1]))
        insert_dict = dict([("city" , location), ("settings_type1" , type1), ("settings_type2" , ""), ("settings_save_places" , save_places), user_id, name, ("type" , 3), ("settings_osm_id" , search_list[0]), ("settings_area_id" , search_list[1]), ("settings_lat" , search_list[2]), ("settings_lon" , search_list[3]), ("settings_wkt" , search_list[4])])
        search = Search(**insert_dict)
        db.session.add(search)
        db.session.commit()

        return {"current_time": current_time, "user_id": user_id, "name": name, "search": search}

    # https://stackoverflow.com/q/52236655
    nominatim = Nominatim(endpoint='https://nominatim.openstreetmap.org/', userAgent='Popular Places', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/nominatim.md
    overpass = Overpass(endpoint='http://overpass-api.de/api/', userAgent='Popular Places', cacheDir='cache', waitBetweenQueries=1)  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/overpass.md

    data = nominatim.query(location, onlyCached=False, shallow=False, params={'limit': 10}, wkt=True)  # Always loads from file if exists and there are also 2 additional parameters, 'onlyCachced' and 'shallow'
    dataJSON = data.toJSON()

    type_snake_case = "_".join(type1.lower().split())
    places_list = {}
    search_list = (0, 0, "", "", "")

    if not dataJSON:
        search_dict = write_search_object_to_DB(search_list, type1.title(), save_places)
        return places_list, None

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
            geotext = final_selection["geotext"]
            search_list = (osm_id, area_id, lat, lon, geotext)

    # Else Recurse Upwards using the Overpass API
    else:
        # Recurse Up: https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_up_.28.3C.29 or https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL#Recurse_.28n.2C_w.2C_r.2C_bn.2C_bw.2C_br.29
        recurseFirstQuery =     '''  
                                (node(%s);
                                <;
                                );
                                out body;
                                ''' % dataJSON[0]["osm_id"]
                                # out center;

        data = overpass.query(recurseFirstQuery, timeout=10, onlyCached=False, shallow=False)

        # Debug
        # print("Total number of Found Elements:", len(data.elements()))  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/element.md

        # admin_level information per Country: https://wiki.openstreetmap.org/wiki/Tag:boundary%3Dadministrative#admin_level.3D.2A_Country_specific_values
        # we will utilize results in the range of 3-11, selecting the highest number

        if not data.elements():
            search_dict = write_search_object_to_DB(search_list, type1.title(), save_places)            
            return places_list, None

        max_level = 2
        for result in data.elements():
            if 'admin_level' in result.tags():
                current_level = int(result.tag('admin_level'))
                current_type = result.type()
                if current_level > max_level and current_type != 'node':
                    final_selection = result
                    max_level = current_level

        # Debug
        # print(final_selection.tags())
        # print(final_selection.type())
        # print(final_selection.id())
        # print(final_selection.lat(), final_selection.lon())
        # print(final_selection.centerLat(), final_selection.centerLon())
        # print()   

        if not final_selection:
            search_dict = write_search_object_to_DB(search_list, type1.title(), save_places)
            return places_list, None

        data = nominatim.query(final_selection.type() + "/" + str(final_selection.id()), onlyCached=False, shallow=False, lookup=True, wkt=True)  # Always loads from file if exists and there are also 2 additional
        dataJSON = data.toJSON()

        osm_id = dataJSON[0]["osm_id"]
        area_id = data.areaId()
        lat = dataJSON[0]["lat"]
        lon = dataJSON[0]["lon"]
        geotext = dataJSON[0]["geotext"]
        search_list = (osm_id, area_id, lat, lon, geotext)

    search_dict = write_search_object_to_DB(search_list, type1.title(), save_places)

    # Final Step
    finalQuery =   '''  
                    area(%s)->.searchArea;
                    (
                    node["amenity"="%s"](area.searchArea);
                    way["amenity"="%s"](area.searchArea);
                    node["natural"="%s"](area.searchArea);
                    way["natural"="%s"](area.searchArea);
                    node["service"="%s"](area.searchArea);
                    way["service"="%s"](area.searchArea);
                    );
                    out center;                    
                    out body;
                    ''' % (area_id, type_snake_case, type_snake_case, type_snake_case, type_snake_case, type_snake_case, type_snake_case)

    data = overpass.query(finalQuery, timeout=10, onlyCached=False, shallow=False)

    # Debug
    # print("Total number of Found Elements:", len(data.elements()))  # https://github.com/mocnik-science/osm-python-tools/blob/master/docs/element.md

    for result in data.elements():
        if result.centerLat():
            lat = result.centerLat()
            lon = result.centerLon()
        elif result.lat():  
            lat = result.lat()
            lon = result.lon()
        else:
            continue

        reverse_geocode = nominatim.query(lat, lon, reverse=True, zoom=18, onlyCached=False, shallow=False)
        reverse_geo_address = reverse_geocode.address()
        detect_nominatim_name = list(reverse_geo_address.keys())[0]

        if detect_nominatim_name not in ['road', 'house_number']:
            name = reverse_geo_address[detect_nominatim_name]          
            address = ""
            if 'road' in reverse_geo_address:
                address += reverse_geo_address['road']
            if 'house_number' in reverse_geo_address:
                address +=  " " + reverse_geo_address['house_number'] 

            if address != "":
                address += ", "

            address += location

            if 'postcode' in reverse_geo_address:            
                address +=  " " + reverse_geo_address['postcode'][:3] + " " + reverse_geo_address['postcode'][3:]

            places_list[name] = ["id_placeholder", name, address, "global_id_placeholder"]

        # Debug
        # print(result.tags())
        # print(result.type())
        # print(result.id())
        # print(result.lat(), result.lon())
        # print(reverse_geocode.displayName())
        # print(reverse_geocode.address())
        # print()

    places_list = list(places_list.values())

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
   
    return places_list, search_dict

# Helper - Maps a string we receive from a Form to a string that can be used as a parameter inside the code, e.g. "Night Club" -> "night_club"
def type_mapper( type_p, mode ): 
    places_map = {"Bar": "bar", "Night Club": "night_club", "Restaurant": "restaurant", "Cafe": "cafe", "Bakery": "bakery", "Food": "food", "Subway Station": "subway_station", "Gas Station": "gas_station", "Bank": "bank", "Pharmacy": "pharmacy", "Health": "health", "Place of Worship": "place_of_worship", "Department Store": "department_store", "Establishment": "establishment", "University": "university", "Library": "library", "Book Store": "book_store", "Gym": "gym", "Clothing Store": "clothing_store", "Casino": "casino", "Liquor Store": "liquor_store", "Other": "other"}
    place_map_inv = {v: k for k, v in places_map.items()}

    if mode == 1:
        if type_p == "Choose...":
            return None
        else:
            return places_map[type_p]
    else:
        try: 
            return place_map_inv[type_p]
        except:
            return "Other"
        
# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
