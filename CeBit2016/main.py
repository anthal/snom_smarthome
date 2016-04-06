#!/usr/bin/python2
# -*- coding: utf8 -*-

#
# History:
# 05.02.2016  v0.2  - initial release Homeautomatisierung
# 14.02.2016  v0.21 - Homeautomatisierung for CeBit

# 3 Raeume:
# 0 - Wohnzimmer WZ
# 1 - Arbeitszimmer AZ
# 2 - Schlafzimmer SZ

# Pro Raum:
# - Steckdose mit Leistungsmessung
# - Heizungssteller mit Temp. Sensor
# - Fensterkontakt

# Menue Aufruf von externem Client:
# http://192.168.111.119/minibrowser.htm?url=192.168.110.9:8083/light
#

## Python Libs:
import BaseHTTPServer
# Install BaseHttpServer: ist in Python2 enthalten
import sys
import time
import pickle
import urllib
import socket
from xml.dom.minidom import *
import xmlrpclib
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import simplejson
from urllib import unquote
from phue import Bridge

## snom libs:
import conf
import commands
from snom import SnomXML
from http import ThreadingServer
import rapi_system
import RPi.GPIO as GPIO

# pacman -S python2-pip
# pip2 install simplejson

global config
config=conf.config()

# global picture 

icons_url = config['icons_url'] 

# import json
import urllib2

snomXML = SnomXML()

# Hue-Helligkeit = 0-254:
command = commands.Commands(config['brightness'])

system = rapi_system.RaPi_System()

# GPIO Nummern:
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

###############################################################################
class WebServer(BaseHTTPServer.BaseHTTPRequestHandler):
    '''
    Webserver Class
    '''
    
    def do_GET(self):
        snom = Snom()
        # snom = SnomXML()
        url=self.path

        # print("Picture (GET): " + snom.picture)
        # print("url: '" + url + "'") 
        writeString = ""
        self.send_response(200)
        self.send_header("Content-type","text/xml")

        # Remove all right of ask sign (?) :
        # url: '/temps?creation=2016-02-04T22%3A53%3A48Z'    
        url_list = url.split('?')
        url = url_list[0]
        # print("url: '" + url + "'") 
        url_list2 = url.split('_')
        url2 = url_list2[0]
        # print("url2: '" + url2 + "'") 
        url_list3 = url.split('/')
        print(url_list3)
        
        # Root, Home:
        if url=='/':
            writeString = SnomXML.SnomIPHeader() + snom.index()
        elif url2=='/alarmcam':
            writeString = SnomXML.SnomIPHeader() + snom.alarmcam(snomXML.picture)
        elif url=='/rooms':
            writeString = SnomXML.SnomIPHeader()+snom.rooms()
        elif url=='/windows':
            writeString = SnomXML.SnomIPHeader()+snom.windows()
            
        elif url=='/wz':
            writeString = SnomXML.SnomIPHeader()+snom.room_menu("Wohnzimmer", "wz")
        elif url=='/az':
            writeString = SnomXML.SnomIPHeader()+snom.room_menu("Arbeitszimmer", "az")
        elif url=='/sz':
            writeString = SnomXML.SnomIPHeader()+snom.room_menu("Schlafzimmer", "sz")
            
        elif url=='/status_wz':
            writeString = SnomXML.SnomIPHeader()+snom.room_status("Wohnzimmer", "wz")
        elif url=='/status_az':
            writeString = SnomXML.SnomIPHeader()+snom.room_status("Arbeitszimmer", "az")
        elif url=='/status_sz':
            writeString = SnomXML.SnomIPHeader()+snom.room_status("Schlafzimmer", "sz")
        
        ## Light:    
        elif url=='/light':
            writeString = SnomXML.SnomIPHeader()+snom.light([])
        elif url=='/light/wz':
            writeString = SnomXML.SnomIPHeader()+snom.light_room("Wohnzimmer", "wz")
        elif url=='/light/az':
            writeString = SnomXML.SnomIPHeader()+snom.light_room("Arbeitszimmer", "az")
        elif url=='/light/sz':
            writeString = SnomXML.SnomIPHeader()+snom.light_room("Schlafzimmer", "sz")
        elif url=='/light/all/0':
            command.set_value('light_1_wz', 0)            
            command.set_value('light_1_az', 0)            
            command.set_value('light_1_sz', 0)            
            writeString = SnomXML.SnomIPHeader()+snom.light([])
        elif url=='/light/all/1':
            command.set_value('light_1_wz', 1)            
            command.set_value('light_1_az', 1)            
            command.set_value('light_1_sz', 1)            
            writeString = SnomXML.SnomIPHeader()+snom.light([])
        # elif url=='/light/wz/0':
        # elif url_list3[1] == 'light' and url_list3.len == 3 :
        elif url_list3[1] == 'light' :
            command.set_value('light_1_' + url_list3[2], url_list3[3])            
            writeString = SnomXML.SnomIPHeader()+snom.light([])

        ## Hue Light - Only for Action URL (Settings):    
        elif url_list3[1] == 'hue' :
            command.set_value('hue_' + url_list3[2], url_list3[3])            

        ## Sockets:    
        elif url=='/socket':
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/wz/0':
            # Switch Light_Living_Decke_W     "Deckenlicht WZ Wand"   (Living, Lights)    { homematic="address=IEQ0101017, channel=1, parameter=STATE"}
            command.set_value('state_socket_1_wz', 'false')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/wz/1':
            command.set_value('state_socket_1_wz', 'true')   
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/az/0':
            command.set_value('state_socket_1_az', 'false')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/az/1':
            command.set_value('state_socket_1_az', 'true')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/sz/0':
            command.set_value('state_socket_1_sz', 'false')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/sz/1':
            command.set_value('state_socket_1_sz', 'true')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/all/0':
            command.set_value('state_socket_1_wz', 'false')            
            command.set_value('state_socket_1_az', 'false')            
            command.set_value('state_socket_1_sz', 'false')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/all/1':
            command.set_value('state_socket_1_wz', 'true')            
            command.set_value('state_socket_1_az', 'true')            
            command.set_value('state_socket_1_sz', 'true')            
            writeString = SnomXML.SnomIPHeader()+snom.sockets([])
        elif url=='/socket/wz':
            writeString = SnomXML.SnomIPHeader()+snom.sockets_room("Wohnzimmer", "wz")
        elif url=='/socket/az':
            writeString = SnomXML.SnomIPHeader()+snom.sockets_room("Arbeitszimmer", "az")
        elif url=='/socket/sz':
            writeString = SnomXML.SnomIPHeader()+snom.sockets_room("Schlafzimmer", "sz")

        # Clima    
        elif url=='/temps':
            writeString = SnomXML.SnomIPHeader()+snom.temps()
        elif url=='/all_temp':
            # writeString = SnomXML.SnomIPHeader()+str(snom.get_temp('all','isttemp', 4))
            writeString = SnomXML.SnomIPHeader()+str(snom.get_temp('all', 4))
        elif url=='/wz_temp':
            writeString = SnomXML.SnomIPHeader()+str(snom.get_temp('Wohnzimmer', 4))
        elif url=='/sz_temp':
            writeString = SnomXML.SnomIPHeader()+str(snom.get_temp('Schlafzimmer', 4))
        elif url=='/az_temp':
            writeString = SnomXML.SnomIPHeader()+str(snom.get_temp('Arbeitszimmer', 1))
        elif url=='/webcam':
            writeString = SnomXML.SnomIPHeader()+snom.webcams()
        elif url=='/webcam0':
            writeString = SnomXML.SnomIPHeader()+snom.webcam(0)
        elif url=='/webcam1':
            writeString = SnomXML.SnomIPHeader()+snom.webcam(1)
        elif url=='/webcam2':
            writeString = SnomXML.SnomIPHeader()+snom.webcam(2)
        elif url=='/webcam3':
            writeString = SnomXML.SnomIPHeader()+snom.webcam(3)
        elif url=='/wetter':
            writeString = SnomXML.SnomIPHeader()+snom.wetter()
        elif url=='/rss':
            writeString = SnomXML.SnomIPHeader()+snom.rss()
        elif url[:5]=='/rss_':
            rss_number = url[5:]
            # print(rss_number)
            writeString = SnomXML.SnomIPHeader()+snom.read_rss_content(rss_number)
        elif url=='/heise':
            writeString = SnomXML.SnomIPHeader()+snom.read_rss('Heise')
        elif url=='/tagesspiegel':
            writeString = SnomXML.SnomIPHeader()+snom.read_rss('Tagesspiegel')
        elif url=='/zdf_heute':
            writeString = SnomXML.SnomIPHeader()+snom.read_rss('ZDF-Heute')
        elif url=='/system':
            writeString = SnomXML.SnomIPHeader()+snom.system()

        # get benoetigt zwingend "/led/2-Off" z.b. als Paramter 
        elif url[0:url.rfind('/')]=='/led':
            searchstring=url[url.rfind('/')+1:] # setze searchstring auf parameter (z.b. "2-Off")
            # basic syntaxcheck, could be better..
            led_state=searchstring[searchstring.rfind('-')+1:] # setze searchstring auf parameter (z.b. "Off")
            led_pos=searchstring[:searchstring.rfind('-')] # setze searchstring auf parameter (z.b. "12")
            # print searchstring
            # print led_pos
            # print led_state
            # if len(searchstring)<4 or searchstring[1]!="-":
            if len(searchstring)<4 or len(searchstring)>8:
                writeString = SnomXML.SnomIPHeader()+snom.error("Falsche URL-Syntax!")
                return
            # searchstring uebergeben und ergebnis auf website schreiben
            writeString = SnomXML.SnomIPHeader()+snom.led(led_pos, led_state)
        else:
            writeString = SnomXML.SnomIPHeader()+snom.error("Server: URL not Found!")
        self.send_header("Content-length",len(writeString))
        self.end_headers()
        self.wfile.write(writeString)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return

    
    def do_POST(self):
        content_len = int(self.headers.getheader('content-length', 0))
        post_body = self.rfile.read(content_len)
        test_data = simplejson.loads(post_body)
        # print "post_body(%s)" % (test_data)
        snomXML.picture = test_data['pathToImage']
        print("ALARM ! - Picture (POST): " + snomXML.picture)
        timestamp = str(time.time())
        f = urllib2.urlopen(config['phone_url'] + '/minibrowser.htm?url=' + config['base_url'] + '/alarmcam_'+ timestamp)
        # return SimpleHTTPRequestHandler.do_POST(self)
        GPIO.output(pins[3], GPIO.LOW)
        time.sleep(0.3)
        # LED OFF:
        GPIO.output(pins[3], GPIO.HIGH)

        return 

        
###############################################################################    
class Snom:
    '''
    Menu Class
    '''
    
    def led(self,number,state):
        return SnomXML.SnomIPPhoneLED(number=number, state=state)

    def index(self):
        '''
        Main Manu:    
        '''
        MenuItems=[]
        # MenuItems.append((icon, 'Sicherheit',config['base_url']+'secure'))
        icon = icons_url + "firstfloor.png"
        MenuItems.append((icon, 'Räume',config['base_url']+'rooms'))
        icon = icons_url + "slider-50.png"
        MenuItems.append((icon, 'Licht',config['base_url']+'light'))
        icon = icons_url + "socket.png"
        MenuItems.append((icon, 'Steckdosen',config['base_url']+'socket'))
        icon = icons_url + "temperature-max.png"
        MenuItems.append((icon, 'Heizung - Klima',config['base_url']+'temps'))
        icon = icons_url + "contact-open.png"
        MenuItems.append((icon, 'Fenster',config['base_url']+'windows'))
        # MenuItems.append((icon, 'Multimedia',config['base_url']+'media'))
        # MenuItems.append((icon, 'Hilfe',config['base_url']+'help'))
        icon = icons_url + "camera.png"
        MenuItems.append((icon, 'Webcams',config['base_url']+'webcam'))
        icon = icons_url + "sun_clouds.png"
        MenuItems.append((icon, 'Wetter',config['base_url']+'wetter'))
        icon = icons_url + "info.png"
        MenuItems.append((icon, 'RSS-Feed',config['base_url']+'rss'))
        # MenuItems.append((icon, 'Szenen',config['base_url']+'szenen'))
        icon = icons_url + "computer.png"
        MenuItems.append((icon, 'System',config['base_url']+'system'))
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Exit','snom://mb_exit'))
        # print MenuItems
        return SnomXML.SnomIPPhoneMenuIcon(Title="Smart Home Status Demo", MenuItems = MenuItems)
    
    
    def rooms(self,):
        '''
        Room Menu:     
        '''
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        icon = icons_url + "sofa.png"
        MenuItems.append((icon, 'Wohnzimmer',config['base_url']+'wz'))
        icon = icons_url + "office.png"
        MenuItems.append((icon, 'Arbeitszimmer',config['base_url']+'az'))
        icon = icons_url + "bedroom.png"
        MenuItems.append((icon, 'Schlafzimmer',config['base_url']+'sz'))
        # icon = icons_url + "child1.png"
        # MenuItems.append((icon, 'Kinderzimmer',config['base_url']+'sz'))
        # icon = icons_url + "kitchen.png"
        # MenuItems.append((icon, 'Küche',config['base_url']+'kueche'))
        # icon = icons_url + "bath.png"
        # MenuItems.append((icon, 'Bad',config['base_url']+'bad'))
        # icon = icons_url + "corridor.png"
        # MenuItems.append((icon, 'Flur',config['base_url']+'flur'))
        return SnomXML.SnomIPPhoneMenuIcon(Title = "Zimmer", MenuItems = MenuItems)

        
    def room_menu(self, room, room_code):
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        icon = icons_url + "line.png"
        MenuItems.append((icon, 'Status',config['base_url'] + 'status_' + room_code))
        icon = icons_url + "temperature-max.png"
        MenuItems.append((icon, 'Heizung - Klima',config['base_url'] + room_code + '_temp'))
        icon = icons_url + "socket.png"
        MenuItems.append((icon, 'Steckdose',config['base_url'] + 'socket/' + room_code))
        # icon = icons_url + "slider-50.png"
        icon = icons_url + "hue-50.png"
        MenuItems.append((icon, 'Licht',config['base_url'] + 'light/' + room_code))
        return SnomXML.SnomIPPhoneMenuIcon(Title = room, MenuItems = MenuItems)
    
    
    def light(self, menu_items):
        '''
        /light
        '''
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append(('1', 'off', icon, 'Hauptmenü',config['base_url']+'/'))
        # Licht WZ:
        state = command.get_value('light_1_wz')
        if state :
            text = "[ON]"
            icon = icons_url + "hue-on.png"
            ledstate = "On"
        else:
            text = "[OFF]"
            icon = icons_url + "hue-off.png"
            ledstate = "Off"
        # print(text)
        MenuItems.append(('5', ledstate, icon, 'Licht Wohnzimmer: ' + text, config['base_url'] + 'light/wz'))
        # Licht AZ:
        state = command.get_value('light_1_az')
        # print("state: " + str(state))
        if state :
            text = "[ON]"
            icon = icons_url + "hue-on.png"
            ledstate = "On"
        else:
            text = "[OFF]"
            icon = icons_url + "hue-off.png"
            ledstate = "Off"
        MenuItems.append(('6', ledstate, icon, 'Licht Arbeitszimmer: ' + text, config['base_url'] + 'light/az'))
        # Licht SZ:
        state = command.get_value('light_1_sz')
        if state :
            text = "[ON]"
            icon = icons_url + "hue-on.png"
            ledstate = "On"
        else:
            text = "[OFF]"
            icon = icons_url + "hue-off.png"
            ledstate = "Off"
        MenuItems.append(('7', ledstate, icon, 'Licht Schlafzimmer: ' + text, config['base_url'] + 'light/sz'))
        icon = icons_url + "hue-off.png"
        MenuItems.append(('1', 'off', icon, 'Alles Aus',config['base_url']+'light/all/0'))
        icon = icons_url + "hue-on.png"
        MenuItems.append(('1', 'off', icon, 'Alles An',config['base_url']+'light/all/1'))
        # print MenuItems
        # <Led number="2">On</Led>
        return SnomXML.SnomIPPhoneMenuIconLED(Title = "Licht-Status", MenuItems = MenuItems)

        
    def light_room(self, room, room_code):
        '''
        Hue
        '''
        MenuItems=[]

        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url'] + '/'))
        
        state = command.get_value('light_1_' + room_code)
        # print("State: " + str(state))    
        if state :
            text= "ON"
            icon = icons_url + "hue-on.png"
        else:
            text= "OFF"
            icon = icons_url + "hue-off.png"
        MenuItems.append((icon, 'Lichtstatus: ' + text, config['base_url'] + 'light'))
        if state :
            icon = icons_url + "hue-off.png"
            MenuItems.append((icon, 'Schalte Licht &#8594; OFF', config['base_url'] + 'light/' + room_code + '/0'))
            MenuItems.append((icon, 'Schalte Licht &#8594; Tageslicht' , config['base_url'] + 'light/' + room_code + '/2'))
            MenuItems.append((icon, 'Schalte Licht &#8594; Glühlampe' , config['base_url'] + 'light/' + room_code + '/3'))
            MenuItems.append((icon, 'Schalte Licht &#8594; Pink' , config['base_url'] + 'light/' + room_code + '/4'))
            MenuItems.append((icon, 'Schalte Licht &#8594; Blau' , config['base_url'] + 'light/' + room_code + '/5'))
        else:    
            icon = icons_url + "hue-on.png"
            MenuItems.append((icon, 'Schalte Licht &#8594; ON' , config['base_url'] + 'light/' + room_code + '/1'))

        return SnomXML.SnomIPPhoneMenuIcon(Title="Licht " + room, MenuItems = MenuItems)

  
    def sockets(self, menu_items):
        MenuItems=[]
        
        icon = icons_url + "_up.png"
        MenuItems.append(('1', 'off', icon, 'Hauptmenü',config['base_url']+'/'))
        
        # Steckdose WZ:
        state = command.get_value('state_socket_1_wz')
        if state :
            text = "[ON]"
            icon = icons_url + "socket-on.png"
            ledstate = "On"
        else:
            text = "[OFF]"
            icon = icons_url + "socket-off.png"
            ledstate = "Off"
        # print(text)
        MenuItems.append(('11', ledstate, icon, 'Steckdose Wohnzimmer: ' + text, config['base_url'] + 'socket/wz'))
        
        # Steckdose AZ:
        state = command.get_value('state_socket_1_az')
        # print("state: " + str(state))
        if state :
            text = "[ON]"
            icon = icons_url + "socket-on.png"
            ledstate = "On"
        else:
            text = "[OFF]"
            icon = icons_url + "socket-off.png"
            ledstate = "Off"
        MenuItems.append(('12', ledstate, icon, 'Steckdose Arbeitszimmer: ' + text, config['base_url'] + 'socket/az'))
        
        # Steckdose SZ:
        state = command.get_value('state_socket_1_sz')
        if state :
            text = "[ON]"
            icon = icons_url + "socket-on.png"
            ledstate = "On"
        else:
            text = "[OFF]"
            icon = icons_url + "socket-off.png"
            ledstate = "Off"
        MenuItems.append(('13', ledstate, icon, 'Steckdose Schlafzimmer: ' + text, config['base_url'] + 'socket/sz'))
        
        icon = icons_url + "socket-off.png"
        MenuItems.append(('1', 'off', icon, 'Alles Aus',config['base_url']+'socket/all/0'))
        icon = icons_url + "socket-on.png"
        MenuItems.append(('1', 'off', icon, 'Alles An',config['base_url']+'socket/all/1'))
        # print MenuItems
        # <Led number="2">On</Led>
        return SnomXML.SnomIPPhoneMenuIconLED(Title = "Steckdosen-Status", MenuItems = MenuItems)

        
    def sockets_room(self, room, room_code):
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        state = command.get_value('state_socket_1_' + room_code)
        power = command.get_value('power_socket_1_' + room_code)
        energycounter = command.get_value('energycounter_socket_1_' + room_code)
        current = command.get_value('current_socket_1_' + room_code)
        voltage = command.get_value('voltage_socket_1_' + room_code)
        frequency = command.get_value('frequency_socket_1_' + room_code)
        print("State: " + str(state))    
        if state :
            text= "ON"
            icon = icons_url + "socket-on.png"
        else:
            text= "OFF"
            icon = icons_url + "socket-off.png"
        MenuItems.append((icon, 'Steckdosenstatus: ' + text, config['base_url']+'socket'))
        if state :
            icon = icons_url + "socket-off.png"
            MenuItems.append((icon, 'Schalte Steckdose &#8594; OFF', config['base_url'] + 'socket/' + room_code + '/0'))
        else:    
            icon = icons_url + "socket-on.png"
            MenuItems.append((icon, 'Schalte Steckdose &#8594; ON' , config['base_url'] + 'socket/' + room_code + '/1'))
        # Power:
        icon = icons_url + "energy.png"  
        text = str(power)
        MenuItems.append((icon, 'Leistungsaufnahme: ' + text + ' W', config['base_url'] + 'socket' ))
        text = str(energycounter)
        MenuItems.append((icon, 'Energie-Zähler: ' + text + ' Wh', config['base_url'] + 'socket' ))
        text = str(voltage)
        MenuItems.append((icon, 'Netzspannung: ' + text + ' V', config['base_url'] + 'socket' ))
        text = str(current)
        MenuItems.append((icon, 'Stromaufnahme: ' + text + ' mA', config['base_url'] + 'socket' ))
        text = str(frequency)
        MenuItems.append((icon, 'Netzfrequenz: ' + text + ' Hz', config['base_url'] + 'socket' ))
        return SnomXML.SnomIPPhoneMenuIcon(Title="Steckdose " + room, MenuItems = MenuItems)

  
    # Fenster:  
    def windows(self):
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        # Wohnzimmer:
        state = command.get_value('window1_wz')
        # print("state: " + str(state))
        if state:
            text = 'Offen'
            icon = icons_url + "contact-open.png"
        # if state == 1:
            # text = 'Gekippt'
            # icon = icons_url + "contact-ajar.png"
        # if state == 2:
        else:
            text = 'Zu'
            icon = icons_url + "contact-closed.png"
            # text = 'Unbekannt'
            # icon = icons_url + "help.png"
        MenuItems.append((icon, 'Wohnzimmer: ' + text, config['base_url'] + '/'))
        return SnomXML.SnomIPPhoneMenuIcon(Title="Status der Fenster",MenuItems=MenuItems)
    
    
    def room_status(self, room, room_code):
        # room='Arbeitszimmer'
        text=''
        MenuItems=[]
        room_status = 1
        
        # Licht:
        state = command.get_value( 'light_1_' + room_code)
        if state:
          text= "ON"
          icon = icons_url + "hue-on.png"
        else:
          text= "OFF"
          icon = icons_url + "hue-off.png"
        MenuItems.append((icon, 'Licht: '+text,config['base_url'] + 'light/' + room_code))

        # Licht:
        state = command.get_value( 'state_socket_1_' + room_code)
        if state:
          text= "ON"
          icon = icons_url + "socket-on.png"
        else:
          text= "OFF"
          icon = icons_url + "socket-off.png"
        MenuItems.append((icon, 'Steckdose: '+text,config['base_url'] + 'socket/' + room_code))
        
        # Fenster:
        # snom:
        if room_status == 1 :
            state = command.get_value('window1_wz')
            if state == 0:
                text = 'geschlossen'
                icon = icons_url + "contact-closed.png"
                # if state == 1:
                  # text = 'gekippt'
                  # icon = icons_url + "contact-ajar.png"
                # if state == 2:
            if state > 0:
                text = 'offen'
                icon = icons_url + "contact-open.png"
            # MenuItems.append((icon, 'Fenster: ' + text, config['base_url'] + 'status_' + room_code))
            MenuItems.append((icon, 'Fenster: ' + text, config['base_url'] + room_code))
        return SnomXML.SnomIPPhoneMenuIcon(Title = "Status " + room, MenuItems = MenuItems)
    
    
    # Menu Klima
    def temps(self):
        # print("  function temps") 
        MenuItems = []
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü', config['base_url'] + '/'))
        icon = icons_url + "temperature-max.png"
        MenuItems.append((icon, 'Alle Zimmer', config['base_url'] + 'all_temp'))
        icon = icons_url + "sofa.png"
        MenuItems.append((icon, 'Wohnzimmer', config['base_url'] + 'wz_temp'))
        icon = icons_url + "office.png"
        MenuItems.append((icon, 'Arbeitszimmer', config['base_url'] + 'az_temp'))
        # icon = icons_url + "bedroom.png"
        # MenuItems.append((icon, 'Schlafzimmer', config['base_url'] + 'sz_temp'))
        return SnomXML.SnomIPPhoneMenuIcon(Title = "Heizung - Klima", MenuItems = MenuItems)
   
   
    def get_temp(self, room, type):
        '''
        
        :param typ: 1 - alter Heizungssteller, 4 - neuer Heizungssteller
        '''
        print("  function get_temp, room: " + room + ", type: " + str(type)) 
        if room == "all":
          room_nr = 0        
        if room == "Wohnzimmer":
          room_nr = 1
        if room == "Arbeitszimmer":
          room_nr = 2
        if room == "Schlafzimmer":
          room_nr = 3
        print "Daten von Raum-ID: " + str(room_nr)
        text = ''
        if room_nr == 0:
            room = 'Raum-Temperaturen'
            # text= 'date<br/>'
            isttemp = command.get_value('temp_wz')
            text = text + "Wohnzimmer: " + str(isttemp) + "°C<br/>"
            isttemp = command.get_value('temp_az')
            text = text + "Arbeitszimmer: " + str(isttemp) + "°C<br/>"
            # isttemp = command.get_value('temp_sz')
            # text = text + "Schlafzimmer: " + str(isttemp) + "°C<br/>"
        if room_nr == 1 or room_nr == 3:
            isttemp = command.get_value('temp_wz')
            settemp = command.get_value('settemp_wz')
            valve = command.get_value('valve_wz')
            control_mode = command.get_value('controlmode_wz')
            battery = command.get_value('battery_valve1_wz')
            if control_mode == 0 :
                str_control_mode = "Auto "
            if control_mode == 1 :
                str_control_mode = "Manual "
            if control_mode == 2 :
                str_control_mode = "Party "
            if control_mode == 3 :
                str_control_mode = "Boost "
            text = text + "- Ist-Temperatur: " + str(isttemp) + " °C<br/>"
            text = text + "- Soll-Temperatur: " + str(settemp) + " °C<br/>"
            text = text + "- Ventilstatus: " + str(valve) + " %<br/>"
            text = text + "- Klima Control Mode: " + str_control_mode + " <br/>"
            text = text + "- Batterie Spannung: " + str(battery) + " V<br/>"
        if room_nr == 2:
            isttemp = command.get_value('temp_az')
            feuchte = command.get_value('humidity_az')
            text = text + "- Ist-Temperatur: " + str(isttemp) + " °C<br/>"
            text = text + "- Luftfeuchte: " + str(feuchte) + " %<br/>"
        print("Text: " + text) 
        return SnomXML.SnomIPPhoneText(Title="Heizung - Klima " + room, Text = text)

        
    def get_lan_ip(self, ifname):
        ip = socket.gethostbyname(socket.gethostname())
        if ip.startswith("127.") and os.name != "nt":
            # interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0"]
            # for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
            except IOError:
                pass
        return ip

    
    def system(self):
        MenuItems = []
        text=''
        cpu_cores = system.cpu('core_count')[0]
        cpu_temp = system.getGpuTemperature()
        cpu_takt = system.getCpuTakt()
        
        # print(system.get_lan_ip('eth0'))
        mem_free = system.memory('available')
        mem_total = system.memory('total')
        mem_percent = system.memory('percent_free')
        
        disk_free = system.disks('free')
        disk_total = system.disks('total')
        disk_percent = system.disks('percent_free')
        uptime = system.uptime()

        text=text + "CPU-Cores: " + str(cpu_cores) + " with " + str(cpu_takt) + " MHz<br/>"
        text=text + "CPU-Temperatur: " + str(cpu_temp) + " °C<br/>"
        # text=text + "CPU-Last: " + str(cpu_load) + " %<br/>"
        text=text + "RAM (frei): "  + str(mem_free)  + " / " + str(mem_total)  + " MB (" + str(mem_percent)  + "%)<br/>"
        text=text + "Flashdisk (frei): " + str(disk_free) + " / " + str(disk_total) + " GB (" + str(disk_percent) + "%)<br/>"
        text=text + "IP-Adresse: " + system.get_lan_ip('eth0') + " <br/>"
        text=text + "Uptime: " + str(uptime) + " Tage<br/>"
        return SnomXML.SnomIPPhoneText(Title="Serverstatus ", Text=text)

        
    def rss(self):
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        icon = icons_url + "info.png"
        MenuItems.append((icon, 'Heise',config['base_url']+'heise'))
        # MenuItems.append(('Tagesspiegel',config['base_url']+'tagesspiegel'))
        # MenuItems.append(('ZDF Heute',config['base_url']+'zdf_heute'))
        return SnomXML.SnomIPPhoneMenuIcon(Title = "RSS-Feeds", MenuItems = MenuItems)

        
    def read_rss(self, feed):
        MenuItems=[]
        prompt = ""
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        icon = icons_url + "info.png"
        # print("rss_file: " + config['rss_file'])
        try:
            fobj = open(config['rss_file'])
        except:
            print("Dateizugriff fehlgeschlagen!")
            # return SnomXML.SnomIPPhoneText("Dateizugriff fehlgeschlagen!", "ERROR", prompt)
            # sys.exit(0)
            return 1
        itemlist = pickle.load(fobj)    
        fobj.close()    
        # print itemlist
        i = 1
        for line in itemlist:
            rss_headline = line[0].encode('utf-8')
            # print(rss_headline)
            MenuItems.append((icon, rss_headline,config['base_url'] + 'rss_' + str(i) ))
            i = i + 1
        # UTF-8 Encoding:
        rss_content = line[1].encode('utf-8')
        # print(rss_content)
        return SnomXML.SnomIPPhoneMenuIcon(Title = feed + '-Feed' , MenuItems = MenuItems)
        
        
    def read_rss_content(self, feed):
        feed = int(feed) - 1
        prompt = ""
        # print("rss_file: " + config['rss_file'])
        try:
            fobj = open(config['rss_file'])
        except:
            # print "Dateizugriff fehlgeschlagen!"
            return SnomXML.SnomIPPhoneText("Dateizugriff fehlgeschlagen!", "ERROR", prompt)
            sys.exit(0)
        itemlist = pickle.load(fobj)    
        fobj.close()   
        # print itemlist
        # UTF-8 Encoding:
        rss_headline = itemlist[feed][0].encode('utf-8')
        rss_content = itemlist[feed][1].encode('utf-8')
        # print(rss_content)
        return SnomXML.SnomIPPhoneText(rss_content, rss_headline, prompt)
        

    #########################################################################
    def webcams(self):
        MenuItems=[]
        icon = icons_url + "_up.png"
        MenuItems.append((icon, 'Hauptmenü',config['base_url']+'/'))
        icon = icons_url + "camera.png"
        MenuItems.append((icon, 'snom CeBIT 1',config['base_url']+'webcam0'))
        MenuItems.append((icon, 'snom CeBIT 2',config['base_url']+'webcam1'))
        MenuItems.append((icon, 'snom CeBIT Alarmcam',config['base_url'] + 'alarmcam'))
        return SnomXML.SnomIPPhoneMenuIcon(Title="Webcams",MenuItems=MenuItems)

    #########################################################################
    def webcam(self, webcam):
        if webcam == 0:
            picture = config['cam1_url']
        if webcam == 1:
            picture = config['cam2_url']
        # return SnomXML.SnomIPPhoneImageFile(picture, refresh_time, xml_url)
        return SnomXML.SnomIPPhoneImageFile(picture)
       
    #########################################################################
    # Wettervorhersage (Yahoo)
    #
    # Quelle: http://kampis-elektroecke.de/?page_id=3894   
    # Funktioniert leider seut Mitte Maerz nicht mehr so...     
    #########################################################################
    def wetter(self):
        MenuItems=[]
        # writeString = SnomXML.SnomIPHeader()+str(snom.get_temp('all','isttemp'))
        # MenuItems.append((feed, config['base_url']+'rss'))
        # return SnomXML.SnomIPPhoneMenu(Title = feed + "-Feeds", MenuItems = MenuItems)
        wetter_txt = "Das Wetter Heute in Berlin \n "
        prompt = ""

        # Liste fuer den Wetterbericht
        # 1. Dimension = heute, 2. Dimension = naechster Tag
        # 1. Element = Tag, 2. Element = Datum, 3. = Niedrigste Temperatur, 4. Element = Hoechste Temperatur, 5. Element = Wettersituation
        Wetter = [["", "", "", "", ""] , ["", "", "", "", ""]]

        # URL oeffnen und XML Daten einlesen
        # &u=c am Ende fuer Wetter in Grad Celsius
        # https://weather.yahoo.com/deutschland/bundesland-berlin/berlin-638242/#
        Baum = urllib.urlopen('http://weather.yahooapis.com/forecastrss?w=638242&u=c').read()

        # XML Daten parsen und in Baumstruktur anordnen
        Baum = parseString(Baum)

        # Ort einlesen
        Ort = Baum.getElementsByTagName('yweather:location')[0]
        Stadt = Ort.attributes["city"].value
        Land = Ort.attributes["country"].value

        # Datum einlesen
        Datum = Baum.getElementsByTagName('lastBuildDate')[0].firstChild.data 

        # Koordinaten auslesen
        Geo_Lat = Baum.getElementsByTagName('geo:lat')[0].firstChild.data
        Geo_Long = Baum.getElementsByTagName('geo:long')[0].firstChild.data
            
        # Wetterdaten von heute einlesen
        Today = Baum.getElementsByTagName('yweather:condition')[0]

        # Wettertext einlesen
        Wetterlage = Today.attributes["text"].value

        # Temperatur einlesen
        Temperatur = float(Today.attributes["temp"].value)

        # Daten in einer Liste speichern
        for Counter in range(2):
            # Wetterdaten fuer die beiden Tage einlesen
            # Daten einlesen
            Future = Baum.getElementsByTagName('yweather:forecast')[Counter]
            # Daten verarbeiten
            Wetter[Counter][0] = Future.attributes["day"].value
            Wetter[Counter][1] = Future.attributes["date"].value    
            Wetter[Counter][2] = float(Future.attributes["low"].value)  
            Wetter[Counter][3] = float(Future.attributes["high"].value)
            Wetter[Counter][4] = Future.attributes["text"].value

        wetter_txt = "Wetter heute am " + wday2wtag(Wetter[0][0]) + ":<br/> Temp.: " + str(Temperatur) + u"°C<br/> Min.: " + str(Wetter[0][2]) + u"°C, Max.: " + str(Wetter[0][3]) + u"°C<br/>Wettersituation: " + Wetterlage + "<br/> Wetter morgen am " + wday2wtag(Wetter[1][0]) + ":<br/>Temp. Min: " + str(Wetter[1][2]) + u"°C, Max: " + str(Wetter[1][3]) + u"°C<br/>Wetter: " + str(Wetter[1][4])
        wetter_string = u"Wetterbericht für " + Stadt

        # UTF-8 Encoding:
        wetter_string = wetter_string.encode('utf-8')
        wetter_txt = wetter_txt.encode('utf-8')
        
        # print(wetter_string)
        # print(wetter_txt)
        return SnomXML.SnomIPPhoneText(wetter_txt, wetter_string, prompt)
       
       
    def error(self,text,url=""):
        index=[(text,config['base_url']+url)]
        return SnomXML.SnomIPPhoneMenu(Title="Home State",MenuItems=index)

        
    def help(self):
        text= u"Einfach aus dem Menü das Gewünschte wählen"
        # text+="0 = 0-9, "
        return SnomXML.SnomIPPhoneText(Title="Homeautomatisierung", Text=text)
  
    def alarmcam(self, picture):
        '''
        webcam:    
        '''
        MenuItems=[]
        # MenuItems.append((icon, 'System',config['base_url']+'system'))
        # print MenuItems
        
        return SnomXML.SnomIPPhoneImageFile(config['capture_url'] + picture)
  
#########################################################################
#
#########################################################################
def wday2wtag(day):
    wtag = day
    if day == "Mon" :
        wtag = 'Montag'
    if day == "Tue" :
        wtag = 'Dienstag'
    if day == "Wed" :
        wtag = 'Mittwoch'
    if day == "Thu" :
        wtag = 'Donnerstag'
    if day == "Fri" :
        wtag = 'Freitag'
    if day == "Sat" :
        wtag = 'Sonnabend'
    if day == "Sun" :
        wtag = 'Sonntag'
    return wtag
  
def init_gpio(pins):
    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        # GPIO.output(pin, GPIO.LOW)
        GPIO.output(pin, GPIO.HIGH)
  
###############################################################################  
server=ThreadingServer(("",config['port']),WebServer,"*")
pins = [21,20,16,12]
init_gpio(pins)
for pin in pins:
    # LED ON:
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.3)
    # LED OFF:
    GPIO.output(pin, GPIO.HIGH)
GPIO.output(pins[0], GPIO.LOW)
GPIO.output(pins[1], GPIO.LOW)
        

print("Enter '%s' as action url for a function key in your snom phone config." % config['base_url'])
print("Exit with ctrl+c\n")
try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\nBye ;)")

