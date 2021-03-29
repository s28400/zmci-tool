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
Availalbe commands:
1. get_units
2. get_userinfo
3. get_last_transmit
4. get_history
```
### Command Descriptions
get_units: Gets units linked to account (motorcycles registered to user) with basic details.
get_userinfo: Gets all information about the user account.
get_last_transmist: Gets the most recent diagnostic packet that the motorcycle uploaded to cloud.
get_history: Gets diagnostic packets from cloud uploaded over a specified range (maximum 2 day range).

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
