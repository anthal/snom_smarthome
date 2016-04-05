#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# see main.py for copyright, contacts and version information
#
# import handlers
def config():
    config = {}
    config['handlers'] = []

    ########################### Port / IP ###########################

    config['port'] = 8083
    
    ## Raspberry Pi:
    server_ip = '172.20.4.117'
    
    ## D375 for Alarm Pictures:
    phone_ip = '172.20.10.202'
    
    ## Homematic Centrale CCU2:
    homematic_ip = '172.20.4.110'
    
    ## Philips Hue:
    config['hue_ip'] = '172.20.4.113'
    
    config['cam1_url'] = 'http://admin:admin@172.20.4.111/tmpfs/auto.jpg'
    config['cam2_url'] = 'http://admin:admin@172.20.4.112/tmpfs/auto.jpg'

    ########################### RSS ###########################
    config['rss_file'] = "/root/python/snom/CeBit/feed_liste.txt"
    
    
    ####################### Do Not Touch ! #######################
    config['base_url'] = "http://" + server_ip + ":%s/" % config['port']

    
    ########################### Icons ###########################
    config['capture_url'] = "http://" + server_ip + "/capture/"
    
    # Pfad zum Lighttpd-Webserver unter Arch-Linux: /srv/http/icons/
    config['icons_url'] = "http://" + server_ip + ":81/icons/"
    
    config['phone_url'] = "http://" + phone_ip + "/"
    config['homematic_url'] = "http://" + homematic_ip
    

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
    
    ########################### Philips Hue ###########################
    # config['brightness'] = 128
    config['brightness'] = 255
    
    
    return config
