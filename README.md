Smart Home Menu for snom phones
===============================

Python code for snom.io phone D375 that was shown at CeBit 2016

Scope of menu
-------------
* States of **Homematic heater control** (current temperature, set temperature, valve state, battery state, mode)
* States of **Homematic plug** (on/off, power, voltage, current, frequency)
* Switching of Homematic plug
* State of **Homematic window contact**
* **HUE lamp** switching
* Room overview
* Show **webcam pictures**
* **Weather** infos (currently: Berlin)
* Show **RSS news feed** (currently: www.heise.de)
* State of **Raspberry Pi** (GPU temperature, flash size, RAM size)
* Show phone states per color of HUE lamps (per Action URL)
* Display the lamp and switch state over the function key LED's 
* The strings in german / Deutsch! 


Required hardware
-----------------

* **snom io phone** (recommend: snom D375)
* **Raspberry Pi** (recommend: Raspberry Pi 2 B or Raspberry Pi 3 B)
* **Philips Hue** bridge with 3 RGB lamps
* **Homematic** Central Control Unit like CCU2 with:
 * Homematic Window Sensor like HM-Sec-SCo)
 * Homematic Radiator Thermostat (HM-CC-RT-DN)
 * Homematic Switch Actuator with power metering (HM-ES-PWSw1-Pl)
 * Homematic Temperature/Humidity Sensor like HM-WDS10-TH-O
* **IP-Webcam** and/or Raspberry Pi camera


Installation
------------

**On a Raspberry Pi:**
* Install the image with "RASPBIAN JESSIE LITE" from https://www.raspberrypi.org/downloads/raspbian/ (The original Raspberry Pi from CeBit 2016 used the Image from https://kerberos.io/)
* Run the Raspberry Pi Configuration Tool:
```
sudo raspi-config 
```
* Go to this points:
 * "Expand Filesystem"
 * "Change User Password"
 * "Internationalisation Options" ==> "Change Timezone"
* Reboot:
```
sudo reboot
```
* Install webserver like *lighttpd* 
```
sudo apt-get update
sudo apt-get install lighttpd
```
* Download icons: 
 * Download the openHAB "Runtime core" from http://www.openhab.org/getting-started/downloads.html
 * Unpack the file *distribution-1.8.2-runtime.zip*
 * Copy the PNG files from openHAB Runtime directory *webapps/images/* to directory */var/www/html/icons/* 
* Install Git:
```
sudo apt-get install git  
```
* Copy the files from the repository to the home directory:
```
git clone https://github.com/anthal/snom_smarthome
```
* Install PIP (Python package manager):
```
sudo apt-get install python-pip 
```
* Install miscellaneous Python packages:
```
sudo apt-get install python-dev  
sudo pip install simplejson
sudo pip install phue
sudo pip install psutil
sudo pip install feedparser
sudo pip install pyowm
```
 
 
Configuration
-------------

**On a Raspberry Pi:**

* Go in directory */home/pi/snom_smarthome/CeBit2016*
* Set the execute bits:
```
chmod +x *.py
chmod +x *.sh
```
* Adapt in *conf.py*:
 * **server_ip** to the IP address of your Raspberry Pi:
```
server_ip = '172.20.4.117'
```
 * **homematic_ip** to the IP address of your Homematic CCU:
```
homematic_ip = '172.20.4.110'
```
 * **hue_ip** to the IP address of your Philips Hue bridge:
```
config['hue_ip'] = '172.20.4.113'
```
 * **cam1_url** to the URL of your IP Webcam for picture:
```
config['cam1_url'] = 'http://admin:admin@172.20.4.111/tmpfs/auto.jpg'
config['cam2_url'] = 'http://admin:admin@172.20.4.112/tmpfs/auto.jpg'
```
 * **my_owm_api_key** get key from http://openweathermap.org/appid:
```
config['my_owm_api_key'] = '11111111111111111111111111111'
```
 * **city** the city for weather values:
```
config['city'] = 'Berlin,ger'
```
 * Change the addresses to your Homematic devices:
```
########################### Homematic ###########################
# Sockets:
config['addr_wz_socket1'] = 'LEQ4272335'
config['addr_az_socket1'] = 'LEQ4272349'
config['addr_sz_socket1'] = 'LEQ4272278'
# Heizungssteller (Thermostat):
config['addr_wz_heating1'] = 'MEQ4797228'
config['addr_sz_heating1'] = 'MEQ4797228'
# Temp./ Feuchte Sensor (Temp./ Humidity Sensor):
config['addr_az_sensor1'] = 'MEQ4202864'
# Fensterkontakt (Window Sensor):
config['addr_wz_window1'] = 'MEQ4484674'
```
* Get new data from RSS feed:
```
python get_rss.py
```
* Start main script:
```
python main
```
* Press the configuration key on the Philips Hue Bridge
* Crontab (crontab -e):
 * You can use the script *start_main.sh* for start per crontab and the script *get_rss.py* to update the RSS feed per crontab:
```
* * * * * /home/pi/snom_smarthome/CeBit2016/start_main.sh
0 * * * * /home/pi/snom_smarthome/CeBit2016/get_rss.py
```

**On snom phone:**

* WEB GUI: "Function Keys" -key like **SNOM/CLOUD** / Type: "Action URL": "[http://IP_addr_of_Rasperry_Pi]:8083"
* Setting on snom phone:
```
dkey_snom=url http://172.20.4.4:8083/
```
* Action URL Settings on the snom phones:
```
action_incoming_url=http://IP_addr_of_Raspberry_Pi:8083/hue/1/4
action_offhook_url=http://IP_addr_of_Raspberry_Pi:8083/hue/1/2
action_onhook_url=http://IP_addr_of_Raspberry_Pi:8083/hue/1/3
action_missed_url=http://IP_addr_of_Raspberry_Pi:8083/hue/1/5
action_connected_url=http://IP_addr_of_Raspberry_Pi:8083/hue/1/2
```

**HUE lamps** 
* URL for HUE lamps (without menu): http://[IP Raspberry Pi]:8083/hue/[channel]/[color]
 * Channel: 1 – 3 (lamp 1 (WZ), 2 (AZ), 3 (SZ) ) 
 * Color: 0 – off, 1 – on, 2 – daylight, 3 – warmwhite, 4 – red, 5 – blue


Using
----- 

* Press the configured key of the snom phone like **SNOM/CLOUD**
* Use the keys **UP** and **DOWN** to navigate to the menu


Problem solving
---------------

* If the XML menus no longer respond properly in the phone or wrong menu items selects, then reboot phone.
* If the HUE lights do not function, press on the Hue bridge the large central button


