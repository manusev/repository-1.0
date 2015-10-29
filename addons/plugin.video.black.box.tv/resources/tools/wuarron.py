# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Regex de Wuarron
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

from __main__ import *

# Módulos EPG
from resources.tools.epg_miguiatv import *
from resources.tools.epg_ehf import *
from resources.tools.epg_arenasport import *
from resources.tools.epg_formulatv import *

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")


__fanart__ = 'http://dl.dropbox.com/s/r61p9v1vczcq2wj/fondo410.jpg'


def wuarronlin0(params):
    plugintools.log("Iniciando WuarronParser..."+repr(params))

    plugintools.modo_vista("list")
	
    thumbnail =  params.get("thumbnail")
    datamovie = {}

    url = 'https://dl.dropbox.com/s/rr7tuzez9g71dlx/PrinciBlack.m3u'
    
    try:
        response = urllib2.urlopen(url)
        body = response.read()
        #plugintools.log("body= "+body)        
    except:
        pass

    # Control modo de vista 
    if body.find("#EXTM3U") >= 0:  
        data = body.split(",")
        if len(data) >= 2:
            show = data[1].strip()
        if show == "":
            show = "LIST"
            plugintools.log("No hay modo de vista predefinido")
        else:
            plugintools.log("show en #EXTM3U: "+show)

    matches = plugintools.find_multiple_matches(body, '#EXTINF:-1,(.*?)m3u8')
    plugintools.add_item(action="", plot="", title='[COLOR blue][B]Digital + [/COLOR][COLOR white]...[COLOR green] Exclusivo en BlackBoxTV[/B][/COLOR]', url="", thumbnail = thumbnail , extra=show, fanart = __fanart__, folder = False, isPlayable = True)

    # Parche para solucionar un bug por el cuál el diccionario params no retorna la variable fanart
    fanart = params.get("extra")
    if fanart == " " :
        fanart = params.get("fanart")
        if fanart == " " :
            fanart = art + 'fanart.png'

    for entry in matches:
        #plugintools.log("entry= "+entry)
        title_line = plugintools.find_single_match(entry, '(.*?)\n')
        plugintools.log("title_line= "+title_line)
        items = []
        items = m3u_items(title_line)
        print items
        title_channel = entry.split(",")
        title_channel = title_channel[0]
        if title_channel.startswith("@") == True:  # Ejecutamos EPG...
            if plugintools.get_setting("epg_no") == "true":
                title_channel = title_channel.replace("@","")                    
                plugintools.log('[%s %s] EPG desactivado ' % (addonName, addonVersion))
                if show == "":
                    plugintools.get_setting("video_id")                                        
            else:
                title_channel = title_channel.replace("@","")
                if show == "":
                    plugintools.get_setting("video_id")
                #plugintools.modo_vista(show)
                epg_channel = []
                epg_source = plugintools.get_setting("epg_source")
                plugintools.log("Fuente EPG = "+epg_source)
                if epg_source == "0":  # FórmulaTV
                    epg_channel = epg_ftv(title_channel)
                    print 'EPG:',epg_channel
                    if epg_channel != False:
                        try:
                            ejemplo = epg_channel[0]
                            print epg_channel[0]
                            title_channel = title_channel + " [COLOR red][B] " + epg_channel[0] + "[COLOR blue] " + epg_channel[1] + "[/B][/COLOR] "
                            plot = "[COLOR red][B]" + epg_channel[2].strip() + "[/B][B][COLOR blue] " + epg_channel[4].strip() + " [/B][/COLOR][B][COLOR white]("+epg_channel[3].strip() + ")[/B][/COLOR][B][CR]" + epg_channel[5].strip()+"[COLOR blue][/B][/COLOR] "+ epg_channel[6].strip()
                            datamovie["Plot"]=plot
                        except:
                            plot = ""
                            pass                        
                elif epg_source == "1":  # MiguíaTV
                    epg_channel = epg_now(title)
                    print 'EPG:',epg_channel                            
                    try:
                        title_channel = title_channel + " [COLOR orange][I][B] " + epg_channel[0] + "[/B][COLOR lightyellow] " + epg_channel[1] + "[/I][/COLOR] "
                        plot = "[COLOR white][I]" + epg_channel[2].strip() + " " + epg_channel[3].strip() + "[CR]"+ epg_channel[4].strip() + " " + epg_channel[5].strip()+"[CR]"+ epg_channel[6].strip() + " " + epg_channel[7].strip()+"[CR]"+ epg_channel[8].strip() + " " + epg_channel[9].strip()+"[/I][/COLOR] "
                        datamovie["Plot"]=plot
                    except:
                        plot = ""
                        pass            
            
        plugintools.log("title_channel= "+title_channel)
        url_channel = plugintools.find_single_match(entry, '\n(.*?)index')
        url_channel = url_channel+'index.m3u8'
        url_fixed = url_channel.split("/")
        channel_id = url_fixed[3]
        plugintools.log("url_channel= "+url_channel)
        thumbnail = items[0]
        fanart = items[1]
        plugintools.add_item(action="wuarron_token", plot=channel_id, title='[COLOR white]'+title_channel+'[/COLOR] [COLOR gold][/COLOR]', info_labels=datamovie, url=url_channel, thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = True)
        datamovie["Plot"]=""

    plugintools.modo_vista("list")    

    try:
        if os.path.exists(tmp + 'backup_ftv.txt'):
            os.remove(tmp + 'backup_ftv.txt')
    except: pass
        


def m3u_items(title):
    plugintools.log("[black.box.tv-0.3.0].m3u_items= "+title)

    plugintools.modo_vista("list")

    thumbnail = art + 'icon.png'
    fanart = art + 'fanart.jpg'
    only_title = title

    if title.find("tvg-logo") >= 0:
        thumbnail = re.compile('tvg-logo="(.*?)"').findall(title)
        num_items = len(thumbnail)
        print 'num_items',num_items
        if num_items == 0:
            thumbnail = 'm3u.png'
        else:
            thumbnail = thumbnail[0]
            #plugintools.log("thumbnail= "+thumbnail)

        only_title = only_title.replace('tvg-logo="', "")
        only_title = only_title.replace(thumbnail, "")

    if title.find("tvg-wall") >= 0:
        fanart = re.compile('tvg-wall="(.*?)"').findall(title)
        fanart = fanart[0]
        only_title = only_title.replace('tvg-wall="', "")
        only_title = only_title.replace(fanart, "")

    try:
        if title.find("imdb") >= 0:
            imdb = re.compile('imdb="(.*?)"').findall(title)
            imdb = imdb[0]
            only_title = only_title.replace('imdb="', "")
            only_title = only_title.replace(imdb, "")
        else:
            imdb = ""
    except:
        imdb = ""

    try:
        if title.find("dir") >= 0:
            dir = re.compile('dir="(.*?)"').findall(title)
            dir = dir[0]
            only_title = only_title.replace('dir="', "")
            only_title = only_title.replace(dir, "")
        else:
            dir = ""
    except:
        dir = ""

    try:
        if title.find("wri") >= 0:
            writers = re.compile('wri="(.*?)"').findall(title)
            writers = writers[0]
            only_title = only_title.replace('wri="', "")
            only_title = only_title.replace(writers, "")
        else:
            writers = ""
    except:
        writers = ""

    try:
        if title.find("votes") >= 0:
            num_votes = re.compile('votes="(.*?)"').findall(title)
            num_votes = num_votes[0]
            only_title = only_title.replace('votes="', "")
            only_title = only_title.replace(num_votes, "")
        else:
            num_votes = ""
    except:
        num_votes = ""

    try:
        if title.find("plot") >= 0:
            plot = re.compile('plot="(.*?)"').findall(title)
            plot = plot[0]
            only_title = only_title.replace('plot="', "")
            only_title = only_title.replace(plot, "")
        else:
            plot = ""
    except:
        plot = ""

    try:
        if title.find("genre") >= 0:
            genre = re.compile('genre="(.*?)"').findall(title)
            genre = genre[0]
            only_title = only_title.replace('genre="', "")
            only_title = only_title.replace(genre, "")
            print 'genre',genre
        else:
            genre = ""
    except:
        genre = ""

    try:
        if title.find("time") >= 0:
            duration = re.compile('time="(.*?)"').findall(title)
            duration = duration[0]
            only_title = only_title.replace('time="', "")
            only_title = only_title.replace(duration, "")
            print 'duration',duration
        else:
            duration = ""
    except:
        duration = ""

    try:
        if title.find("year") >= 0:
            year = re.compile('year="(.*?)"').findall(title)
            year = year[0]
            only_title = only_title.replace('year="', "")
            only_title = only_title.replace(year, "")
            print 'year',year
        else:
            year = ""
    except:
        year = ""

    if title.find("group-title") >= 0:
        cat = re.compile('group-title="(.*?)"').findall(title)
        if len(cat) == 0:
            cat = ""
        else:
            cat = cat[0]
        plugintools.log("m3u_categoria= "+cat)
        only_title = only_title.replace('group-title=', "")
        only_title = only_title.replace(cat, "")
    else:
        cat = ""

    if title.find("tvg-id") >= 0:
        title = title.replace('”', '"')
        title = title.replace('“', '"')
        tvgid = re.compile('tvg-id="(.*?)"').findall(title)
        print 'tvgid',tvgid
        tvgid = tvgid[0]
        plugintools.log("m3u_categoria= "+tvgid)
        only_title = only_title.replace('tvg-id=', "")
        only_title = only_title.replace(tvgid, "")
    else:
        tvgid = ""

    if title.find("tvg-name") >= 0:
        tvgname = re.compile('tvg-name="(.*?)').findall(title)
        tvgname = tvgname[0]
        plugintools.log("m3u_categoria= "+tvgname)
        only_title = only_title.replace('tvg-name=', "")
        only_title = only_title.replace(tvgname, "")
    else:
        tvgname = ""

    only_title = only_title.replace('"', "").strip()

    plugintools.modo_vista("list")

    return thumbnail, fanart, cat, only_title, tvgid, tvgname, imdb, duration, year, dir, writers, genre, num_votes, plot




def wuarron_token(params):
    plugintools.log("Capturando parámetros..."+repr(params))

    plugintools.modo_vista("list")

    # 15:08:04 T:5944  NOTICE: DVDPlayer: Opening: http://94.23.217.50:2082/digitv-canal2/index.m3u8?st=KvM1G2R1Yeypg52q3uxTtA&e=1430154483
    # 15:10:09 T:5944  NOTICE: DVDPlayer: Opening: http://94.23.217.50:2082/digitv-canal2/index.m3u8?st=AUCqF0evqHhUzYpdgpusdg&e=1430154608
    
    url_fixed = params.get("url")
    channel_id = params.get("plot")

    url = 'http://aperezjimenez423.premiumhostingweb.com/secure-json.php?channel='+channel_id
    referer = 'http://aperezjimenez423.premiumhostingweb.com/'
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)
    channel_id = plugintools.find_single_match(data, '"channel":"([^"]+)')
    token_id = plugintools.find_single_match(data, '"token":"([^"]+)')
    expire_id = plugintools.find_single_match(data, '"expire":"([^"]+)')
    url = url_fixed+'?st='+token_id+'&e='+expire_id
    url=url.strip()
    print url
    plugintools.play_resolved_url(url)
    




def gethttp_referer_headers(url,referer):
    plugintools.modo_vista("list")
    
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    return data
