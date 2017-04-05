#import logging
#
#logging.basicConfig(level=logging.DEBUG)
#def inWeather(location):
#	forecast = 'rainy'
#	logging.info("{}".format(main_forecast))
#	return main_forecast
#name = 'London'
#inWeather(name)
import pyowm

owm = pyowm.OWM('929d3119163895b3abe69e0c5905f1bd')
#forecast = owm.daily_forecast("London")

def inWeather(location):
	obs = owm.weather_at_place(location)
	w = obs.get_weather()
	detailed_weather = w.get_detailed_status()
	temp = w.get_temperature(unit='celsius')
	return detailed_weather
