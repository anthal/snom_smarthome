#!/usr/bin/python2

### Libs:
## python2:
import random
import time

## hue:
import phue
# pip2 install phue

## snom
from homematic import Homematic
import conf
from snom import SnomXML

global config
config = conf.config()

hue = phue.Bridge(config['hue_ip']) # Enter bridge IP here.
# If running for the first time, press button on bridge and run with b.connect() uncommented
# hue.connect()

try:
    lights = hue.get_light_objects()
except:
    print("=================================================================")
    print("ERROR: HUE Bridge nicht erreichbar! IP Adresse in conf.py falsch?")
    print("=================================================================")
homematic = Homematic()

###############################################################################
class Commands():

    interface = 'wireless'
    
    def __init__(self, brightness ) :
        self.brightness = brightness

    
    def set_value(self, name, value):
        # value2 = 0
        name_list = name.split('_')
        print(name_list)
        
        # Light (Hue) with Menue:
        if name_list[0] == 'light' : 
            value2 = int(value)
            print("set_value - name: " + name + ", value: " + str(value)) 
            if name == 'light_1_wz':
                light_id = 1
            if name == 'light_1_az':
                light_id = 2
            if name == 'light_1_sz':
                light_id = 3
            if value2 == 0 :
                value = False
            if value2 > 0 :
                value = True
            if value2 > 1 :
                print("int value2 > 1: " + str(value2) + ", light_id: " + str(light_id))
                lights = hue.get_light_objects(mode='id')
                # Tageslicht:
                if value2 == 2 :
                    val_xy = [0.3101, 0.3162]
                    # hue.set_light(light_id, 'ct', 154) # white
                # Gluehlampe / warm    
                if value2 == 3 :
                    # val_xy = [0.3484, 0.3516] # 
                    val_xy = [0.4476, 0.4074]
                    # hue.set_light(light_id, 'ct', 500) # gelb
                if value2 == 4 :
                    # Pink:
                    # val_xy = [0.5204, 0.2362]
                    # Weinrot:
                    val_xy = [0.3933, 0.1656]
                if value2 >= 5 :
                    # val_xy = [0.6267, 0.2952]
                    # val_xy = [0.5204, 0.2362]
                    # val_xy = [0.23, 0.23]
                    # Blau:
                    val_xy = [0.05, 0.15]
                print("val_xy[0]: " + str(val_xy[0]) + ", val_xy[1]: " + str(val_xy[1]) + ", light_id: " + str(light_id))
                lights[light_id].xy = [ val_xy[0], val_xy[1] ]
            print("set_value - name: " + name + ", value: " + str(value) + ", value2: " + str(value2) + ", light_id: " + str(light_id)) 
            hue.set_light(light_id, 'bri', self.brightness)
            hue.set_light(light_id, 'on', value)
            
        # Light (Hue) without Menue:
        elif name_list[0] == 'hue' : 
            value2 = int(value)
            print("set_value - name: " + name + ", value2: " + str(value2)) 
            light_id = int(name_list[1])
            if value2 == 0 :
                value = False
            if value2 > 0 :
                value = True
            if value2 > 1 :
                print("int value2 > 1: " + str(value2) + ", light_id: " + str(light_id))
                lights = hue.get_light_objects(mode='id')
                # Tageslicht:
                if value2 == 2 :
                    val_xy = [0.3101, 0.3162]
                    # hue.set_light(light_id, 'ct', 154) # white
                # Gluehlampe / warm    
                if value2 == 3 :
                    # val_xy = [0.3484, 0.3516] # 
                    val_xy = [0.4476, 0.4074]
                    # hue.set_light(light_id, 'ct', 500) # gelb
                if value2 == 4 :
                    # Pink:
                    # val_xy = [0.5204, 0.2362]
                    # Weinrot:
                    val_xy = [0.3933, 0.1656]
                if value2 >= 5 :
                    # val_xy = [0.6267, 0.2952]
                    # val_xy = [0.5204, 0.2362]
                    # val_xy = [0.23, 0.23]
                    # Blau:
                    val_xy = [0.05, 0.15]
                print("val_xy[0]: " + str(val_xy[0]) + ", val_xy[1]: " + str(val_xy[1]) + ", light_id: " + str(light_id))
                lights[light_id].xy = [ val_xy[0], val_xy[1] ]
            print("set_value - name: " + name + ", value: " + str(value) + ", value2: " + str(value2) + ", light_id: " + str(light_id)) 
            hue.set_light(light_id, 'bri', self.brightness)
            hue.set_light(light_id, 'on', value)
            
        # Homematic Sockets:
        else :
            if name == 'state_socket_1_wz':
                homematic.set_value(self.interface, config['addr_wz_socket1'], 1, 'STATE', value)
            if name == 'state_socket_1_az':
                homematic.set_value(self.interface, config['addr_az_socket1'], 1, 'STATE', value)
            if name == 'state_socket_1_sz':
                homematic.set_value(self.interface, config['addr_sz_socket1'], 1, 'STATE', value)
    
    
    def get_value(self, name):
        value = 0
        self.interface = 'wireless'
        
        print("get_value - name: " + name) 
        ## Light Hue:
        if name == 'light_1_wz':
            # Prints if light 1 is on or not
            value = hue.get_light(1, 'on')
        if name == 'light_1_az':
            value = hue.get_light(2, 'on')
        if name == 'light_1_sz':
            value = hue.get_light(3, 'on')
            
        ## Homematic Sockets:        
        '''
        Unterstuetzte Geraetetypen
        - HM-LC-Dim1L-Pl
        - HM-LC-Dim1L-CV
        - HM-LC-Dim2L-CV
        - HM-LC-Dim2L-SM
        - HSS-DX
        '''
        # WZ:    
        # addr = addr_wz_socket1
        if name == 'state_socket_1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_socket1'], 1, 'STATE')
        if name == 'power_socket_1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_socket1'], 2, 'POWER')
        if name == 'energy_counter_socket_1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_socket1'], 2, 'ENERGY_COUNTER')
        if name == 'current_socket_1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_socket1'], 2, 'CURRENT')
        if name == 'voltage_socket_1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_socket1'], 2, 'VOLTAGE')
        if name == 'frequency_socket_1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_socket1'], 2, 'FREQUENCY')
        
        # AZ
        if name == 'state_socket_1_az':
            value = homematic.get_value(self.interface, config['addr_az_socket1'], 1, 'STATE')
        if name == 'power_socket_1_az':
            value = homematic.get_value(self.interface, config['addr_az_socket1'], 2, 'POWER')
        if name == 'energy_counter_socket_1_az':
            value = homematic.get_value(self.interface, config['addr_az_socket1'], 2, 'ENERGY_COUNTER')
        if name == 'current_socket_1_az':
            value = homematic.get_value(self.interface, config['addr_az_socket1'], 2, 'CURRENT')
        if name == 'voltage_socket_1_az':
            value = homematic.get_value(self.interface, config['addr_az_socket1'], 2, 'VOLTAGE')
        if name == 'frequency_socket_1_az':
            value = homematic.get_value(self.interface, config['addr_az_socket1'], 2, 'FREQUENCY')
            
        # SZ:    
        if name == 'state_socket_1_sz':
            value = homematic.get_value(self.interface, config['addr_sz_socket1'], 1, 'STATE')
        if name == 'power_socket_1_sz':
            value = homematic.get_value(self.interface, config['addr_sz_socket1'], 2, 'POWER')
        if name == 'energy_counter_socket_1_sz':
            value = homematic.get_value(self.interface, config['addr_sz_socket1'], 2, 'ENERGY_COUNTER')
        if name == 'current_socket_1_sz':
            value = homematic.get_value(self.interface, config['addr_sz_socket1'], 2, 'CURRENT')
        if name == 'voltage_socket_1_sz':
            value = homematic.get_value(self.interface, config['addr_sz_socket1'], 2, 'VOLTAGE')
        if name == 'frequency_socket_1_sz':
            value = homematic.get_value(self.interface, config['addr_sz_socket1'], 2, 'FREQUENCY')
        # WZ:
        '''
        Unterstuetzte Geraetetypen:
        - HM-CC-RT-DN
        '''
        if name == 'temp_wz':
            value = homematic.get_value(self.interface, config['addr_wz_heating1'], 4, 'ACTUAL_TEMPERATURE')
        if name == 'settemp_wz':
            value = homematic.get_value(self.interface, config['addr_wz_heating1'], 4, 'SET_TEMPERATURE')
        if name == 'valve_wz':
            value = homematic.get_value(self.interface, config['addr_wz_heating1'], 4, 'VALVE_STATE')
        if name == 'controlmode_wz':
            value = homematic.get_value(self.interface, config['addr_wz_heating1'], 4, 'CONTROL_MODE')
        if name == 'battery_valve1_wz':
            value = homematic.get_value(self.interface, config['addr_wz_heating1'], 4, 'BATTERY_STATE')
        # AZ:    
        if name == 'temp_az':
            '''
            Unterstuetzte Geraetetypen:
            - KS550
            - KS888
            - KS550Tech
            - KS550LC
            - HM-WDS100-C6-O
            '''
            print("self.interface: " + self.interface) 
            value = homematic.get_value(self.interface, config['addr_az_sensor1'], 1, 'TEMPERATURE')
        if name == 'humidity_az':
            value = homematic.get_value(self.interface, config['addr_az_sensor1'], 1, "HUMIDITY")
            
        if name == 'window1_wz':
            '''
            Unterstuetzte Geraetetypen:
            '''
            # state = command.get_value(self.interface, config['addr_wz_window1'], 1, 'STATE')
            value = homematic.get_value(self.interface, config['addr_wz_window1'], 1, 'STATE')
        
        
        
        print("get_value - value: " + str(value)) 
        return value

