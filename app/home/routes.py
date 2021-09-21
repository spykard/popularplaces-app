# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request, abort, jsonify
from flask_login import login_required, current_user
from app import db, login_manager
from sqlalchemy import func, nullslast
from jinja2 import TemplateNotFound
from app.base.forms import EditProfileForm, EditSettingsForm, EditSettingsFormAdvanced, AddPlaceForm
from app.base.models import User, Place, Search, City, PlaceResult
from app.base.util import hash_pass
from datetime import datetime
import populartimes
import json

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
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

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
        if current_user.premium_enabled == 0: current_user.free_runs_remaining = current_user.free_runs_remaining-1
        db.session.commit()            

        # Main
        search_success, search_msg = search_populartimes(city, type1, type2, all_places)

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
    settings_form = EditSettingsFormAdvanced(request.form)
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
        if current_user.premium_enabled == 0: current_user.free_runs_remaining = current_user.free_runs_remaining-1
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
    # Load Cities
    places = db.session.query(Place, City).join(City).filter((Place.user_id == current_user.id) | (Place.global_place == 1)).order_by(Place.time.asc()).all() 
    place_dicts = []
    count = 1
    for place in places:
        place_dicts.append({'id': place[0].id, 'count': count, 'name': place[0].name, 'address': place[0].address, 'type': place[0].type_p,  'city': place[1].name, 'verification': place[0].verification, 'time': place[0].time.strftime("%Y-%m-%d")})
        count += 1

    add_place_form = AddPlaceForm(request.form)
    if 'name' in request.form:  # In this scenario we have not set a submit button, thus we check one of the input boxes' id

        # Read form data
        name = request.form['name']
        address = request.form['address']
        type_p = request.form['type_p']
        city = request.form['city'].title()        

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

        insert_dict = dict([("name" , name), ("address" , address), ("type_p" , type_p), ("user_id" , current_user.id), ("city_id" , city_to.id)])
        place_to = Place(**insert_dict)
        db.session.add(place_to)
        db.session.commit()

        # Load Cities
        places = db.session.query(Place, City).join(City).filter((Place.user_id == current_user.id) | (Place.global_place == 1)).order_by(Place.time.asc()).all() 
        place_dicts = []
        count = 1
        for place in places:
            place_dicts.append({'id': place[0].id, 'count': count, 'name': place[0].name, 'address': place[0].address, 'type': place[0].type_p,  'city': place[1].name, 'verification': place[0].verification, 'time': place[0].time.strftime("%Y-%m-%d")})
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
    #data = db.session.query(Place).filter((Place.id == id) & (Place.global_place == 1)).all()
    place_results = db.session.query(PlaceResult).join(Search).filter(Search.id == id).order_by(nullslast(PlaceResult.current_popularity.desc()), nullslast(PlaceResult.rating_num.desc())).all() 

    data = []
    converter = lambda i : i or ''  # Convert None to empty string
    for place_result in place_results:
        data.append({'name': place_result.name, 'address': place_result.address, 'rating': str(converter(place_result.rating)) + " (" + str(converter(place_result.rating_num)) + ")", 'popular_times': converter(place_result.popular_times),  'time_spent': converter(place_result.time_spent), 'current_popularity': converter(place_result.current_popularity), 'difference': converter(place_result.difference)})   

    return jsonify(data)

@blueprint.route('/delete-search', methods=['POST'])
@login_required
def delete_search():
    id = int(request.form['id'])
    if id == 0: abort(400)

    if current_user.is_authenticated:
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
def search_populartimes(city, type1, type2, all_places):
    ''' Query Google's PopularTimes, using a crawler that takes name and address of a specific place as input '''

    places = get_places_to_search(city, type1, type2, all_places)

    # Write Search Object to DB
    current_time = datetime.now()    
    user_id = ("user_id", current_user.id)
    if type2 == "Choose...": type2 = ""
    name = ("name", current_time.strftime("%Y%m%d-%H%M%S.%f") + "-" + str(user_id[1]))
    insert_dict = dict([("city" , city), ("settings_type1" , type1), ("settings_type2" , type2), ("settings_all_places" , all_places), user_id, name, ("type" , 1)])
    search = Search(**insert_dict)
    db.session.add(search)
    db.session.commit()  

    try:
        for place in places:
            # Debug
            # search_name = "Avli By Vouz"
            # search_address = "Pantanassis 17-29"
            # search_name = "Kynorodo"
            # search_address = "Korinthou 167, Patra 262 23"    
            search_name = place[1]
            search_address = place[2]
            data = populartimes.get_popular_times_by_crawl(name=search_name, address=search_address)            

            # Write Verification for Places to DB
            if data["populartimes"]:
                Place.query.filter_by(id=place[0]).update({"verification": "True"})

                if data["current_popularity"]:
                    difference = ("difference", data["current_popularity"] - data["populartimes"][current_time.weekday()]["data"][current_time.hour])
                else:
                    difference = ("difference", None)

            else:
                Place.query.filter_by(id=place[0]).update({"verification": "False"}) 
                difference = ("difference", None)

            # db.session.commit() 
             
            # if "time_wait" not in data:
            #     data["time_wait"] = None

            # Write Data to DB
            insert_dict = dict([("rating" , data["rating"]), ("rating_num" , data["rating_n"]), ("popular_times" , json.dumps(data["populartimes"])), ("time_spent" , data["time_spent"]), user_id, ("search_id", search.id), ("name" , search_name), ("address" , search_address), ("current_popularity" , data["current_popularity"]), difference])
            placeresult = PlaceResult(**insert_dict)
            db.session.add(placeresult)
            db.session.commit()

    except Exception as e:
        raise ValueError(str(e))
        return False, str(e) 

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

# Helper - Check whether user must be notified for Premium subscription Enabling
def notify_premium():
    if current_user.premium_enabled == 1 and current_user.premium_notified == 0:
        to_notify = "true"
        current_user.premium_notified = 1
        db.session.commit()        
    else:
        to_notify = "false"
    
    return to_notify

# Helper - Get the details of all the places that match the given Search Settings
def get_places_to_search(city, type1, type2, all_places):
    city_id = City.query.filter_by(name=city).first()
    if type2 != "Choose...":
        if all_places == 0:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & ((Place.type_p == type1) | (Place.type_p == type2)) & (Place.verification != "False")).order_by(Place.time.asc()).all()
        else:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & ((Place.type_p == type1) | (Place.type_p == type2))).order_by(Place.time.asc()).all()
    else:
        if all_places == 0:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & (Place.type_p == type1) & (Place.verification != "False")).order_by(Place.time.asc()).all()
        else:
            places = db.session.query(Place).join(City).filter((Place.city_id == city_id.id) & ((Place.user_id == current_user.id) | (Place.global_place == 1)) & (Place.type_p == type1)).order_by(Place.time.asc()).all()            

    places_list = []
    count = 1
    for place in places:
        places_list.append((place.id, place.name, place.address))
    
    return places_list

# Helper - Maps a string we receive from a Form to a string that can be used as a parameter inside the code, e.g. "Night Club" -> "night_club"
def type_mapper( type1, type2 ): 
    places_map = {"Bar": "bar", "Night Club": "night_club", "Restaurant": "restaurant", "Cafe": "cafe", "Bakery": "bakery", "Food": "food", "Subway Station": "subway_station", "Gas Station": "gas_station", "Bank": "bank", "Pharmacy": "pharmacy", "Health": "health", "Place of Worship": "place_of_worship", "Department Store": "department_store", "Establishment": "establishment", "University": "university", "Library": "library", "Book Store": "book_store", "Gym": "gym", "Clothing Store": "clothing_store", "Casino": "casino", "Liquor Store": "liquor_store"}
    to_return = []

    if type1 != "Choose...":
        to_return.append([places_map[type1]])
    if type2 != "Choose...":
        to_return.append([places_map[type2]])
    
    return to_return
        
# Helper - Extract current page name from request 
def get_segment( request ): 
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
