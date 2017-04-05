import pyowm

owm = pyowm.OWM('929d3119163895b3abe69e0c5905f1bd')
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
