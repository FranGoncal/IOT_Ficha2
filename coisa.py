from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt
import json



id = '78354614315'

client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")

sensor = DHT("11", 5)


while True:
	_, temp = sensor.read()
	#print(f'Temperature {temp}°C')
	telemetry = json.dumps({'temperature' : temp})

	print("Sending telemetry ", telemetry)

	mqtt_client.publish(client_telemetry_topic, telemetry)
	
	time.sleep(10)
	#time.sleep(10 * 60)
