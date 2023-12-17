import googlemaps
from datetime import datetime
import urllib.parse
#import pyshorteners

# 請填入你的 Google Maps API 金鑰
api_key = 'AIzaSyBq22u-UfqFsez8TL_YzHStxBC5v6HhmOs'
gmaps = googlemaps.Client(key=api_key)

def to_short_url(original_url):
    # 使用 TinyURL 服務
    #s = pyshorteners.Shortener()
    #short_url = s.tinyurl.short(original_url)
    #return short_url
    return original_url

def get_coordinates(location):
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        location_info = geocode_result[0]['formatted_address']
        return location_info
    else:
        return None

def generate_google_maps_directions_link(locations):
    places_info = []
    places_link = []
    i = 1
    for location_data in locations:
        location = location_data["location"]
        # 進行地理編碼
        geocode_result = gmaps.geocode(location)
        #print(geocode_result)
        if geocode_result:
            # 獲取地點的地理座標
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            place_id = geocode_result[0]['place_id']
            # 構建 Google Maps 連結
            single_place = f"https://www.google.com/maps/search/?api=1&query={latitude}%2C-{longitude}&query_place_id={place_id}"
            place_short_link = to_short_url(single_place)
            places_link.append({'order': i, 'location': location, 'url': place_short_link})

            # 構建 Google Maps 旅遊規劃連結
            places_info.append({'name': location, 'id':place_id})
            i+=1

    _names = [item['name'] for item in places_info]
    way_names = '|'.join(_names)
    _ids = [item['id'] for item in places_info]
    way_ids = '|'.join(_ids)
    directions_link = f'https://www.google.com/maps/dir/?api=1&origin={places_info[0]["name"]}&origin_place_id={places_info[0]["id"]}&waypoints={way_names}&waypoint_place_ids={way_ids}&destination={places_info[-1]["name"]}&destination_place_id={places_info[-1]["id"]}&travelmode=driving'
    #print(directions_link)
    travel_link = to_short_url(directions_link)

    return {'status': True, 'location_list': places_link, 'url': travel_link}


#print(generate_google_maps_directions_link(locations));

# https://www.google.com/maps/search/?api=1&query=24.8244437%2C-121.6996876&query_place_id=ChIJ1bDi_mH8ZzQRnkhhoTrdJkg
# https://www.google.com/maps/dir/?api=1&origin=渭水之丘&origin_place_id=ChIJ1bDi_mH8ZzQRnkhhoTrdJkg&waypoints=張美阿嬤農場|清水地熱公園&waypoint_place_ids=ChIJhfheDgnhZzQRzHYRfqcbt3E|ChIJVVVVVRVxaDQRDc3Y8MyRVlE&destination=紅樓中餐廳&destination_place_id=ChIJGfBznMPkZzQR_glSXRElhag&travelmode=driving
