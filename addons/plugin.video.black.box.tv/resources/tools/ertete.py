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

import plugintools, requests

playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumbnail = 'http://ertete.com/assets/img/logo.png'
fanart = 'http://plusfutbol.es/wp-content/uploads/2014/11/Liga-BBVA-2014-2015-Football-Stars-Wallpaper1.jpg'

from resources.regex.broadcastlive import *


def ertete0(params):
    plugintools.log("[%s %s] ertete.com parser %s " % (addonName, addonVersion, repr(params)))

    plugintools.add_item(action="", title = '[COLOR yellow]erTETE.com[/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

    url = params.get("url")
    body = plugintools.read(url)
    channels = plugintools.find_single_match(body, '<ul class="nav">(.*?)</ul>')

    kanal = plugintools.find_multiple_matches(channels, '<li(.*?)</li>')
    for entry in kanal:
        plugintools.log("entry= "+entry)
        url_canal = plugintools.find_single_match(entry, '<a href="([^"]+)')
        url_canal = 'http://www.ertete.com/'+url_canal
        plugintools.log("url_canal= "+url_canal)
        title_canal = plugintools.find_single_match(entry, '<a href[^>]+([^<]+)')
        title_canal = title_canal.replace(">", "").strip();plugintools.log("title_canal= "+title_canal)
        plugintools.add_item(action="ertete1", title='[COLOR white]'+title_canal+'[/COLOR]', url=url_canal, thumbnail = thumbnail, fanart=fanart, folder=False, isPlayable=True)

# http://ertete.com/embed/2.php

def ertete1(params):
    plugintools.log("[%s %s] ertete1 %s " % (addonName, addonVersion, repr(params)))

    url = params.get("url")
    body = plugintools.read(url)

    iframe = plugintools.find_single_match(body, '<iframe width="728" height="420"(.*?)</iframe>');iframe_link = plugintools.find_single_match(iframe, 'src="([^"]+)')
    iframe_link = 'http://ertete.com'+iframe_link;ref=iframe_link;plugintools.log("iframe_link= "+iframe_link)    

    bodi = plugintools.read(iframe_link)
    plugintools.log("bodi= "+bodi)
    bloque_rtmp = plugintools.find_single_match(bodi, "<script type='text/javascript'(.*?)<div")
    if bloque_rtmp != "":        
        plugintools.log("bloque_rtmp= "+bloque_rtmp)
        swf = plugintools.find_single_match(bloque_rtmp,"src='([^']+)");plugintools.log("swf= "+swf)
        width = plugintools.find_single_match(bloque_rtmp,"width=([^,]+)");plugintools.log("width= "+width)
        height = plugintools.find_single_match(bloque_rtmp,"height=([^,]+)");plugintools.log("height= "+height)
        channel = plugintools.find_single_match(bloque_rtmp,"channel='([^']+)");plugintools.log("channel= "+channel)
    else:
        bloque_rtmp = plugintools.find_single_match(bodi, '<script type="text/javascript"(.*?)<div')
        plugintools.log("bloque_rtmp= "+bloque_rtmp)
        swf = plugintools.find_single_match(bloque_rtmp,'src="([^"]+)');plugintools.log("swf= "+swf)
        width = plugintools.find_single_match(bloque_rtmp,"width=([^&]+)");plugintools.log("width= "+width)
        height = plugintools.find_single_match(bloque_rtmp,"height=([^&]+)");plugintools.log("height= "+height)
        channel = plugintools.find_single_match(bloque_rtmp,"embed/(.*?)&width");plugintools.log("channel= "+channel)        

    if swf.find("broadcastlive") >= 0:
        pageurl = 'http://1broadcastlive.com/embed/embed.php?channel='+channel+'&w='+width+'&h='+height
        params = plugintools.get_params();params["url"]='swfUrl='+swf+' pageUrl='+pageurl+' referer='+ref;broadcastlive1(params)
    elif swf.find("iguide") >= 0:  # Crear regex de iguide!!
        # http://www.iguide.to/embedplayer_new.php?width=728&height=420&channel=31086&autoplay=true
        pageurl = 'http://www.iguide.to/embedplayer_new.php?width='+width+'&height='+height+'&channel='+channel+'&autoplay=true'
        body = gethttp_referer_headers(pageurl,ref);plugintools.log("body= "+body)
        playpath=plugintools.find_single_match(body,"'file': '(.*?).flv");plugintools.log("playpath= "+playpath)
        token='#ed%h0#w18623jsda6523lDGD'
        url = 'rtmp://safe.iguide.to/iguide playpath='+playpath+' swfUrl=http://cdn.iguide.to/player/secure_player_iguide_embed_token.swf pageUrl='+pageurl+' token='+token
        print url;plugintools.play_resolved_url(url)
        #body = gethttp_referer_headers(swf,ref);plugintools.log("body="+body)
        
        
        



def gethttp_referer_headers(url,ref):
    plugintools.log("url= "+url)
    plugintools.log("ref= "+ref)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    #plugintools.log("body= "+body)
    return body        


        


        
    
    

    

    

    


