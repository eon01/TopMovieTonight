# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Add your USERHASH, you can get one here: http://kazer.org/ ,  you should create an account and you select the channels here http://kazer.org/my-channels.html,
# then save your choice and run the script with your userhash. TMPDIR by default is /tmp/ just change it to whatever you want according to your OS, or just keep it if you're using *nix system.

USERHASH = ""
TEMPDIR = "/tmp/"


import os
import urllib
import zipfile
import xml.etree.ElementTree as ET
from oauthlib.common import urlencode
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import sys,re
from IMDB import ImdbRating
from time import sleep
from tempfile import TemporaryFile

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
            title = tv.find('title').text.encode('utf8')            
            date = tv.find('date').text #.encode('utf8')
            start = tv.get('start')
            chan = tv.get('channel').split('.',1)[0]    
            length = tv.find('length').text
            
            try: 
                rating = ImdbRating(title).rating
            except:
                rating = None
             
            try:
                url = ImdbRating(title).url
            except:
                import urllib2
                url = "http://www.imdb.com/find?q=" + urllib2.quote(title)
            sleep(1)
            d.append({ 'title':title ,'date':date, 'start':start, 'chan':chan, 'length':length, 'rating':rating, 'url':url})
            
    newd = sorted(d, key=lambda k: k['rating'], reverse= True) 
    return newd
                    

           

if __name__ == "__main__":
    url = "http://www.kazer.org/tvguide.zip?u="+ USERHASH
    file = getunzipped(url, TEMPDIR)
    print parse_xml(file)
