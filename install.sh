#!/bin/bash

INSTALL_DIR="/home/pi/smartbms_thingspeak"

if [ "$(whoami)" != root ]
then
  echo "Please run as root. Example: sudo bash install.sh"
  exit 1
fi

read -p "Install 123\\SmartBMS to Thingspeak? [Y to proceed]" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
	then
	if [ -d "$INSTALL_DIR" ]
	then
		echo "Cannot install, directory ${INSTALL_DIR} already exists..."
		exit
	fi
	echo "Downloading..."

	wget https://github.com/123electric/smartbms-thingspeak/archive/main.zip
	unzip main.zip
	rm main.zip
	systemctl is-active --quiet smartbms.service && systemctl stop smartbms.service
	mv smartbms-thingspeak-main "${INSTALL_DIR}"
	python3 -m venv ${INSTALL_DIR}/.venv
	source ${INSTALL_DIR}/.venv/bin/activate
	python3 -m pip install -e "${INSTALL_DIR}"
	
	echo -e "\r\n"
	read -p "Enter the port the 123\\SmartBMS is connected to [leave empty for /dev/ttyUSB0]: " SERIAL_PORT
	SERIAL_PORT=${SERIAL_PORT:-/dev/ttyUSB0}
	read -p "Enter the Thingspeak channel key: " THINGSPEAK_KEY
	cp "${INSTALL_DIR}/.env.example" "${INSTALL_DIR}/.env.installed"
	echo -e "\nSERIAL_PORT=${SERIAL_PORT}" >> ${INSTALL_DIR}/.env.installed
	echo "THINGSPEAK_KEY=${THINGSPEAK_KEY}" >>  ${INSTALL_DIR}/.env.installed

	cp "${INSTALL_DIR}/lib/systemd/system/smartbms.service" /lib/systemd/system/smartbms.service
	chmod 644 /lib/systemd/system/smartbms.service

	systemctl daemon-reload
	systemctl enable smartbms.service
	systemctl start smartbms.service
	echo "Installation finished"
fi
