import settings
import pyowm

# OWM API TOKEN Parameters
OWM_API_TOKEN = settings.OWM_API_TOKEN

# Initialize OWM Class
owm = pyowm.OWM(OWM_API_TOKEN)
#forecast = owm.daily_forecast("London")

def inWeather(location):
	obs = owm.weather_at_place(location)
	w = obs.get_weather()
	detailed_weather = w.get_detailed_status()
	detailed_weather = detailed_weather.capitalize()
	temp = w.get_temperature('fahrenheit')
	temp = temp['temp']
	result = detailed_weather +' with a temperature of ' +str(temp)+' F'
	return result
