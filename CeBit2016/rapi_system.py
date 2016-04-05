#!/usr/bin/python2
# -*- coding: utf8 -*-

#
# History:
# 06.03.2016 0.1  - initial


import os
import sys
import socket
import time

# https://github.com/giampaolo/psutil
# sudo pip2 install psutil
import psutil

#
###############################################################################
## Get IP:    
if os.name != "nt":
    import fcntl    # sudo pip2 install fcntl
    import struct
    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])
        
###############################################################################
class RaPi_System():


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

    
    def memory(self, key):
        '''
         total=970862592, available=579059712, percent=40.4, used=628842496, free=342020096, active=405573632, inactive=170086400, buffers=48046080, cached
        '''
        if key == 'total' :
            value = psutil.virtual_memory().total  / 1048576
        if key == 'available' :
            value = psutil.virtual_memory().available  / 1048576
        if key == 'percent' :
            value = psutil.virtual_memory().percent 
        if key == 'percent_free' :
            value = 100 - psutil.virtual_memory().percent 
        if key == 'used' :
            value = psutil.virtual_memory().used  / 1048576
        if key == 'free' :
            value = psutil.virtual_memory().free  / 1048576
        if key == 'active' :
            value = psutil.virtual_memory().active  / 1048576
        if key == 'inactive' :
            value = psutil.virtual_memory().inactive  / 1048576
        if key == 'buffers' :
            value = psutil.virtual_memory().buffers  / 1048576
        if key == 'cached' :
            value = psutil.virtual_memory().cached  / 1048576
        print psutil.virtual_memory()
        return value
    

    def disks(self, key):
        '''
        >>> psutil.disk_usage('/')
        sdiskusage(total=21378641920, used=4809781248, free=15482871808, percent=22.5)
        '''
        if key == 'total' :
            value = psutil.disk_usage('/').total / 1073741824
        if key == 'used' :
            value = psutil.disk_usage('/').used / 1073741824
        if key == 'free' :
            value = psutil.disk_usage('/').free / 1073741824
        if key == 'percent' :
            value = psutil.disk_usage('/').percent 
        if key == 'percent_free' :
            value = 100 - psutil.disk_usage('/').percent 
        # print psutil.disk_usage('/')
        return value

        
    def cpu(self, key):
        '''
        for x in range(3):
        psutil.cpu_percent(interval=1)
        '''
        cpu_load_list = []
        cpu_count = psutil.cpu_count()
        cpu_load_list.append(cpu_count)
        if key != 'core_count' :
            # print(cpu_count)
            for x in range(cpu_count):
                # print(str(x))
                # print(psutil.cpu_percent(interval=1))
                if x <= cpu_count:
                    cpu_load = psutil.cpu_percent(interval=1)
                    cpu_load_list.append(cpu_load)
        return cpu_load_list   

        
    def getGpuTemperature(self):
        ret = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline();
        temperature = ret.replace("temp=","").replace("'C\n","");
        return(float(temperature))  
        
        
    def getCpuTakt(self):
        ret = os.popen('/opt/vc/bin/vcgencmd measure_clock arm').readline();
        takt = ret.replace("frequency(45)=","").replace("'C\n","");
        return(float(takt)/1000000)  
        
        
    def uptime(self):
        # now = time.localtime() 
        now = time.time() 
        # print(now)
        uptime = now - psutil.boot_time() 
        # print(uptime)
        return int(uptime / 86400)
        
        
        
##########################################################################        
# MAIN    
system = RaPi_System()

# print(system.getCpuTakt())
# uptime = system.uptime()
# print(uptime)
# cpu_load = system.cpu('load')
# print(cpu_load())

# print(system.getGpuTemperature()) 
# print(system.get_lan_ip('eth0'))
# free_mem = system.memory('total')
# print(free_mem)
# free_mem = system.memory('free')
# print(free_mem)
# mem_percent = system.memory('percent')
# print(100 - mem_percent)
# mem_percent = system.memory('percent_free')
# print(mem_percent)



