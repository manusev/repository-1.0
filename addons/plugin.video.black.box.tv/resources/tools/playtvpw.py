# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de laligatv.es
# Version 0.1 (18.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, scrapertools

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://playtv.pw/wp-content/uploads/2015/05/logo1.png'
fanart = 'http://46wvda23y0nl13db2j3bl1yxxln.wpengine.netdna-cdn.com/wp-content/uploads/2013/06/tsn-dudes.jpg'

from resources.regex.broadcastlive import *


def playtvpw0(params):
    plugintools.log("[%s %s] PlayTV.pw0 parser %s " % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="", title = '[COLOR yellow][B]PlayTV.pw[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

    url = 'http://www.playtv.pw/'
    data = scrapertools.cache_page(url)
    #plugintools.log("data= "+data)
    events = plugintools.find_multiple_matches(data, '<div class="events_grid">(.*?)</div><!--/entry-->')
    for entry in events:
        plugintools.log("entry= "+entry)
        event_day = plugintools.find_single_match(entry, '<div class="events_date">([^<]+)');event_day=event_day.strip()
        event_time = plugintools.find_single_match(entry, '<div class="events_time">([^<]+)');event_time=event_time.strip()
        event_cat = plugintools.find_single_match(entry, '<div class="events_cat">([^<]+)');event_cat=event_cat.strip()
        event_title = plugintools.find_single_match(entry, '<div class="events_title">([^<]+)');event_title=event_title.strip()
        event_url = plugintools.find_single_match(entry, '<a href="([^"]+)');event_url=event_url.strip()
        event_id = event_url.replace("/", "").split("events")
        if len(event_id) >= 2:
            event_id = event_id[1]
            plugintools.log("event_id= "+event_id)
        event_title=event_title.replace("&#8211;", "-")
        #plugintools.log("event_day= "+event_day)
        #plugintools.log("event_time= "+event_time)
        #plugintools.log("event_cat= "+event_cat)
        #plugintools.log("event_title= "+event_title)
        #plugintools.log("event_url= "+event_url)
        plugintools.add_item(action="playtvpw1",title=event_day+" "+event_time+" "+event_cat+" "+event_title,url=event_url, extra=event_id, thumbnail = thumbnail , fanart = fanart , folder=False, isPlayable=True)
        
        

def playtvpw1(params):
    plugintools.log("[%s %s] PlayTV.pw1 parser %s " % (addonName, addonVersion, repr(params)))

    title_canales = []
    url_canales = []

    url = params.get("url")
    data = scrapertools.cache_page(url)
    #plugintools.log("data= "+data)
    #num_links_bloque = plugintools.find_single_match(data, 'jQuery(.*?)</script>')
    num_links_bloque = plugintools.find_single_match(data, '<div class="alternative-link"(.*?)</div>')
    plugintools.log("num_links_bloque= "+num_links_bloque)
    num_links = plugintools.find_multiple_matches(num_links_bloque, '<a class="mybutton" href="([^"]+)')
    title_links = plugintools.find_multiple_matches(num_links_bloque, ';">(.*?)</a>')
    for entry in num_links:
        url_canales.append(entry)

    for entri in title_links:
        title_canales.append(entri)

    #print url_canales
    #print title_canales

    try:

        dia = plugintools.selector(title_canales, 'PlayTV.pw')
        ch = url_canales[dia];ch=ch.replace("#","")
        #plugintools.log("CANAL: "+ch)
        url_ajax = 'http://playtv.pw/wp-admin/admin-ajax.php?action=get_link_func&link='+ch+'&id='+params.get("extra")
        plugintools.log("url_ajax= "+url_ajax)
        url = playtvpw2(params,url_ajax)
        plugintools.play_resolved_url(url)
        
    except KeyboardInterrupt: pass;
    except IndexError: raise;
    except: pass    

    


def playtvpw2(params, url_ajax):
    plugintools.log("[%s %s] PlayTV.pw2 parser %s " % (addonName, addonVersion, repr(params)))

    plugintools.log("url_ajax= "+url_ajax)
    data = scrapertools.cache_page(url_ajax)
    plugintools.log("data= "+data)
    url = plugintools.find_single_match(data, 'file: "([^"]+)')
    #plugintools.log("URL final= "+url)
    return url
    
    
        



    

def gethttp_referer_headers(url,ref):
    plugintools.log("url= "+url)
    plugintools.log("ref= "+ref)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    #plugintools.log("body= "+body)
    return body        


        


        
    
    

    

    

    


