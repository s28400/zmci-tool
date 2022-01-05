# zmci-tool
Non official zero-motorcycle cloud interface tool


## Tool Installation
To get up and running quickly, you only need to have a python3 environment and clone this repo into it. 


## Tool Usage
This tool contains an example main function that demonstrates basic functionality. To run the example, execute the script with
```
./zmc-tool.py
```
The tool will then ask for your user name (email) and password that you use on the zero app.

If the credentials are correct, it will then fetch the unit(s) associated with the account. If there are multiple, it will prompt to select one.

Next it will display the following menu:
```
#### MAIN MENU ####
Available commands:
1. get_units
2. get_userinfo
3. get_last_transmit
4. get_history
```

### Command Descriptions
get_units: Gets units linked to account (motorcycles registered to user) with basic details.
get_userinfo: Gets all information about the user account.
get_last_transmit: Gets the most recent diagnostic packet that the motorcycle uploaded to cloud.
get_history: Gets diagnostic packets from cloud uploaded over a specified range (maximum 2 day range).



# HomeAssistant MQTT Client:

The HomeAssistant MQTT Client allows for zero integration into the HomeAssistant ecosystem. Until I have time to properly write a built in integration for home assistant, this MQTT based data forwarder works perfect with minimal setup.


## Installation:
The HomeAssistant MQTT client can be setup quickly on a separate host. For this example, I'll be using a Ubuntu VM running alongside my HomeAssistant instance.

Before beginning, make sure you have the following prerequisites satisfied:
- Ubuntu or other Linux distro host to run the client
- Requirements installed from requirements.txt
- HomeAssistant instance with MQTT broker installed and configured (you'll need the credentials for this)


### Linux Host Side Configuration:

First, let's configure the host side which will run the script to fetch data from your Zero account and forward it to HomeAssistant.

1. Clone the repo to the host machine to ```/home/<user>/zmci_tool/```.

2. Sanity check the tool is working and you can access your account by running ```./zmci_tool.py``` and following the prompts:

3. Create a .env file in the zmci_tool directory and enter both your zero account and MQTT broker credentials as follows:
```
ZERO_USER=zero_user_email
ZERO_PASS=zero_user_pass
MQTT_HOST=mqtt_broker_ip
MQTT_USER=mqtt_user
MQTT_PASS=mqtt_pass

```

4. Test run home assistant mqtt script and check for received data packet with:
```
./zmci_ha_mqtt.py
```

5. Navigate to the systemd directory and update the user and path in zmci_ha_mqtt.service to match your host setup.


6. Copy systemd service and timer to your host with:
```
sudo cp zmci_ha_mqtt.service /etc/systemd/system
```
and
```
sudo cp zmci_ha_mqtt.timer /etc/systemd/system
```

6. Enable and start service and timer with:
```
sudo systemctl enable zmci_ha_mqtt.service
```
and
```
sudo systemctl enable zmci_ha_mqtt.timer
```
and finally
```
sudo systemctl start zmci_ha_mqtt.timer
```

7. Check journalctl logs with:
```
sudo journalctl
```
and use end key to navigate to bottom. You should see logs of service running and fetching data without errors. That's it, there should be data fetching from your zero account and forwarding to HomeAssistant via MQTT. Neat!


### HomeAssistant Side Configuration:

Now we need to get the MQTT data into a device/entities in HomeAssistant and also create a location tracker from the raw longitude/latitude data.

1. Add the following to scripts.yaml in home assistant which will create the Zero device with data entities. Past in the following:
```
## Zero MQTT Create
zero_motorcycle_create:
  alias: "Zero Motorcycle MQTT - Create"
  sequence:
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/soc/config"
        retain: true
        payload: >
          {
            "name": "Zero Packet Datetime UTC",
            "state_topic": "home/motorcycle/datetime_utc",
            "unit_of_measurement": "UTC",
            "unique_id": "zero_srf_datetime_utc",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/soc/config"
        retain: true
        payload: >
          {
            "name": "Zero SoC",
            "state_topic": "home/motorcycle/soc",
            "unit_of_measurement": "%",
            "unique_id": "zero_srf_soc",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/vin/config"
        retain: true
        payload: >
          {
            "name": "Zero VIN",
            "state_topic": "home/motorcycle/vin",
            "unique_id": "zero_srf_vin",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/sw/config"
        retain: true
        payload: >
          {
            "name": "Zero Software Version",
            "state_topic": "home/motorcycle/sw_version",
            "unique_id": "zero_srf_sw_version",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/mileage/config"
        retain: true
        payload: >
          {
            "name": "Zero Mileage",
            "state_topic": "home/motorcycle/mileage",
            "unit_of_measurement": "miles",
            "unique_id": "zero_srf_mileage",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/latitude/config"
        retain: true
        payload: >
          {
            "name": "Zero Latitude",
            "state_topic": "home/motorcycle/latitude",
            "unique_id": "zero_srf_latitude",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/longitude/config"
        retain: true
        payload: >
          {
            "name": "Zero Longitude",
            "state_topic": "home/motorcycle/longitude",
            "unique_id": "zero_srf_longitude",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/velocity/config"
        retain: true
        payload: >
          {
            "name": "Zero Velocity",
            "state_topic": "home/motorcycle/velocity",
            "unit_of_measurement": "mph",
            "unique_id": "zero_srf_velocity",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/heading/config"
        retain: true
        payload: >
          {
            "name": "Zero Heading",
            "state_topic": "home/motorcycle/heading",
            "unique_id": "zero_srf_heading",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/binary_sensor/shock/config"
        retain: true
        payload: >
          {
            "name": "Zero Shock",
            "state_topic": "home/motorcycle/shock",
            "unique_id": "zero_srf_shock",
            "state_on": "1",
            "state_off": "0",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/binary_sensor/tipover/config"
        retain: true
        payload: >
          {
            "name": "Zero Tipover",
            "state_topic": "home/motorcycle/tipover",
            "unique_id": "zero_srf_tipover",
            "payload_on": "1",
            "payload_off": "0",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/binary_sensor/charging/config"
        retain: true
        payload: >
          {
            "name": "Zero Charging",
            "state_topic": "home/motorcycle/charging",
            "unique_id": "zero_srf_charging",
            "payload_on": "1",
            "payload_off": "0",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/binary_sensor/chargecomplete/config"
        retain: true
        payload: >
          {
            "name": "Zero Charge Complete",
            "state_topic": "home/motorcycle/chargecomplete",
            "unique_id": "zero_srf_chargecomplete",
            "payload_on": "1",
            "payload_off": "0",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/binary_sensor/pluggedin/config"
        retain: true
        payload: >
          {
            "name": "Zero Plugged In",
            "state_topic": "home/motorcycle/pluggedin",
            "unique_id": "zero_srf_pluggedin",
            "payload_on": "1",
            "payload_off": "0",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/chargingtimeleft/config"
        retain: true
        payload: >
          {
            "name": "Zero Charging Time Left",
            "state_topic": "home/motorcycle/chargingtimeleft",
            "unique_id": "zero_srf_chargingtimeleft",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }
    - service: mqtt.publish
      data:
        topic: "homeassistant/sensor/mainvoltage/config"
        retain: true
        payload: >
          {
            "name": "Zero Main Voltage",
            "state_topic": "home/motorcycle/main_voltage",
            "unit_of_measurement": "V",
            "unique_id": "zero_srf_main_voltage",
            "device": {
                "identifiers": ["zero_srf"],
                "name": "Zero SR/F",
                "model": "SR/F",
                "manufacturer": "Zero Motorcycles"
            }
          }

```
In my case, I have the SR/F model so I named it accordingly in the above script. You can change it to match your model if different.

Restart HomeAssistant or refresh scripts and head to the scripts page under configuration. You should now see a script "Zero Motorcycle MQTT - Create"

Run this script to create the Zero motorcycle device with data entities.

Next, navigate to devices under configuration and check that the Zero device has been created and that the entities are populating with data from the running service.

NOTE: If you want to update the device/entities, delete the device, then update script, refresh scripts and re-run script. 

Next, we need to make a location tracker from the device latitude and longitude data. To do so, make a new automation and paste in the following:
```
alias: Zero Tracker
description: ''
trigger:
  - platform: state
    entity_id: sensor.zero_latitude
  - platform: state
    entity_id: sensor.zero_longitude
  - platform: time_pattern
    minutes: /5
condition: []
action:
  - service: device_tracker.see
    data_template:
      dev_id: zero_location
      gps_accuracy: 50
      gps:
        - '{{ states(''sensor.zero_latitude'') }}'
        - '{{ states(''sensor.zero_longitude'') }}'
mode: single
```

Finally, make a nice dash board to show off the data. I pulled in an image of the bike, used some gauges to display SoC, remaining charge time, and mileage as well as some history graphs. I also made some alerts and automatons for when the bike starts/stops charging and when charging is complete. It's nice to have reminders if I forget to plug in the night before work and the SoC is low.



## Diagnostics Information Contents:

### Useful Diagnostic Contents:
```
unitnumber: Unique unit number for motorcycle (string)
name: Motorcycle VIN (string)
unittype: Unclear what this equates to (int)
unitmodel: Unclear what this equates to (int)
analog1: Unknown (float)
milleage: Motorcyle odometer (float)
software_version: Motorcycle FW version (int)
logic_state: Unknown (unknown)
reason: Unknown (unknown)
response: Unknown (unknown)
driver: Unknown (unknown)
logitude: Motorcycle GPS logitude (float)
latitude: Motorcycle GPS lattitude (float)
altitude: Motorcycle GPS altitude (int)
gps_valid: Unclear what this is, probable if gps coords are fresh (boolean)
gps_connected: Motorcycle GPS connected (boolean) 
satellites: Number of satellites connected for GPS
velocity: Motorcycle GPS velocity, not accurate (int)
heading: Motorcycle GPS heading (int)
emergency: Unclear what this is (boolean)
shock: Motorcycle experienced shock/impact recently (boolean) 
ignition: Motorcycle ignition on (boolean)
door: Unknown (unknown)
hood: Unknown (unknown)
volume: Unknown (unknown)
water_temp: Unknown (unknown)
oil_pressure: Unknown (unknown)
main_voltage: Charger voltage? (float)
siren: Unknown (unknown)
lock: Unknown (unknown)
int_lights: Unknown (unknown)
datetime_utc: Datetime of packet upload in UTC format (int)
datetime_actual: Datetime of packet uploaded (int)
address: Motorcycle location address (string)
perimeter: Unknown (unknown)
color: Motorcycle color (int)
soc: Motorcycle state of charge (int)
charging: Motorcycle charging (boolean)
tipover: Motorcycle tipover (boolean)
chargercomplete: Charge complete (boolean)
pluggedin: Motorcycle charger plugged in (boolean)
chargingtimeleft: Motorcycle charge time left (boolean)
storage: Unknown (unknown)
```

### Unknown Diagnostic Packet Contents:
```
analog1
logic_state
reason
response
driver
door
hood
volume
water_temp
oil_pressure
siren
lock
int_lights
storage
```

### Unit Packet Contents
```
unitnumber: Unique unit number for motorcycle (string)
name: Motorcycle VIN (string)
address: Country code of registered unit (string)
vehiclemodel: Unknown (int)
unittype: Unknown (int)
icon: Unknown (unknown)
active: Unknown (boolean)
unitmodel: Unknown (int)
custom: Unknown (list/array)
```

### User Info Packet Contents
```
fullname: Account username email (string)
phone: Account phone number (string)
email: Account email (string)
country: Account country (string)
utcdifference: Unknown (unknown)
timezone: Empty field
language: Language code (string)
speedunits: Unknown (int)
allowcommands: Unknown (boolean)
allowstop: Unknown (boolean)
allowlogic: Unknown (boolean)
allowclearfleet: Unknown (boolean)
template: Unknown (string)
maptype: Unknown (unknown)
allowhistoryreport: Unknown (boolean)
addunitsbycode: Unknown (boolean)
logourl: URL for logo (string)
```


## Other Information
The tracking system used appears to be made by Starcom Systems: https://www.starcomsystems.com/

Further research around these systems could help explain some of the still unknown values. Some of these values could be general values from the OTS system that is not used by the motorcycle.
