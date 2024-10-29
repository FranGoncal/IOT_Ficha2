from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)
import time
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt
import json
import threading


id = '52313255'
client_name = id + 'soilmoisturesensor_client'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

water_time = 5
wait_time = 20

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'


adc = ADC()
relay = GroveRelay(7)

def send_relay_command(client, state):
    command = { 'relay_on' : state }
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

def control_relay(client):
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)

    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)

    time.sleep(wait_time)

    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)

def handle_command(client, userdata, message):
	payload = json.loads(message.payload.decode())
	print("Message received:", payload)

	if payload['relay_on']:
		relay.on()
	else:
		relay.off()

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['soil_moisture'] > 450:
        threading.Thread(target=control_relay, args=(client,)).start()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
	soil_moisture = adc.read(0)
	print("Soil moisture:", soil_moisture)

	mqtt_client.publish(client_telemetry_topic, json.dumps({'soil_moisture' : soil_moisture}))

	time.sleep(10)
