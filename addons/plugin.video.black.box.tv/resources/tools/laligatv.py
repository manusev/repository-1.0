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
import shutil
import zipfile

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


def laligatv(params):
    plugintools.log("[black.box.tv-0.3.0].laligatv.es Playlist Sport Channels( "+repr(params))

    thumbnail = params.get("thumbnail")
    plugintools.log("thumbnail= "+thumbnail)
   
    plugintools.add_item(action="", title = '[B][COLOR blue]Liga Adelante[/B][/COLOR]', url = "", thumbnail = 'https://dl.dropboxusercontent.com/s/5ovesra1r4ddvra/Eventos%20deportivos%20liga%20adelante.jpg' , fanart = 'http://www.sdponferradina.com/documents/30276/30332/Horario+Jornada+Liga+Adelante+blanco/5b72e948-fc08-443c-9fb1-035e35b08e36?t=1380727968000' , folder = True, isPlayable = False)
    plugintools.add_item(action="", title = '[B][COLOR white]Los Canales se activarán 15 minutos antes de cada partido[/B][/COLOR]', url = "", thumbnail = 'https://dl.dropboxusercontent.com/s/5ovesra1r4ddvra/Eventos%20deportivos%20liga%20adelante.jpg' , fanart = 'http://www.sdponferradina.com/documents/30276/30332/Horario+Jornada+Liga+Adelante+blanco/5b72e948-fc08-443c-9fb1-035e35b08e36?t=1380727968000' , folder = True, isPlayable = False)
    
    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")
    plugintools.log("title= "+title)
    data = plugintools.read(url)
    match_total = plugintools.find_single_match(data, 'id=\"coming-soon\"(.*?)fb-root')
    plugintools.log("match_total= "+match_total)
    matches_dia = plugintools.find_single_match(data, 'id=\"coming-soon\"(.*?)</div></div>')
    plugintools.log("matches_dia= "+matches_dia) 
    jornada = plugintools.find_multiple_matches(match_total, 'class=\"title_jornada\">(.*?)</div>')
    #print 'jornada',jornada       
    matches = plugintools.find_multiple_matches(matches_dia, '<a href="(.*?)</a>')
    plugintools.add_item(action="" , title = '[COLOR red][B]' + jornada[0] + '[/B][/COLOR]' , thumbnail = thumbnail , folder = False , isPlayable = False)
    
    for entry in matches:
        plugintools.log("entry= "+entry)
        url_partido = entry.split('"')
        url_partido = url_partido[0]
        url_partido = url_partido.strip()
        if url_partido == "http://www.hyundai.com/":
            url_partido = plugintools.find_single_match(entry, 'a href="([^"]+)')
        plugintools.log("url_partido= "+url_partido)
        hora = plugintools.find_single_match(entry, 'hora_partido_otras_competiciones\">(.*?)</span>')
        plugintools.log("hora= "+hora)
        local = plugintools.find_single_match(entry, 'equipo_local_otras_competiciones\">(.*?)</span>')
        visitante = plugintools.find_single_match(entry, 'equipo_visitante_otras_competiciones\">(.*?)</span>')
        plugintools.log("local= "+local)
        plugintools.log("viistante= "+visitante)
        plugintools.add_item(action="adelante_geturl" , title = '[COLOR blue][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' - ' + visitante + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)

    if len(jornada) >= 2:
        plugintools.add_item(action="" , title = '[COLOR red][B]' + jornada[1] + '[/B][/COLOR]' , thumbnail = thumbnail , folder = False , isPlayable = False)
        matches_dia = plugintools.find_single_match(match_total, jornada[1]+'(.*?)</div></div>')
        plugintools.log("matches_dia= "+matches_dia)
        matches = plugintools.find_multiple_matches(matches_dia, '<a href="(.*?)</a>')
        for entry in matches:
            plugintools.log("entry= "+entry)
            url_partido = entry.split('"')
            url_partido = url_partido[0]
            url_partido = url_partido.strip()
            plugintools.log("url_partido= "+url_partido)
            hora = plugintools.find_single_match(entry, 'hora_partido_otras_competiciones\">(.*?)</span>')
            plugintools.log("hora= "+hora)
            local = plugintools.find_single_match(entry, 'equipo_local_otras_competiciones\">(.*?)</span>')
            visitante = plugintools.find_single_match(entry, 'equipo_visitante_otras_competiciones\">(.*?)</span>')
            plugintools.log("local= "+local)
            plugintools.log("viistante= "+visitante)
            plugintools.add_item(action="adelante_geturl" , title = '[COLOR blue][B](' + hora + ')[/B][/COLOR][COLOR white] ' + local + ' - ' + visitante + ' [/COLOR]' , url = url_partido , thumbnail = params.get("thumbnail") , folder = False , isPlayable = True)       
    
        
               


def adelante_geturl(params):
    plugintools.log("[black.box.tv-0.3.0].LaLigatv.es getURL: "+repr(params))

    data = plugintools.read(params.get("url"))
    plugintools.log("data= "+data)
    url = plugintools.find_single_match(data, 'src: escape\(\"(.*?)\"')    
    plugintools.log("URL= "+url)
    plugintools.play_resolved_url(url)
        
        
