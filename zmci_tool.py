#!/usr/bin/python3
#!python

import os
import sys
import time
import requests
from getpass import getpass
import json

# Configuration
data_format = "json"  # Format to return data back as (Options: json, csv)
POLLING_INTERVAL = 60

# Basic defines
GET_UNITS = 'get_units'
GET_USERINFO = 'get_userinfo'
GET_LAST_TRANSMIT = 'get_last_transmit'
GET_HISTORY = 'get_history'

command_list = [GET_UNITS,
                GET_USERINFO,
                GET_LAST_TRANSMIT,
                GET_HISTORY]

url = "https://mongol.brono.com/mongol/api.php"

# Packet Info Defines
COLORS = {'blue': 1, 'red': 2, 'black': 3}  # Only know red model
UNIT_MODEL = {'sr/f': 6, 'sr/s': 7}  # From key 'unittype' SR/S not confirmed


class ZeroCloudInterface:


    def __init__(self, user_name, user_pass):
        self.user_name = user_name
        self.user_pass = user_pass
        # Get unit number for account
        self.units = self.get_info_by_command(GET_UNITS, None)
        print(f"Found {len(self.units)} unit{'s' if len(self.units)>1 else ''} associated with account: {self.user_name}")


    def get_info_by_command(self, command_name, unit_number, additional_args=None):
        # Fetch data from cloud
        payload = {'commandname': command_name,
                   'format': data_format,
                   'user': self.user_name,
                   'pass': self.user_pass,
                   'unitnumber': unit_number}

        response = requests.get(url, params=payload)

        # Check if response is good
        if response.status_code != 200:
            print(f"Error fetching information, status code {response.status_code}. Check credentials and try again.")
            sys.exit(0)

        zero_string_result = response.text

        # Load json format dict
        zero_dict_result = json.loads(zero_string_result)
        return zero_dict_result


    def scan_for_new_diagnostic_packets(self, unit_number, scan_interval_s):
        previous_diagnostic_packet = None
        # Loop through and look for new diagnosti packets
        while(1):
            diagnostics_packet = z1.get_info_by_command(GET_LAST_TRANSMIT, unit_number, None)

            # Check last received packet time against latest and see if new
            if previous_diagnostic_packet:
                if previous_diagnostic_packet['datetime_actual'] != diagnostics_packet[0]['datetime_actual']:
                    previous_diagnostic_packet = diagnostics_packet[0]
                    # Check out objects in our dict
                    for item in diagnostics_packet[0]:
                        print(f"  {item}: {diagnostics_packet[0][item]}")
            time.sleep(20)



if __name__ == "__main__":

    # Example usage:
    print("\nWelcome to the non-official Zero Motorcycle cloud API interface tool")
    print("This menu will guide you through the example usage")
    print("\nFirst, enter your login information for your zero account")
    user_name = input("Username (email): ")
    user_pass = getpass("Password: ")

    # Create interface object with username and pass
    z1 = ZeroCloudInterface(user_name, user_pass)

    if len(z1.units)>1:
        print("Select which you would like to use:")
        index = 1
        for unit in z1.units:
            print(f"{index}. VIN: {unit['name']}")
        response = input(f"Select which unit (1-{len(z1.units)}): ")
        unit_number  = z1.units[int(response)-1]['unitnumber']
    else:
        unit_number  = z1.units[0]['unitnumber']

    # Create menu:
    # Loop through options
    print(command_list[1])
    while(1):
        print("\n#### MAIN MENU ####")
        print("Available commands:")
        index = 1
        for command in command_list:
            print(f"{index}. {command}")
            index += 1
        command_index = 0
        while command_index < 1 or command_index > len(command_list):
            command_index = int(input(f"\nSelect command (1-{len(command_list)}): "))

        args = None
        if command_list[command_index-1] == GET_HISTORY:
            print("Start and end date required for get history command. Note: 2 day max span.")
            start_date = input("Input start date for history (Format: YYYYMMDD): ")
            end_date = input("Input end date for history (Format: YYYYMMDD): ")
            args = f" -d start={start_date} -d end={end_date}"
        print(f"Command: {command_list[command_index-1]}, unit number: {unit_number}, args: {args}")
        print(z1.get_info_by_command(command_list[command_index-1], unit_number, args))

        print("\nDone, returning to menu")

    # Scan continuously for new diagnostics
    z1.scan_for_new_diagnostic_packets(unit_number, 10)
