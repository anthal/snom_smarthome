Smart Home Menu for snom phones
===============================

Python code for snom.io phone D375 that was shown at the CeBit 2016

Scope of menu
-------------
* States of **Homematic heater control** (actual temperature, set temperature, valve state, battery state, mode)
* States of **Homematic plug** (on/off, power, voltage, current, frequency)
* Switching of Homematic plug
* State of **Homematic window contact**
* **HUE lamp** switching
* Room overview
* Show **webcam pictures**
* **Weather** infos (currently: Berlin, since middle March is the Yahoo service not available)
* **RSS feed** news (currently: www.heise.de)
* State of **Raspberry Pi** (GPU temperature, flash size, RAM size)


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


Install
-------

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
 * Change the addresses to your Homematic devices:
```
########################### Homematic ###########################
# Sockets:
config['addr_wz_socket1'] = 'LEQ4272335'
config['addr_az_socket1'] = 'LEQ4272349'
config['addr_sz_socket1'] = 'LEQ4272278'
# Heizungssteller:
config['addr_wz_heating1'] = 'MEQ4797228'
config['addr_sz_heating1'] = 'MEQ4797228'
# Temp./ Feuchte Sensor:
config['addr_az_sensor1'] = 'MEQ4202864'
# Fensterkontakt:
config['addr_wz_window1'] = 'MEQ4484674'
```
* Get new datas from RSS feed:
```
python get_rss.py
```
* Start main script:
```
python main
```
* Press the configuration key on the Philips Hue Bridge
* Crontab (crontab -e):
 * You can use the script *start_main.sh* for start per crontab:
```
* * * * * /home/pi/snom_smarthome/CeBit2016/start_main.sh
```
 * You can use the script *get_rss.py* for update the RSS feed per crontab:
```
0 * * * * /home/pi/snom_smarthome/CeBit2016/get_rss.py
```

**On snom phone:**

 * WEB GUI: "Function Keys" -key like **SNOM/CLOUD** / Type: "Action URL": "[http://IP_addr_of_Rasperry_Pi]:8083"
 * Setting on snom phone:
```
dkey_snom=url http://172.20.4.4:8083/
```

Using
----- 

* Press the configured key of the snom phone like **SNOM/CLOUD**
* Use the keys **UP** and **DOWN** to navigate to the menu
* The menu **Wetter** used a Yahoo service, this service is at middle of March 2016 out of order! 




