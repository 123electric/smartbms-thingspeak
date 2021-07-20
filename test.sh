#!/bin/bash
read -p "\rEnter the port the 123\\SmartBMS is connected to [leave empty for /dev/ttyUSB0]: " port
port=${port:-/dev/ttyUSB0}
read -p "\rEnter the Thingspeak channel key: " thingspeak_key
echo "${thingspeak_key}"