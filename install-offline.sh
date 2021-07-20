#!/bin/bash

read -p "Install 123\\SmartBMS to Thingspeak? [Y to proceed]" -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]
then
	python3 -m pip install -e .

	if [ ! -f .env.installed ]
	then
		cp .env.example .env.installed
	fi

	cp ./lib/systemd/system/smartbms.service /lib/systemd/system/smartbms.service
	chmod 644 /lib/systemd/system/smartbms.service

	systemctl daemon-reload
	systemctl enable smartbms.service
	systemctl start smartbms.services
fi