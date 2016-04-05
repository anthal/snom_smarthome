#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# see main.py for copyright, contacts and version information
#
# Hinweis: uebergebene Strings muessen im UTF-8-Encoding sein

import xmlrpclib
import random

import conf

global config
config=conf.config()

########################################################### 
# Homematic 
########################################################### 
class Homematic:
    
    licht_wz = False
    licht_az = False
    licht_sz = False
    
    def get_value(self, interface, addr, channel, value_key):  
        '''
        
        '''
        if interface == 'wired':
            port = 2000
        if interface == 'wireless':
            port = 2001
        if interface == 'system':
            port = 2002
        cli = xmlrpclib.ServerProxy(config['homematic_url'] + ":" + str(port))
        # print("homematic.getValue " + addr + ":" + str(channel) + ", value_key: " + value_key)
        try:
            status = cli.getValue(addr + ":" + str(channel),value_key)
        except:
            print("ERROR - Homematic Problem with addr.: " + addr + ", channel: " + str(channel) + ", value_key: " + value_key) 
            status = 0
        
        ##Only For Simulation:
        '''
        if value_key == 'TEMPERATURE' :
            status = random.randint(17,25)
        elif value_key == 'SETPOINT' :
            status = random.randint(17,25)
        elif value_key == 'HUMIDITY' :
            status = random.randint(37,85)
        elif value_key == 'VALVE_STATE' :
            status = random.randint(0,99)
        elif value_key == 'STATE' :
            if addr == 'IEQ4101017':
                if channel == 1 :
                    status = self.licht_wz
                if channel == 9 :
                    status = self.licht_az
                if channel == 7 :
                    status = self.licht_sz
            else:    
                status = random.randint(0,2)
        else:    
            status = random.randint(0,1)
        '''    
        # print("get_value - value_key: " + value_key + ", channel: " + str(channel) + ", status: " + status) 
        
        # print status
        # self.status
        # return self.status
        return status
        
    def set_value(self, interface, addr, channel, value_key, value):  
        '''
        homematic.set_value('wired', 'IEQ4101017', 1, 'STATE', 'true')
        '''
        
        if interface == 'wired':
            port = 2000
        if interface == 'wireless':
            port = 2001
        if interface == 'system':
            port = 2002
        cli = xmlrpclib.ServerProxy(config['homematic_url'] + ":" + str(port))
        cli.setValue(addr+":"+str(channel), value_key, value)
        
        ##Only For Simulation:
        '''
        if value_key == 'STATE':
            if channel == 1 :
                self.licht_wz = value
            if channel == 9 :
                self.licht_az = value
            if channel == 7 :
                self.licht_sz = value
        '''
        # print("set_value - value_key: " + value_key + ", channel: " + str(channel) + ", value: " + value) 
        
        return 0
        