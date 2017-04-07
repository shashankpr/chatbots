import settings
import pyowm
import logging

logging.basicConfig(level=logging.DEBUG)

# OWM API TOKEN Parameters
OWM_API_TOKEN = settings.OWM_API_TOKEN

# Initialize OWM Class
owm = pyowm.OWM(OWM_API_TOKEN)
#forecast = owm.daily_forecast("London")

def inWeather(location):
	city_id = get_city_id(location)

	obs = owm.weather_at_id(city_id)
	w = obs.get_weather()
	detailed_weather = w.get_detailed_status()
	detailed_weather = detailed_weather.capitalize()
	temp = w.get_temperature('fahrenheit')
	temp = temp['temp']
	result = detailed_weather +' with a temperature of ' +str(temp)+' F'

	logging.info(result)
	return result

def get_city_id(location):
	registry_id = owm.city_id_registry()
	city_id = registry_id.id_for(location)

	logging.info("ID : {}".format(city_id))
	return city_id

def get_time(location):
	format = "%A, %d. %B, %H:%M:%S"
	city_id = get_city_id(location)

	obs = owm.weather_at_id(city_id)
	w = obs.get_weather()
	local_time = w.get_reference_time(timeformat='date')

	logging.info(str(local_time.strftime(format)))

	return str(local_time.strftime(format))

def get_latlong(location):
	"""
	This method return the coordinates of the location.
	"""
	city_id = get_city_id(location)
	obs = owm.weather_at_id(city_id)
	l = obs.get_location()
	lat = l.get_lat()
	lon = l.get_lon()
	return ((lat,lon))
