# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = "Aymen Amri aka eon, eon01"
__copyright__ = "GNU GENERAL PUBLIC LICENSE Version 2"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "https://github.com/eon01/TopMovieTonight"
__email__ = "amri.aymen@gmail.com"
# ================================================================================================
# Add your USERHASH, you can get one here: http://kazer.org/ ,  
# you should create an account and you select the channels here http://kazer.org/my-channels.html,
# then save your choice and run the script with your userhash. 
# TMPDIR (temporary directory for extracting the zip file containing xmltv data)
# by default is /tmp/ just change it to whatever you want according to your OS, 
# or just keep it if you're using *nix system.
# ================================================================================================

USERHASH = "ENTER YOUR USERHASH HERE"
TEMPDIR = "/tmp/"


import os
import urllib
import zipfile
import xml.etree.ElementTree as ET
from oauthlib.common import urlencode
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import sys,re
sys.path.append("./res/")
from IMDB import ImdbRating
from time import sleep
import time
from tempfile import TemporaryFile
from dateutil import parser
from datetime import date
import locale
import json

def getunzipped(theurl, thedir):
    
    name = os.path.join(thedir, 'temp.zip')
    
    try:
		name, headers = urllib.urlretrieve(theurl, name)
    
    except IOError, e :
        print "Can't retrieve %r to %r: %s" % (theurl, thedir, e)
        return 1
	
    try:
		z = zipfile.ZipFile(name)
    except zipfile.error, e:
		print "Bad zipfile (from %r): %s" % (theurl, e)
		return 1
        
    for n in z.namelist():
		dest = os.path.join(thedir, n)
		destdir = os.path.dirname(dest)
		if not os.path.isdir(destdir):
			os.makedirs(destdir)
		data = z.read(n)
		f = open(dest, 'w')
		f.write(data)
		f.close()
    z.close()
    os.unlink(name)
    for i in z.namelist():
        if i == "tvguide.xml":
            return destdir+"/"+ i

def parse_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()
    i = 0
    d= []
    for tv in root.findall('programme'):
        cat = tv.find('category').text
        if cat == "Film":
            #Movie name
            try:
                title = tv.find('title').text.encode('utf8')
            except:
                title = "N/A"            
            #Movie date
            try:
                date = tv.find('date').text #.encode('utf8')
            except:
                date = "N/A"
            #Start date
            try:
                s = tv.get('start')
                st = parser.parse(s)
                lc = locale.getdefaultlocale()
                locale.setlocale (locale.LC_ALL ,lc)
                start = st.strftime('%A %C %B - %H:%M GMT+1')
            except: 
                start = "N/A"
            #Channel
            try :
                c = tv.get('channel').split('.',1)[0]            
                json_data=open('./res/channels.json')            
                data = json.load(json_data)
                chan = data[c]
            except:
                chan = "N/A"
            #Movie length    
            try:
                length = tv.find('length').text
            except:
                length = "N/A"
            #IMDB Rating and URL
            try: 
                rating = ImdbRating(title).rating + "/10"
            except:
                rating = "N/A"
              
            try:
                url = ImdbRating(title).url
            except:
                import urllib2
                url = "http://www.imdb.com/find?q=" + urllib2.quote(title)
            else:
                import urllib2
                url = "https://duckduckgo.com/?q=" + urllib2.quote(title)
            #You can remove sleep, if you're sure .. The size of a json file can be more than 20 MB and the scrappping could take a long time
            sleep(1)
            d.append({ 'title':title ,'date':date, 'start':start, 'chan':chan, 'length':length, 'rating':rating, 'url':url})
            
    newd = sorted(d, key=lambda k: k['rating'], reverse= True)
    return newd
                    

           

if __name__ == "__main__":
    url = "http://www.kazer.org/tvguide.zip?u="+ USERHASH
    
    try:
        file = getunzipped(url, TEMPDIR)
    except:
        print ("XMLTV service is down or conncetion error")
         
        
    try:
        l = parse_xml(file)
        for k in l:
            title = k['title']  + "\n"
            rating = str(k['rating']) + "\n"
            date = k['date'] + "\n"
            start = k['start'] + "\n"
            chan = k['chan'] + "\n"
            length = k['length'] + "minutes " + "\n"
            url = k['url'] + "\n"
            print title , rating, date, start, chan, length, url         
            print("\n ============= ")
    except:
         #When there is no movie on TV !
         print ("Bad luck! There 's no movies on your list buddy")
