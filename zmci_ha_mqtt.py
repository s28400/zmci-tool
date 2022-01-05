#!/usr/bin/python3
#!python

import os
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from zmci_tool import ZeroCloudInterface
from dotenv import load_dotenv
from datetime import datetime


if __name__ == "__main__":

	# Load .env to get credentials
	try:
		load_dotenv()
	except:
		print("Could not load .env file, does it exist?")

	print("Got credentials from .env file:")
	print(f"ZERO_USER: {os.getenv('ZERO_USER')}")
	print(f"MQTT_USER: {os.getenv('MQTT_USER')}")

	# MQTT Creds:
	mqtt_broker = os.getenv('MQTT_HOST')
	mqtt_user = os.getenv('MQTT_USER')
	mqtt_pass = os.getenv('MQTT_PASS')

	# Zero Creds
	user_name = os.getenv('ZERO_USER')
	user_pass = os.getenv('ZERO_PASS')


	# Create interface object with username and pass
	z1 = ZeroCloudInterface(user_name, user_pass)

	# Connect to HA MQTT broker
	client = mqtt.Client("ha-client")
	client.username_pw_set(username=mqtt_user,password=mqtt_pass)
	client.connect(mqtt_broker)
	client.loop_start()


	# Fetch last data trasmit
	last_transmit = z1.get_info_by_command('get_last_transmit', unit_number=z1.units[0]['unitnumber'], additional_args=None)

	print(f"Last Transmit Data: {last_transmit}")

	# Convert UTC timestamp to formatted string
	dt_obj = datetime.strptime(last_transmit[0]['datetime_utc'], '%Y%m%d%H%M%S')

	# Pack up useful data to send to HA via MQTT
	client.publish('home/motorcycle/datetime_utc', str(dt_obj))
	client.publish('home/motorcycle/vin', last_transmit[0]['name'])
	client.publish('home/motorcycle/sw_version', last_transmit[0]['software_version'])
	client.publish('home/motorcycle/soc', last_transmit[0]['soc'])
	client.publish('home/motorcycle/mileage', int(float(last_transmit[0]['mileage'])*0.62127))  # Convert to miles
	client.publish('home/motorcycle/latitude',last_transmit[0]['latitude'])
	client.publish('home/motorcycle/longitude',last_transmit[0]['longitude'])

	client.publish('home/motorcycle/velocity',int(float(last_transmit[0]['velocity'])*0.62167))  # Convert to mph
	client.publish('home/motorcycle/heading',last_transmit[0]['heading'])
	client.publish('home/motorcycle/shock',last_transmit[0]['shock'])
	client.publish('home/motorcycle/tipover',last_transmit[0]['tipover'])
	client.publish('home/motorcycle/charging',last_transmit[0]['charging'])
	client.publish('home/motorcycle/chargecomplete',last_transmit[0]['chargecomplete'])
	client.publish('home/motorcycle/pluggedin',last_transmit[0]['pluggedin'])
	client.publish('home/motorcycle/chargingtimeleft',last_transmit[0]['chargingtimeleft'])
	client.publish('home/motorcycle/analog1',last_transmit[0]['analog1'])
	client.publish('home/motorcycle/main_voltage',last_transmit[0]['main_voltage'])

	print("ZMCI HA MQTT done!")