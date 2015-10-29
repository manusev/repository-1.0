# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de Stadium-live.biz
# Version 0.1 (17.10.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)


import os
import urllib
import urllib2
import shutil
import zipfile
import time

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools, scrapertools
import sys,traceback,urllib2,re

from __main__ import *


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

art = xbmc.translatePath(os.path.join(addonPath + '/art/', ''))
fanart = 'http://images.forwallpaper.com/files/thumbs/preview/20/200693__fan-football-stadium-sports_p.jpg'
thumbnail = art + 'stadiumlive.png'

def stadiumlivebiz0(params):
    plugintools.log('[%s %s] Initializing stadium-live.biz parser... %s' % (addonName, addonVersion, repr(params)))
    plugintools.add_item(action="", title="[COLOR lightgreen][B]stadium-live.biz[/B][/COLOR]", url="" , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)
    plugintools.add_item(action="stadiumlivebiz2", title="[COLOR lightyellow]Abrir canal...[/COLOR]", url="" , thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)

    burl = params.get("url")
    ref = burl;body=gethttp_referer(burl,ref,"")
    #plugintools.log("body= "+body)    

    schedule_bloque = plugintools.find_single_match(body, 'calendar_wrap(.*?)<!--')
    #plugintools.log("schedule= "+schedule_bloque)
    events = plugintools.find_multiple_matches(schedule_bloque, '<tr>(.*?)</a>')
    for entry in events:
        #plugintools.log("entry= "+entry)
        if entry != "":
            entry = entry.replace("&nbsp;", "")
            event_time = plugintools.find_single_match(entry, '<p class=\"sdfsf\">(.*?)</td>')
            event_title = plugintools.find_single_match(entry, '\" class="sdfsf">(.*?)</td>')
            event_title = event_title.replace("<p>","").strip()
            event_channel = plugintools.find_single_match(entry, 'href="([^"]+)')
            event_channel = 'http://www.stadium-live.biz/'+event_channel
            ch = plugintools.find_single_match(entry, '<a targ[^>]+>([^<]+)')
            #plugintools.log("event_time= "+event_time)
            #plugintools.log("event_title= "+event_title)
            #plugintools.log("event_channel= "+event_channel)
            #plugintools.log("ch= "+ch)
            
            plugintools.add_item(action="stadiumlivebiz1", title='[COLOR orange][B]'+event_time+' [/B][COLOR lightyellow][I]'+event_title+' [COLOR lightgreen]['+ch+'][/I][/COLOR]' , fanart = fanart , thumbnail = thumbnail , url=event_channel , folder = False, isPlayable = True)
            
        

def stadiumlivebiz1(params):
    plugintools.log('[%s %s] Initializing stadium-live.biz parser... %s' % (addonName, addonVersion, repr(params)))    
    
    burl = 'http://www.stadium-live.biz'
    ref = 'http://www.stadium-live.biz'
    ch = params.get("url")
    title = params.get("title")
    
    body = "";body = gethttp_referer(ch,ref,body)
    #plugintools.log("body= "+body)

    caster = plugintools.find_multiple_matches(body, '<!--<script type="text/javascript" src="([^"]+)')
    for entry in caster:
        if entry.find("autostart=true") >= 0:
            #plugintools.log("entry= "+entry)
            caster = entry

    ref = params.get("url")
    url = ref.replace("Channel", "ch_").strip()
    url = url.replace(".html", "");url = url+'code.html'
    #plugintools.log("url= "+url)
    #plugintools.log("ref= "+ref)
    body = ''
    body = gethttp_referer(url,ref,body)
    #plugintools.log("body= "+body)

    #<script type="text/javascript" src="http://www.playerapp1.pw/channel.php?file=118&width=800&height=450&autostart=true"></script>
    
    url = plugintools.find_single_match(body, 'src="([^"]+)')
    ref = 'http://www.stadium-live.biz/ch_1code.html'
    
    body = gethttp_referer(url,ref,body)
    url = plugintools.find_single_match(body, 'src="([^"]+)');url=url.strip()    
    #plugintools.log("url= "+url)
    #plugintools.log("ref= "+ref)
    body = gethttp_referer(url,ref,body)
    playerapp1(url,ref,body)
    
    
    
def playerapp1(url,ref,body):
    k=url;hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);#print hidd;
    swfUrl='http://www.playerapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));    
    app=plugintools.find_single_match(hidd[1][1].decode('base64').replace('\\',''),'1735\/([^"]+)');#app=app.replace("vod", "redirect")
    q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto    
    w=hidd[1][1].decode('base64').replace('\\','').replace("vod","redirect")+' app='+app+' playpath='+hidd[0][1].decode('base64')+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
    plugintools.play_resolved_url(w);sys.exit()
    

# Black Box TV: rtmp://185.39.9.66:1735/redirect/?token=play@143138721306103 app=redirect/?token=play@143138721306103 playpath=stream22 flashver=WIN%5C2017,0,0,134 swfUrl=http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf swfVfy=1 pageUrl=http://www.businessapp1.pw/embed.php?c=118&width=800&height=450&autostart=true&tk1=fSF2wqOS8zrUpyVvdccG4H0iAa7acLpPNneTN65QPW37WkuYMawC4oWoV10tE4N8TgsjmZ0lswpj2o4bzFcypg%3D%3D&tk2=0A01D3oBwZLM0G1K%2BKHY7PkfAUDLfRxdS8v%2B%2FvaYpAM%3D&tk3=ETl1snhb7rMJsb7WnkLumNk3MdHlcOnEBP8bfp%2BvyMs%3D live=1 timeout=15
# URLHELPER: rtmp://185.39.11.10:1735/vod/?token=play@143138689202438 playpath=stream22 swfUrl=http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf pageUrl=http://www.playerapp1.pw/embed.php?c=118&width=800&height=450&autostart=true&tk1=EFnWAFo7tCIi245Xljl%2BYX4eiUtijJWNHRunrIH2mVWA11uMgHwhTqLkUgxgu5jT9JuYHsqJqpj5sJYwamXUlw%3D%3D&tk2=L8pz%2BHjjc7%2FxGBXNoXEJEVMkCDhlvh3uot%2FzrM3GVbQ%3D&tk3=zentLoFQweXhbE3DUb86sM6qqiODtB8s9LukwfazBl0%3D

   
def stadiumlivebiz2(params):
    plugintools.log('[%s %s] stadiumlivebiz2 %s' % (addonName, addonVersion, repr(params)))
    
    burl = 'http://www.stadium-live.biz'
    ref = burl;body=gethttp_referer(burl,ref,"")
    #plugintools.log("body= "+body)
    channel_bloque = plugintools.find_single_match(body, '<ul id="main"(.*?)</ul>')
    channel = plugintools.find_multiple_matches(channel_bloque, '<li>(.*?)</li>')
    lista_ch = []
    url_ch = []

    for entry in channel:
        if entry != "":
            #plugintools.log("entry= "+entry)
            url_channel = plugintools.find_single_match(entry, '<a href="([^"]+)')
            url_channel = 'http://www.stadium-live.biz/'+url_channel
            title_channel = plugintools.find_single_match(entry, '<a href[^>]+>(.*?)</a>')
            #plugintools.log("title_channel= "+title_channel)
            lista_ch.append(title_channel)
            url_ch.append(url_channel)
            #plugintools.log("url_channel= "+url_channel)
            #plugintools.add_item(action="stadiumlivebiz1", title='[COLOR white]'+title_channel+'[/COLOR]', url=url_channel , thumbnail = art + 'stadiumlive.png' , fanart = fanart , folder = False, isPlayable = True)

    select_ch = plugintools.selector(lista_ch, 'Stadium-live.biz')
    #print url_ch
    plugintools.get_params()
    params["url"]=url_ch[select_ch]
    params["title"] = lista_ch[select_ch]
    stadiumlivebiz1(params)
    
    

def gethttp_referer(url,ref,body):
	request_headers=[];
	request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
	request_headers.append(["Referer",ref])
	body,response_headers=plugintools.read_body_and_headers(url, headers=request_headers);
	#print "HEADERS:N";print response_headers
	return body
    


def find_multiple_matches_multi(text,pattern):
    matches = re.findall(pattern,text, re.MULTILINE)
    return matches
