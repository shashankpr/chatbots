import settings
import googlemaps
from datetime import datetime
from datetime import timedelta

GOOGLE_MAPS_TOKEN = settings.GOOGLE_MAPS_TOKEN

gmaps = googlemaps.Client(key=GOOGLE_MAPS_TOKEN)

# Geocoding an address - location to lat,long

def geocode_location(location):
    """
    :param location: 
    :return: 
    """
    geocode_result = gmaps.geocode(location)

    lat = geocode_result[0]['geometry']['location']['lat']
    lng = geocode_result[0]['geometry']['location']['lng']

    return ((lat,lng))

def reverse_geocode(coordinates):

    result = gmaps.reverse_geocode((coordinates))

    return result

# Get Timezone for the geocoded location

def world_time(location):
    """
    :param location: 
    :return: 
    """
    # Format is as follows :
    # %A Day
    # %d Date
    # %B Month
    # %H, %M, %S - Hour, Min, Sec

    format = "%A, %d. %B, %H:%M:%S"

    location_latlong = geocode_location(location)
    api_response  = gmaps.timezone(location_latlong)

    # Daylight savings offset
    DST_offset = api_response['dstOffset']

    # UTC Offset
    UTC_offset = api_response['rawOffset']

    # Current Timestamp
    timestamp = datetime.utcnow()

    # Computing local time at the location
    local_time = timestamp + timedelta(seconds = DST_offset + UTC_offset)


    local_time = local_time.strftime(format)
    return str(local_time)
