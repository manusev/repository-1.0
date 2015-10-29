# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV parser de mebuscan.net
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import sys
import urllib
import urllib2
import re
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


thumbnail = 'http://dl.dropbox.com/s/6hz0zis2uaz87v9/Canales%20acestream.jpg'
fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg'



def mebuscan(params):
    plugintools.log("[black.box.tv].Mebuscan.net( "+repr(params))
    plugintools.add_item(action="", title = '[B][COLOR blue]Acestream Sports Playlist[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)    

    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)

    matches = plugintools.find_multiple_matches(data, '<td  class="classcelda"(.*?)</td>')    
    for entry in matches:
        plugintools.log("entry= "+entry)
        canal_url = plugintools.find_single_match(entry, 'onclick=(.*?)><strong>')
        canal_url = canal_url.replace("ventananueva(", "")
        canal_url = canal_url.replace(")", "")
        canal_url = 'http://www.mebuscan.net/kos/Depo'+canal_url+'.php'
        plugintools.log("canal_url= "+canal_url)
        thumb_canal = plugintools.find_single_match(entry, 'src="([^"]+)')
        thumb_canal = 'http://www.mebuscan.net/'+thumb_canal
        plugintools.log("thumb_canal= "+thumb_canal)
        canal_title = plugintools.find_single_match(entry, '<br>(.*?)</strong>')
        plugintools.log("canal_title= "+canal_title)
        plugintools.add_item(action="mebuscan_geturl" , title = canal_title, url = canal_url , thumbnail = thumb_canal , fanart = fanart , isPlayable = True, folder = False)

        
def mebuscan_geturl(params):
    plugintools.log("[black.box.tv].mebuscan_geturl( "+repr(params))

    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)

    # Control Acestream
    url = plugintools.find_multiple_matches(data, 'var httpid="([^"]+)')
    for entry in url:
        url_ace = entry.strip()
        if len(url_ace) == 40:
            #title = params.get("title").strip()
            #title_fixed = title.replace(" ", "+")
            url = 'plugin://plugin.video.p2p-streams/?url=' + url_ace + '&mode=1&name='
            #title_fixed = title.replace(" ", "+")
            plugintools.log("url_ace= "+url_ace)
            plugintools.play_resolved_url(url)
    
