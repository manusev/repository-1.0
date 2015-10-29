# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de Torrentz.eu
# Version 0.1 (29.12.2014)
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

import re,urllib,urllib2,sys
import plugintools

thumbnail = 'http://www.geekduweb.fr/wp-content/uploads/2010/04/Torrentz.jpg'
fanart = 'https://emptyencore.files.wordpress.com/2011/06/pirate-3.png'


def torrentz(params):
    plugintools.log("[black.box.tv 0.3.0].Torrentz "+repr(params))
    url = 'https://www.torrentz.eu/search?q=the+strain+spanish'
    referer = 'http://www.torrentz.eu/'
    data = gethttp_referer_headers(url,referer)
    matches = plugintools.find_single_match(data, '<div class="results">(.*?)</span></div></body></html>')
    results = plugintools.find_multiple_matches(matches, '<dl><dt><a href="(.*?)</dd></dl>')
    plugintools.add_item(action="", title='[COLOR lightblue][B][I]Torrentz.eu[/I][/B][/COLOR]', url="", thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    for entry in results:
        plugintools.log("entry= "+entry)
        #match = plugintools.find_single_match(entry, '<a href="(.*?)</a>')
        match = entry.replace("<b>", "[B][COLOR gold]").replace("</b>","[/COLOR][/B]").strip()
        results = match.split('"')
        print results
        result_url = 'http://www.torrentz.eu'+results[0]
        result_title = results[1].replace("</dt>", "").replace("<dd>", "").replace(">", "")
        result_title = result_title.split("</a")
        result_title = result_title[0]       
        plugintools.add_item(action="torrentz_links", title='[COLOR white]'+result_title+'[/COLOR]', url=result_url, thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)


def torrentz_links(params):
    plugintools.log("[black.box.tv Torrentz links]"+repr(params))

    url = params.get("url")
    referer = 'http://www.torrentz.eu/'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    matches = plugintools.find_single_match(data, 'Sponsored Link(.*?)<div class="votebox">')
    plugintools.log("matches= "+matches)
    results = plugintools.find_multiple_matches(matches, '<dl><dt>(.*?)</span>')
    plugintools.add_item(action="", title='[COLOR gold][B]Descargar de... [/B][/COLOR]', url="", thumbnail = thumbnail, fanart = fanart, folder=True, isPlayable=False)
    for entry in results:
        plugintools.log("entry= "+entry)
        url_to_get = plugintools.find_single_match(entry, u'<a href="([^"]+)')
        url_to_get = url_to_get.replace("?", "ñ").replace("%C3%B1", "ñ").replace("espa\xc3\xb1ol", "español").replace("Espa%25C3%25B1ol", "Español").replace("espa?ol", "español").replace("espa\xc3\x91ol", "español").replace("ESPA%25C3%2591OL", "ESPAÑOL")       
        plugintools.log("url_to_get= "+url_to_get)
        try:
            server_result = entry.split(">")
            num_items = len(server_result) - 1
            server_result = server_result[num_items]
            if server_result == "":
                if entry.find("kickass") >= 0:
                    server_result = "kickass.to"
                elif entry.find("katproxy") >= 0:
                    server_result = "katproxy.com"
                elif entry.find("monova") >= 0:
                    server_result = "monova.org"
                elif entry.find("limetorrents") >= 0:
                    server_result = "limetorrents"
                elif entry.find("torlock") >= 0:
                    server_result = "torlock.com"
                elif entry.find("bitsnoop") >= 0:
                    server_result = "bitsnoop.com"
                elif entry.find("torrents.net") >= 0:
                    server_result = "torrents.net"
        except:
            pass
                     
        plugintools.log("server_result= "+server_result)
        if url_to_get != "":
            plugintools.add_item(action="torrentz_getmagnet", title=server_result, url=url_to_get, thumbnail = thumbnail, fanart = fanart, folder=True, isPlayable=False)
        


def torrentz_getmagnet(params):
    plugintools.log("black.box.tv torrentz_getmagnet "+repr(params))

    url = params.get("url")    
    if url.find("kickass") >= 0:
        referer = "http://www.kickass.to"
    elif url.find("katproxy") >= 0:
        referer = "http://www.katproxy.com"
    elif url.find("monova") >= 0:
        referer = "http://www.monova.org"
    elif url.find("limetorrents") >= 0:
        referer = "http://www.limetorrents"
    elif url.find("torlock") >= 0:
        referer = "http://www.torlock.com"
    elif url.find("bitsnoop") >= 0:
        referer = "http://www.bitsnoop.com"
    elif url.find("torrents.net") >= 0:
        referer = "http://www.torrents.net"
    else:
        referer = 'http://www.torrentz.eu/'    
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)

    magnet = plugintools.find_multiple_matches(data, 'magnet:?(.*?)"')
    for entry in magnet:
        entry = 'magnet:'+entry
        if entry.find("xt=urn:btih:") >= 0:
            plugintools.add_item(action="launch_torrent", title=params.get("title"), url=entry, folder=False, isPlayable=False)



def launch_torrent(params):
    plugintools.log("URL Magnet= "+repr(params))  # Comprobamos addon reproductor de magnet links y lanzamos vídeo...

    url = params.get("url")
    
    addon_magnet = plugintools.get_setting("addon_magnet");print addon_magnet
    if addon_magnet == "0":  # Stream (por defecto)
        url = 'plugin://plugin.video.stream/play/'+url
        url = url.strip()
        print url
    elif addon_magnet == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url
        url = url.strip()
        print url
    elif addon_magnet == "2":  # Kmediatorrent
        url = 'plugin://plugin.video.kmediatorrent/play/'+url
        url = url.strip()
        print url
        




def gethttp_referer_headers(url,referer):
    plugintools.log("black.box.tv-0.3.0.gethttp_referer_headers ")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return data

