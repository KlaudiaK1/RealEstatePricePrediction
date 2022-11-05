# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import joblib
import re
import requests
from numpy import nan
import sys
import pickle
from tensorflow.keras.models import  load_model
from xgboost import XGBClassifier
import pandas as pd


def get_address_details(localisation):
    localisation = re.sub(r'\w*\.\w*', '', localisation).strip()
    r = requests.get(f'https://nominatim.openstreetmap.org/search/{localisation}?format=json&addressdetails=1')
    if(bool(r.json())):
        result = r.json()[0]
        address_details = result['address']
        return {'latitude': result['lat'], 'longtitude': result['lon'], 'city': address_details.get('city', nan), 'state': address_details.get('state', nan), 'village': address_details.get('village', nan), 'town': address_details.get('town', nan), 'road': address_details.get('road', nan), 'city_district': address_details.get('city_district', nan)}


def get_population(locality):
    r = requests.get(f'https://public.opendatasoft.com/api/records/1.0/search/?dataset=geonames-all-cities-with-a-population-1000&q={locality}')
    if(locality.lower() == 'Warszawa'.lower()):
        return 1765000
    if(bool(r.json().get('records'))):
        return r.json().get('records')[0].get('fields').get('population')

def get_time_to_nearest_point(point_type, lat, lon):
    result = requests.get(f'https://nominatim.openstreetmap.org/search.php?q={point_type}+near+{lat},{lon}&format=jsonv2&limit=1').json()
    if(bool(result)):
        point_lat = result[0].get('lat')
        point_lon = result[0].get('lon')
        duration_res = requests.get(f'https://router.project-osrm.org/route/v1/car/{lon},{lat};{point_lon},{point_lat}?overview=false').json()
        if(bool(duration_res and bool(duration_res.get('routes')))):
            duration = duration_res.get('routes')[0].get('duration') 
            return duration / 60 #convert to minutes

def get_time_to_nearest_shop(lat, lon):
    time_to_nearest_supermarket = get_time_to_nearest_point('supermarket', lat, lon)
    time_to_nearest_convenience_shop = get_time_to_nearest_point('convenience_shop', lat, lon)
    
    result = min(time_to_nearest_supermarket or 100000, time_to_nearest_convenience_shop or 100000)
    
    if(result != 100000):
        return result

def get_time_to_nearest_stop(lat, lon):
    time_to_nearest_bus_stop = get_time_to_nearest_point('bus stop', lat, lon)
    time_to_nearest_tram_stop = get_time_to_nearest_point('tram stop', lat, lon)
    
    result = min(time_to_nearest_bus_stop or 100000, time_to_nearest_tram_stop or 100000) 
    
    if(result != 100000):
        return result

def get_time_to_centre(lat, lon, location):
    result = requests.get(f'https://nominatim.openstreetmap.org/search/{location}?format=json&addressdetails=1').json()
    if(bool(result)):
        centre_lat = result[0].get('lat')
        centre_lon = result[0].get('lon')
        duration_res = requests.get(f'https://router.project-osrm.org/route/v1/car/{lon},{lat};{centre_lon},{centre_lat}?overview=false').json()
        if(bool(duration_res) and bool(duration_res.get('routes'))):
            duration = duration_res.get('routes')[0].get('duration')  
            return duration / 60

def get_additional_information(localisation):
    dict_temp = get_address_details(localisation)
    if(bool(dict_temp)):
        state = dict_temp.get('state')

        if(isinstance(dict_temp.get('city'), str)):
            locality = dict_temp.get('city')
            population = get_population(dict_temp.get('city'))
            type_of_locality = 'city'
        if(isinstance(dict_temp.get('village'), str)):
            locality = dict_temp.get('village')
            population = get_population(dict_temp.get('village'))
            type_of_locality = 'village'
        if(isinstance(dict_temp.get('town'), str)):
            locality = dict_temp.get('town')
            population = get_population(dict_temp.get('town'))
            type_of_locality = 'town'

        latitude = dict_temp.get('latitude')
        longtitude = dict_temp.get('longtitude')
        print(locality)
        time_to_nearest_shop = get_time_to_nearest_shop(latitude, longtitude)
        time_to_nearest_stop = get_time_to_nearest_stop(latitude, longtitude)
        time_to_centre = get_time_to_centre(latitude, longtitude, locality)
        population = get_population(locality)

    return {'state': nan if state is None else state, 'locality': nan if locality is None else locality, 'type_of_locality': nan if type_of_locality is None else type_of_locality,'time_to_nearest_shop': nan if time_to_nearest_shop is None else time_to_nearest_shop, 'time_to_nearest_stop': nan if time_to_nearest_stop is None else time_to_nearest_stop, 'time_to_centre': nan if time_to_centre is None else time_to_centre, 'population': nan if population is None else population}

def transform_data(data_type, property_type, transformer_type, data_frame):
    transformer = joblib.load(open(f'../preprocessing/{data_type}_{transformer_type}_{property_type}.save', 'rb'))
    data_frame[[data_type]] = transformer.transform(data_frame[[data_type]].to_numpy())

def extract_data(data):
    if(bool(data)): 
        return int(re.findall('(\d+\.*,*\d*)', data)[0])
    return nan

finishing_standard_dict = {'to renovate': 'do remontu', 'ready to move in': 'do zamieszkania', 'shell condition': 'do wykończenia'}
heating_type_dict = {'gas': 'gazowe', 'electric': 'elektryczne', 'tiled stove': 'piece kaflowe', 'urban heating': 'miejskie', 'boiler': 'kotłownia'}
market_dict = {'primary': 'pierwotny', 'secondary': 'wtórny'}
building_type_dict = {'residential block': 'blok', 'apartment building': 'apartamentowiec', 'tenement': 'kamienica', 'detached': 'dom wolnostojący', 'semidetached': 'bliźniak', 'manor': 'dworek/pałac', 'farm': 'gospodarstwo', 'row house': 'szeregowiec'}

class ActionPrintInformation(Action):

    def name(self) -> Text:
        return "validate_newsletter_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        localisation = tracker.get_slot('localisation')
        area = tracker.get_slot('area')
        finishing_standard = tracker.get_slot('finishing_standard')

        print(localisation)
        print(area)
        print(finishing_standard)
        return []

class ActionEstimateFlatPrice(Action):
    def name(self) -> Text:
        return 'estimate_flat_price'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        loaded_model = joblib.load(open('./grid_search_model.save', 'rb'))

        #categorical values
        finishing_standard = finishing_standard_dict.get(tracker.get_slot('finishing_standard'), nan)
        heating_type = heating_type_dict.get(tracker.get_slot('heating_type'), nan)
        market = market_dict.get(tracker.get_slot('market'), nan)
        building_type = building_type_dict.get(tracker.get_slot('building_type'), nan)

        #numerical values
        area = extract_data(tracker.get_slot('area'))
        number_of_rooms = extract_data(tracker.get_slot('number_of_rooms'))
        floor = extract_data(tracker.get_slot('floor'))
        rent = extract_data(tracker.get_slot('rent'))
        number_of_floors = extract_data(tracker.get_slot('number_of_floors'))
        age =  2022 - extract_data(tracker.get_slot('construction_year'))

        #boolean values
        has_balcony = 0
        has_terrace = 0
        has_garden = 0
        balcony_terrace_garden = tracker.get_slot('balcony_terrace_garden')
        if(balcony_terrace_garden == 'balcony'):
            has_balcony = 1
        if(balcony_terrace_garden == 'terrace'):
            has_terrace = 1
        if(balcony_terrace_garden == 'garden'):
            has_garden = 1
        is_parking = int(tracker.get_slot('is_parking'))
        is_furnished = int(tracker.get_slot('is_furnished'))
        is_lift = int(tracker.get_slot('is_lift'))
        is_security = int(tracker.get_slot('is_security'))
        is_duplex = int(tracker.get_slot('is_duplex'))
        is_basement = int(tracker.get_slot('is_basement'))

        print(is_parking)

        localisation = tracker.get_slot('localisation')
        additional_information = get_additional_information(localisation)

        print(additional_information)

        #additional values
        state = additional_information.get('state')
        locality = additional_information.get('locality')
        population = additional_information.get('population')
        type_of_locality = additional_information.get('type_of_locality')
        time_to_nearest_shop = additional_information.get('time_to_nearest_shop')
        time_to_nearest_stop = additional_information.get('time_to_nearest_stop')
        time_to_centre = additional_information.get('time_to_centre')

        #creating a data frame with one row
        data_frame = pd.DataFrame([[area, number_of_rooms, finishing_standard, floor, rent, heating_type, market, building_type, state, locality, population, type_of_locality, time_to_nearest_shop, time_to_nearest_stop, time_to_centre]], columns=['area', 'number_of_rooms', 'finishing_standard', 'floor', 'rent', 'heating', 'market', 'building_type', 'state', 'locality', 'population', 'type_of_locality', 'time_to_nearest_shop', 'time_to_nearest_stop', 'time_to_centre'])

        print(data_frame)

        transform_data('area', 'flats', 'scaler', data_frame)
        transform_data('rent', 'flats', 'scaler', data_frame)
        
        print(data_frame)

        print(localisation)
        print(area)
        print(number_of_rooms)
        print(finishing_standard)
        print(floor)
        print()
        return []
        
