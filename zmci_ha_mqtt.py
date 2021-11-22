#!/usr/bin/python3
#!python

import os
import sys
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from zmci_tool import ZeroCloudInterface


# TODO Get creds from env
# MQTT Creds:
mqtt_broker = '192.168.1.10'
mqtt_user = 'mqtt-user'
mqtt_pass = 'mqtt-password'

# Zero Creds
user_name = 'zero-user-email'
user_pass = 'zero-user-pass'


if __name__ == "__main__":

	# Create interface object with username and pass
	z1 = ZeroCloudInterface(user_name, user_pass)

	# Connect to HA MQTT broker
	client = mqtt.Client("ha-client")
	client.username_pw_set(username=mqtt_user,password=mqtt_pass)
	client.connect(mqtt_broker)
	client.loop_start()

	while True:

		# Fetch last data trasmit
		last_transmit = z1.get_info_by_command('get_last_transmit', unit_number=z1.units[0]['unitnumber'], additional_args=None)

		print(last_transmit)
	
		# Pack up useful data to send to HA via MQTT
		client.publish('home/motorcycle/vin', last_transmit[0]['name'])
		client.publish('home/motorcycle/sw_version', last_transmit[0]['software_version'])
		client.publish('home/motorcycle/soc', last_transmit[0]['soc'])
		client.publish('home/motorcycle/mileage', last_transmit[0]['mileage'])
		client.publish('home/motorcycle/latitude',last_transmit[0]['latitude'])
		client.publish('home/motorcycle/longitude',last_transmit[0]['longitude'])

		client.publish('home/motorcycle/velocity',last_transmit[0]['velocity'])
		client.publish('home/motorcycle/heading',last_transmit[0]['heading'])
		client.publish('home/motorcycle/shock',last_transmit[0]['shock'])
		client.publish('home/motorcycle/tipover',last_transmit[0]['tipover'])
		client.publish('home/motorcycle/charging',last_transmit[0]['charging'])
		client.publish('home/motorcycle/chargecomplete',last_transmit[0]['chargecomplete'])
		client.publish('home/motorcycle/pluggedin',last_transmit[0]['pluggedin'])
		client.publish('home/motorcycle/chargingtimeleft',last_transmit[0]['chargingtimeleft'])
		client.publish('home/motorcycle/analog1',last_transmit[0]['analog1'])
		client.publish('home/motorcycle/main_voltage',last_transmit[0]['main_voltage'])


		time.sleep(5)


	# TODO Setup systemd to call script every x minutes and kill loop