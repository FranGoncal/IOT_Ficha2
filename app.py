from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import json
import paho.mqtt.client as mqtt

id = 'asdffdas'

client_name = id + 'soilmoisturesensor_client'
server_command_topic = id + '/commands'
client_telemetry_topic = id + '/telemetry'

adc = ADC()
relay = GroveRelay(7)

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

def handle_command(client, userdata, message):
	payload = json.loads(message.payload.decode())
	print("Message received:", payload)

	if payload['relay_on']:
		relay.on()
	else:
		relay.off()
        
mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
	soil_moisture = adc.read(0)
	print("Soil moisture:", soil_moisture)
	telemetry = json.dumps({'soil_moisture' : soil_moisture})
	print("Sending telemetry ", telemetry)
	#cliente manda um telemetry
	mqtt_client.publish(client_telemetry_topic, telemetry)

	time.sleep(10)







