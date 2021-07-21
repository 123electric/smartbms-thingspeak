# License
- MIT
- No offical support

# Description
This software creates a Linux service that reads the 123\SmartBMS data via a serial port and uploads it to Thingspeak.
It is automatically started when the Raspberry Pi is booted.
You can connect as many BMS instances as you want. Each 123\SmartBMS needs it's own Thingspeak channel.

# Requirements
- One BMS to USB cable for every battery pack. This cable received the BMS data from the End Board and creates a virtual COM port.
- A Raspberry Pi with internet connection
- A Thingspeak account

# Installation
1. Download install.sh on your Raspberry Pi.
2. If you are working on the Raspberry Pi via a GUI, open a terminal. Go to the location where the script is located. Example: if you have the install script downloaded to **\home\pi**, type: **cd \home\pi**
3. Now execute the script with the following command: **sudo bash install.sh** - this will run the installer with all rights needed. The installer will download all required files from Github and install them under **\home\pi\smartbms_thingspeak**
4. During the installation, it will ask for the port where the BMS is connected to. In many cases, this is **/dev/ttyUSB0** If you have multiple BMS, separate them with a space.
5. After this, it will ask for the Thingspeak channel key. Enter the channel key of the channel where you want the data to be uploaded to. If you have multiple BMS connections, enter one channel key per BMS port and separate with a space.

The system is now configured and will upload the BMS data every minute.

# Changing configuration
If you ever need to change or add a port and/or thingspeak key, open the terminal or SSH and change the **.env.installed** file in **/home/pi/smartbms_thingspeak**
You can use your favorite text editor for this. Make sure to edit with superuser privileges.
The following commands will open the file with a text editor:
```
sudo nano /home/pi/smartbms_thingspeak/.env.installed
```

# Notes
If you want to check if the service is running fine without any errors, please open a terminal or SSH and use the following command:
```
systemctl status smartbms
```
The errors should be self explanatory. If there are no errors, you should only see the message that the values are updated every minute.
If you get any strange errors, please plug out the USB from the Raspberry Pi, plug it back in and reboot.
