#!/usr/bin/python
# -*- coding: utf8 -*-

import feedparser
# pip2 install feedparser
import pickle
import re
import conf

global config
config=conf.config()

#########################################################################
# RSS
#########################################################################
def get_rss():
    fobj = open(config['rss_file'], "w")
    
    print "get_rss"
    d = feedparser.parse('http://www.heise.de/newsticker/heise-atom.xml')
    ## print all posts
    index = 0
    feed = []
    for post in d.entries:
        print post.title
        
        # print post.description
        content = post.description.split("<br")
        # content_out.replace("&quot", "'")
        content_out = re.sub("\u201c","\"", content[0] )
        content_out = re.sub("&quot;","\"", content_out )
        content_out = re.sub("&apos;","'", content_out )
        # print content_out
        
        picture = post.content[0].value.split("src=")
        # print picture[1]
        pic_link = picture[1].split("/>")
        # print pic_link[0] 
        
        data = (post.title, content_out, pic_link[0])
        # feed.append([ post.title, content[0], pic_link[0] ])
        feed.append( data )
        # print feed[index]
        # print index
        print "---------------------------------------------------------"
        index = index + 1
        if index > 15 :
            break

    pickle.dump(feed, fobj)
    # To read it back:
    # itemlist = pickle.load(fobj)    
    fobj.close()
        
#########################################################################
# RSS
#########################################################################
def test_liste():
    print "test_liste"
    index = 0
    feed = [[""],[""]]
    for post in (1,2,3):
        # feed[index][0] = content[0]
        feed.append(["TEST","ABS","ABC"])
        
        print "---------------------------------------------------------"
        index = index + 1
    
def read_liste():
    # fobj = open("feed_liste.txt","r")
    fobj = open("feed_liste.txt")
    # fobj = open(config['rss_file'])
    itemlist = pickle.load(fobj) 
    # print itemlist
    for item in itemlist:
        print item[0]

    
        
#########################################################################
# MAIN
#########################################################################
get_rss()
# test_liste()
# read_liste()

