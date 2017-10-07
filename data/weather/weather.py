import pyowm

def get_temperature():
	owm = pyowm.OWM('042400fd47928b3883a780aee2921aed')  # You MUST provide a valid API key
	observation = owm.weather_at_place('Offenburg,de')
	w = observation.get_weather()
	return w.get_temperature('celsius')