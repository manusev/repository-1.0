# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Seriesadicto.com parser para Black Box TV
# Version 0.1 (20/12/2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Librerías Plugintools por Jesús (www.mimediacenter.info)


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




# Lectura de cada carátula, título y enlace a la página de descargas de la peli
def pelicatcher(params):
    plugintools.log("[black.box.tv-0.3.5].pelicatcher "+repr(params))  
    
    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)
    items = plugintools.find_multiple_matches(data, '<li class="col-xs-6 col-sm-2(.*?)</li>')
    for entry in items:
        plugintools.log("entry= "+entry)
        thumbnail = plugintools.find_single_match(entry, 'src="([^"]+)')
        thumbnail = 'http://www.pelisadicto.com'+thumbnail
        plugintools.log("thumbnail= "+thumbnail)
        title = plugintools.find_single_match(entry, 'title="([^"]+)')
        title = title.replace("Ver", "").replace("Online", "").strip()
        plugintools.log("title= "+title)        
        movie_url = 'http://www.pelisadicto.com' + plugintools.find_single_match(entry, 'href="([^"]+)')
        plugintools.log("movie_url= "+movie_url)
        plugintools.add_item(action="", title=title, url=movie_url, thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
        
        


def GetSerieChapters(params):
    plugintools.log("[black.box.tv-0.3.0].GetSerieChapters "+repr(params))

    season = params.get("season")
    data = plugintools.read(params.get("url"))
    
    season = plugintools.find_multiple_matches(data, season + '(.*?)</table>')
    season = season[0]
    
    for entry in season:
        url_cap = plugintools.find_multiple_matches(season, '<a href=\"/capitulo(.*?)\" class=\"color4\"')
        title = plugintools.find_multiple_matches(season, 'class=\"color4\">(.*?)</a>')

    num_items = len(url_cap)    
    i = 1
    
    while i <= num_items:
        url_cap_fixed = 'http://seriesadicto.com/capitulo/' + url_cap[i-1]
        title_fixed = title[i-1]
        fanart = params.get("extra")
        GetSerieLinks(fanart , url_cap_fixed, i, title_fixed)
        i = i + 1
        
        
    
def GetSerieLinks(fanart , url_cap_fixed, i, title_fixed):
    plugintools.log("[black.box.tv-0.3.0].GetSerieLinks")
    
    data = plugintools.read(url_cap_fixed)
    amv = plugintools.find_multiple_matches(data, 'allmyvideos.net/(.*?)"')
    strcld = plugintools.find_multiple_matches(data, 'streamcloud.eu/(.*?)"')
    vdspt = plugintools.find_multiple_matches(data, 'vidspot.net/(.*?)"')
    plydt = plugintools.find_multiple_matches(data, 'played.to/(.*?)"')
    thumbnail = plugintools.find_single_match(data, 'src=\"/img/series/(.*?)"')
    thumbnail_fixed = 'http://seriesadicto.com/img/series/' + thumbnail
    
    for entry in amv:
        amv_url = 'http://allmyvideos.net/' + entry        
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lightyellow] [Allmyvideos][/COLOR]', url = amv_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in strcld:
        strcld_url = 'http://streamcloud.eu/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lightskyblue] [Streamcloud][/COLOR]', url = strcld_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in vdspt:
        vdspt_url = 'http://vidspot.net/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR palegreen] [Vidspot][/COLOR]', url = vdspt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'http://played.to/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR lavender] [Played.to][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'vk.com' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR royalblue] [Vk][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

    for entry in plydt:
        plydt_url = 'nowvideo.sx' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR red] [Nowvideo][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)           

    for entry in plydt:
        plydt_url = 'http://tumi.tv/' + entry
        plugintools.add_item(action="play" , title = title_fixed + '[COLOR forestgreen] [Tumi][/COLOR]', url = plydt_url , thumbnail = thumbnail_fixed , fanart = fanart , folder = False , isPlayable = True)

        
        

def SelectTemp(params, temp):
    plugintools.log("[black.box.tv-0.3.0].SelectTemp "+repr(params))

    seasons = len(temp)
    
    dialog = xbmcgui.Dialog()
    
    if seasons == 1:
        selector = dialog.select('Black Box TV', [temp[0]])
                                             
    if seasons == 2:
        selector = dialog.select('Black Box TV', [temp[0], temp[1]])
                                             
    if seasons == 3:
        selector = dialog.select('Black Box TV', [temp[0],temp[1], temp[2]])
                                             
    if seasons == 4:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3]])
                                             
    if seasons == 5:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3], temp[4]])
        
    if seasons == 6:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5]])
        
    if seasons == 7:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6]])
        
    if seasons == 8:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7]])
        
    if seasons == 9:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8]])
        
    if seasons == 10:
        selector = dialog.select('Black Box TV', [temp[0], temp[1],temp[2], temp[3], temp[4], temp[5], temp[6], temp[7], temp[8], temp[9]])                               

    i = 0
    while i<= seasons :
        if selector == i:
            params["season"] = temp[i]
            GetSerieChapters(params)

        i = i + 1
