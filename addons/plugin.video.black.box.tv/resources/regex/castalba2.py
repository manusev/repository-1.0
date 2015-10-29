# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Regex de castalba
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
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools
import json


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


# En construcción!
def castalba(params):
    plugintools.log("[black.box.tv-0.3.0].castalba "+repr(params))

    url = params.get("url")
    plugintools.play_resolved_url(url)


# Función que guía el proceso de elaboración de la URL original
def castalba(params):
    plugintools.log("[black.box.tv-0.3.0].castalba "+repr(params))
    url_user = {}
    
    # Construimos diccionario...
    url = params.get("url")
    url_extracted = url.split(" ")
    for entry in url_extracted:
        if entry.startswith("rtmp"):
            entry = entry.replace("rtmp=", "")         
            url_user["rtmp"]=entry
        elif entry.startswith("playpath"):
            entry = entry.replace("playpath=", "")
            url_user["playpath"]=entry            
        elif entry.startswith("swfUrl"):
            entry = entry.replace("swfUrl=", "")
            url_user["swfurl"]=entry
        elif entry.startswith("pageUrl"):
            entry = entry.replace("pageUrl=", "")
            url_user["pageurl"]=entry          
        elif entry.startswith("token"):
            entry = entry.replace("token=", "")
            url_user["token"]=entry
        elif entry.startswith("referer"):
            entry = entry.replace("referer=", "")
            url_user["referer"]=entry

    plugintools.log("URL_user dict= "+repr(url_user))
    pageurl = url_user.get("pageurl")
    referer = url_user.get("referer")
    body = gethttp_referer_headers(pageurl,referer)
    plugintools.log("body= "+body)

    # Controlamos el caso de canal privado (requiere referer, por implementar)
    if body.find("THIS CHANNEL IS CURRENTLY OFFLINE") > 0 :
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Black Box TV', "Canal offline", 3 , art+'icon.png'))
        return 0
    else:
    
        # Iniciamos captura de parámetros
        file = re.compile('file\': \'(.*?)\',').findall(body)
        if file[0].endswith("m3u8"):
            plugintools.play_resolved_url(file[0])
        else:
            streamer = re.compile('streamer\': \'(.*?)\',').findall(body)
            playpath = re.compile('file\': \'(.*?)\',').findall(body)
            swfurl=url_user.get("swfurl")
            print streamer[0]
            print playpath[0]            
            
            # Construimos la URL original
            url = streamer[0] + ' playpath='+playpath[0]+' swfUrl='+swfurl+' pageUrl=http://castalba.tv live=true timeout=20'
            plugintools.log("url= "+url)
            plugintools.play_resolved_url(url)
        
 

def gethttp_referer_headers(url,ref):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    plugintools.log("body= "+body)
    return body
    
