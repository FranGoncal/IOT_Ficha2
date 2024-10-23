from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

adc = ADC()
relay = GroveRelay(7)

while True:
	relay.on()
	time.sleep(.5)
	relay.off()
	soil_moisture = adc.read(0)
	print("Soil moisture:", soil_moisture)

	time.sleep(10)


