# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Seriesadicto.com parser para Black Box Movie
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
from resources.tools.resolvers import *


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.blackbox.movie/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.blackbox.movie/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.blackbox.movie/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.blackbox.movie/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.blackbox.movie/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'

def seriesblanco0(params):
    plugintools.log("[blackbox.movie-0.2.0].seriesblanco "+repr(params))

    thumbnail = "https://pbs.twimg.com/profile_images/552583274883600384/zrUo7Ya1.jpeg"
    fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
    
    url = params.get("url")    
    referer = url
    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    seasons = plugintools.find_multiple_matches(data, "<h2 style='cursor: hand; cursor: pointer;'><u>(.*?)</table>")
    for entry in seasons:
        #plugintools.log("entry= "+entry)
        title_temp = plugintools.find_single_match(entry, "(.*?)</u></h2>")
        chapter = plugintools.find_multiple_matches(entry, '<tr><td>(.*?)</td>')
        for entri in chapter:
            #plugintools.log("entri= "+entri)
            url_chapter = plugintools.find_single_match(entri, "<a href='([^']+)")
            url_chapter = 'http://www.seriesblanco.com'+url_chapter
            title_chapter = plugintools.find_single_match(entri, "'>(.*?)</a>")
            plugintools.log("title_chapter="+title_chapter)
            plugintools.log("url_chapter="+url_chapter)
            if title_chapter.find("x00") < 0:
                plugintools.add_item(action="seriesblanco1", title=title_chapter, url=url_chapter, thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)

    

def seriesblanco1(params):
    plugintools.log("[blackbox.movie-0.2.0].seriesblanco "+repr(params))

    thumbnail = "http://seriesblanco.com/imags_estilos/logoblanconavidad2.png"
    fanart = "http://socialgeek.co/wp-content/uploads/2013/06/series-TV-Collage-television-10056729-2560-1600.jpg"
    
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    match_listacapis = plugintools.find_single_match(data, "<form method='post' name=validacion action=''><table class='zebra'><caption class='tam16'>Visionados online</caption>(.*?)<div id='backlinks-container'>")
    #plugintools.log("match_listacapis= "+match_listacapis)
    match_capi = plugintools.find_multiple_matches(match_listacapis, "<td class='tam12'(.*?)</td></tr>")
    for entry in match_capi:
        plugintools.log("entry= "+entry)
        url_capi = plugintools.find_single_match(entry, "<a href='([^']+)")
        url_capi = 'http://www.seriesblanco.com'+url_capi
        plugintools.log("url_capi= "+url_capi)
        lang_audio = plugintools.find_single_match(entry, "<img src='/banderas/([^']+)")
        if lang_audio.find("es.png") >= 0:
            lang_audio = "Español"
        elif lang_audio.find("la.png") >= 0:
            lang_audio = "Latino"
        elif lang_audio.find("vos.png") >= 0:
            lang_audio = "Versión Original Subtitulada."
        elif lang_audio.find("vo.png") >= 0:
            lang_audio = "Versión Original."            
        plugintools.log("lang_audio= "+lang_audio)
        url_server = plugintools.find_single_match(entry, "<img src='/servidores/([^']+)")
        if url_server.find("allmyvideos") >=0:
            url_server = "allmyvideos"
        elif url_server.find("vidspot") >= 0:
            url_server = "vidspot"
        elif url_server.find("played.to") >= 0:
            url_server = "played.to"
        elif url_server.find("streamin.to") >= 0:
            url_server = "streamin.to"
        elif url_server.find("streamcloud") >= 0:
            url_server = "streamcloud"
        elif url_server.find("nowvideo") >= 0:
            url_server = "nowvideo"
        elif url_server.find("veehd") >= 0:
            url_server = "veehd"
        elif url_server.find("vk") >= 0:
            url_server = "vk"
        elif url_server.find("tumi") >= 0:
            url_server = "tumi"
        else:
            url_server = url_server.replace(".png", "").replace(".jpg", "")
        plugintools.log("url_server= "+url_server)
        quality_url = plugintools.find_single_match(entry, "<td class='tam12'>(.*?)</td></tr>")
        if quality_url == "":
            quality_url = "undefined"
        plugintools.log("quality_url= "+quality_url)
        plugintools.add_item(action="seriesblanco2", title=params.get("title")+'[COLOR green][B] ['+lang_audio+'] [/COLOR]'+'[COLOR blue] ['+url_server+'][/COLOR][/B]', url = url_capi, thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)

            

def seriesblanco2(params):
    plugintools.log("[blackbox.movie-0.2.0].seriesblanco "+repr(params))
    
    url = params.get("url")
    referer = url
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    
    # onclick='window.open("http://allmyvideos.net/lh18cer7ut8r")
    url_final = plugintools.find_single_match(data, "onclick='window.open(.*?);'/>")
    url_final = url_final.replace('("', "").replace('")', "")
    plugintools.log("url_final= "+url_final)
    params = plugintools.get_params()
    params["url"]=url_final
    getlink_seriesblanco(params)


def getlink_seriesblanco(params):
    plugintools.log("GetLink for SeriesBlanco.com "+repr(params))
    
    url_final = params.get("url")
    
    if url_final.find("allmyvideos") >= 0:
        params["url"]=url_final
        allmyvideos(params)
    elif url_final.find("vidspot") >= 0:
        params["url"]=url_final
        vidspot(params)
    elif url_final.find("streamin.to") >= 0:
        params["url"]=url_final
        streaminto(params)
    elif url_final.find("streamcloud") >= 0:
        params["url"]=url_final
        streamcloud(params)
    elif url_final.find("nowvideo.sx") >= 0:
        params["url"]=url_final
        nowvideo(params)
    elif url_final.find("veehd") >= 0:
        params["url"]=url_final
        veehd(params)     
       

def gethttp_referer_headers(url,referer):
    plugintools.log("blackbox.movie-0.2.0.gethttp_referer_headers ")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
