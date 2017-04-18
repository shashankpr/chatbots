import sys
from os import path
from datetime import datetime
from datetime import timedelta
import googlemaps
from weather import CallWeather

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from src import settings


GOOGLE_MAPS_TOKEN = settings.GOOGLE_MAPS_TOKEN


class CallGoogleTime(object):
    def __init__(self, location):
        self.location = location
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_TOKEN)

    # Geocoding an address - location to lat,long

    def geocode_location(self):
        """
        :param location:
        :return:
        """
        geocode_result = self.gmaps.geocode(self.location)

        lat = geocode_result[0]['geometry']['location']['lat']
        lng = geocode_result[0]['geometry']['location']['lng']

        return ((lat, lng))

    def get_reverse_geocode(self, coordinates):
        result = self.gmaps.reverse_geocode(coordinates)

        return result

    # Get Timezone for the geocoded location

    def world_time(self):
        """
        Get World Time using Google API
        :param:
        :return:
        """
        # Format is as follows :
        # %A Day
        # %d Date
        # %B Month
        # %H, %M, %S - Hour, Min, Sec

        format = "%A, %d. %B, %H:%M:%S"

        # Initialize Weather Object
        weatherObj = CallWeather(self.location)

        # retreiving coords from owm
        location_latlong = weatherObj.get_latlong()
        api_response = self.gmaps.timezone(location_latlong)

        # Daylight savings offset
        DST_offset = api_response['dstOffset']

        # UTC Offset
        UTC_offset = api_response['rawOffset']

        # Current Timestamp
        timestamp = datetime.utcnow()

        # Computing local time at the location
        local_time = timestamp + timedelta(seconds=DST_offset + UTC_offset)

        local_time = local_time.strftime(format)
        return str(local_time)