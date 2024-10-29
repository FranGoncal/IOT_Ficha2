import json
import time

import paho.mqtt.client as mqtt
import threading

id = 'asdffdas'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soilmoisturesensor_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

water_time = 5
wait_time = 20

def send_relay_command(client, state):
	#state = true | false
    command = { 'relay_on' : state }
    print("Sending message:", command)
    client.publish(server_command_topic, json.dumps(command))

def control_relay(client):
	#5 nao le mensagnes
    print("Unsubscribing from telemetry")
    mqtt_client.unsubscribe(client_telemetry_topic)

	#6manda true para o relay (ligar)
    send_relay_command(client, True)
    	#7 espera 5 segundos
    time.sleep(water_time)
	#8 desliga o relay (false)
    send_relay_command(client, False)
	#9 espera 20 segundos
    time.sleep(wait_time)

	#10 volta a ler as mensagens
    print("Subscribing to telemetry")
    mqtt_client.subscribe(client_telemetry_topic)

def handle_telemetry(client, userdata, message):
	#1 le o nivel
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
	#2 verifica o nivel
    if payload['soil_moisture'] > 450:
    	#3 chama o control_relay(client)
        threading.Thread(target=control_relay, args=(client,)).start()

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)
    
    
    
    
