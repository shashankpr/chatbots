import logging

logging.basicConfig(level=logging.DEBUG)
def inWeather(location):
	forecast = 'rainy'
	main_forecast = location + forecast
	logging.info("{}".format(main_forecast))
	return main_forecast

name = 'London'
inWeather(name)
