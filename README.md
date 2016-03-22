Smart Home Menu for snom phones
===============================

Python code for snom.io phone D375 that was shown at the CeBit 2016

Scope of menu
-------------
* States of Homematic heter control (actual temperature, set temperature, valve state, battery state, mode)
* States of Homematic plug (on/off, power, voltage, current, frequency)
* Switching of Homematic plug
* State of Homematic window contact
* HUE lamp switching
* Room overview
* Show webcam pictures
* Weather infos (currently: Berlin)
* RSS feed new (currently: www.heise.de)
* State of Raspberry Pi (GPU temperature, flash size, RAM size)

Install
-------

**On a Raspberry Pi:**

 1. Install image with "RASPBIAN JESSIE LITE" from https://www.raspberrypi.org/downloads/raspbian/ 
 2. Install webserver like *lighttpd* 
3. Download icons from openhab (http://www.openhab.org/getting-started/downloads.html => "Runtime core", directory *webapps\images\*) and copy to directory */var/www/icons/* 
4. Copy the files from this repository in a user directory like */home/pi/python/snom.io/*  
5. On crontab:
```
* * * * * /home/pi/python/snom/start_main.sh
0 * * * * /home/pi/python/snom/get_rss.sh
```

** On snom phone **

6. WEB GUI: "Function Keys" -key like "SNOM/CLOUD" / Type: "Action URL": "http://<IP addr. of Rasperry Pi>:8083"
 


