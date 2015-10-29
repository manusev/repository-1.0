# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de Kickasstorrents.to
# Version 0.1 (01.12.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info)

from __main__ import *

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

import re,urllib,urllib2,sys
import plugintools,ioncube



thumbnail = 'http://static.myce.com/images_posts/2011/04/kickasstorrents-logo.jpg'
#fanart = 'http://i.imgur.com/LaeHXnR.png'
fanart = 'https://yuq.me/users/19/529/lcqO6hj0XK.png'



def bum(params):
    plugintools.log("[black.box.tv 0.3.0].BUM+" +repr(params))

    try:
        texto = params.get("title")
        texto = texto.replace("[Multiparser]", "").replace("[/COLOR]", "").replace("[I]", "").replace("[/I]", "").replace("[COLOR white]", "").replace("[COLOR lightyellow]", "").strip()
        texto = texto+' spanish'
        plugintools.set_setting("bum_search",texto)
        params["plot"]=texto
        texto = texto.lower().strip()
        texto = texto.replace(" ", "+")
        if texto == "":
            errormsg = plugintools.message("Black Box TV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            url = 'https://kickass.to/usearch/'+texto+'/'  # Kickass
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.kickass.to'
            kickass_results(params)
            url = 'http://bitsnoop.com/search/all/'+texto+'/c/d/1/'  # BitSnoop
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.bitsnoop.com'
            bitsnoop1(params)
            url = 'https://isohunt.to/torrents/?ihq='+texto+'&Torrent_sort=seeders.desc'  # Isohunt
            params["url"]=url            
            url = params.get("url")
            referer = 'https://isohunt.to'
            isohunt1(params)
            url = 'https://www.monova.org/search.php?sort=5&term='+texto+'&verified=1'  # Monova
            params["url"]=url            
            url = params.get("url")
            referer = 'https://monova.org'
            monova1(params) 

    except:
         pass  


def kickasstorrents(params):
    plugintools.log("[black.box.tv 0.3.0].KickassTorrents" +repr(params))

    try:
        texto = "";
        #texto='riddick'
        texto = plugintools.keyboard_input(texto, "Buscador Unificado de Torrents (BUM+)")
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Black Box TV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:           
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            # https://kickass.to/usearch/birdman%20lang_id:14/
            url = 'https://kickass.to/usearch/'+texto+'/'
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.kickass.to'            
    except:
         pass      

    # Archivo de control de resultados (evita la recarga del cuadro de diálogo de búsqueda tras cierto tiempo)
    bumfile = tmp + 'bum.dat'
    if not os.path.isfile(bumfile):  # Si no existe el archivo de control, se crea y se registra la búsqueda
        controlbum = open(bumfile, "a")
        controlbum.close()
        ahora = datetime.now()
        print 'ahora',ahora
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        controlbum = open(tmp + 'bum.dat', "wb")
        controlbum.seek(0)
        controlbum.write(timestamp+":"+texto)
        controlbum.close()
    else:
        controlbum = open(tmp + 'bum.dat', "r")
        controlbum.seek(0)
        data = controlbum.readline()
        controlbum.close()        
        plugintools.log("BUM+= "+data)           
        plugintools.log("Control de BUM+ activado. Analizamos timestamp...")
        data = data.split(":")
        timestamp = data[0]
        term_search = data[1]
        ahora = datetime.now()
        print 'ahora',ahora
        anno_actual = ahora.year
        mes_actual = ahora.month
        hora_actual = ahora.hour
        min_actual = ahora.minute
        seg_actual = ahora.second
        hoy = ahora.day
        # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
        if hoy <= 9:
            hoy = "0" + str(hoy)
        if mes_actual <= 9:
            mes_actual = "0" + str(ahora.month)
        timenow = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
        # Comparamos valores (hora actual y el timestamp del archivo de control)
        if term_search == texto:
            result = int(timenow) - int(timestamp)
            print 'result',result
            if result > 90:  # Control fijado en 90 segundos; esto significa que una misma búsqueda no podremos realizarla en menos de 90 segundos, y en ese tiempo debe reproducirse el torrent
                # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
                ahora = datetime.now()
                print 'ahora',ahora
                anno_actual = ahora.year
                mes_actual = ahora.month
                hora_actual = ahora.hour
                min_actual = ahora.minute
                seg_actual = ahora.second
                hoy = ahora.day
                # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
                if hoy <= 9:
                    hoy = "0" + str(hoy)
                if mes_actual <= 9:
                    mes_actual = "0" + str(ahora.month)
                timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
                controlbum = open(tmp + 'bum.dat', "wb")
                controlbum.seek(0)
                controlbum.write(timestamp+":"+texto)
                controlbum.close()                
                kickass_results(params)
            else:
                plugintools.log("Recarga de página")
                kickass_results(params)
        else:
            # Borramos registro actual y guardamos el nuevo (crear una función que haga esto y no repetir!)
            ahora = datetime.now()
            print 'ahora',ahora
            anno_actual = ahora.year
            mes_actual = ahora.month
            hora_actual = ahora.hour
            min_actual = ahora.minute
            seg_actual = ahora.second
            hoy = ahora.day
            # Si el día o mes está entre el 1 y 9, nos devuelve un sólo dígito, así que añadimos un 0 (cero) delante:
            if hoy <= 9:
                hoy = "0" + str(hoy)
            if mes_actual <= 9:
                mes_actual = "0" + str(ahora.month)
            timestamp = str(ahora.year) + str(mes_actual) + str(hoy) + str(hora_actual) + str(min_actual) + str(seg_actual)
            controlbum = open(tmp + 'bum.dat', "wb")
            controlbum.seek(0)
            controlbum.write(timestamp+":"+texto)
            controlbum.close()                
            kickass_results(params)
                
                
                
def kickass_results(params):
    plugintools.log("black.box.tv Kickass Results "+repr(params))

    show = 'movies'

    plugintools.add_item(action="", title= '[COLOR green][B]KickAss[/COLOR][COLOR gold][I] Torrents[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    #plugintools.add_item(action="", title= '[COLOR red][B]Título [/COLOR][COLOR white] (Tamaño) [/COLOR]   [/B][COLOR lightyellow][I](Semillas)[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://kickass.to/'

    data = gethttp_referer_headers(url,referer)
    logo = plugintools.find_single_match(data, '<img src="([^"]+)')
    logo = 'http:'+logo
    plugintools.log("logo= "+logo)        

    match_num_results = plugintools.find_single_match(data, '<div><h2>(.*?)</a></h2>')
    num_results = plugintools.find_single_match(match_num_results, '<span>(.*?)</span>')
    num_results = num_results.replace("from", "de").replace("results", "Resultados:").strip()
    plugintools.log("num_results= "+num_results)
    results = plugintools.find_single_match(data, '<table width="100%" cellspacing="0" cellpadding="0" class="doublecelltable" id="mainSearchTable">(.*?)</table>')
    plugintools.log("results_table= "+results)
    matches = plugintools.find_multiple_matches(results, '<div class="torrentname">(.*?)<a title="Download torrent file')
    for entry in matches:
        plugintools.log("entry= "+entry)
        match_title = plugintools.find_single_match(entry, 'class="cellMainLink">(.*?)</a>')
        match_title = match_title.replace("</strong>", "").replace("<strong>", "").replace('<strong class="red">', "").strip()        
        plugintools.log("match_title= "+match_title)        
        magnet_match = plugintools.find_single_match(entry, 'Torrent magnet link" href="([^"]+)')
        plugintools.log("magnet_match= "+magnet_match)
        magnet_match = urllib.quote_plus(magnet_match).strip()
        addon_magnet = plugintools.get_setting("addon_magnet")
        if addon_magnet == "0":  # Stream (por defecto)
            magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
            magnet_url = magnet_url.strip()
        elif addon_magnet == "1":  # Pulsar
            magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
            magnet_url = magnet_url.strip()
        elif addon_magnet == "2":  # KMediaTorrent
            magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
            magnet_url = magnet_url.strip()
        plugintools.log("magnet_url= "+magnet_url)        
        size = plugintools.find_single_match(entry, 'class=\"nobr center\">(.*?)</td>')
        size = size.replace("<span>","").replace("</span>","").strip()
        plugintools.log("size= "+size)
        seeds = plugintools.find_single_match(entry, '<td class="green center">(.*?)</td>')
        leechs = plugintools.find_single_match(entry, '<td class="red lasttd center">(.*?)</td>')
        plugintools.log("seeds= "+seeds)
        plugintools.log("leechs= "+leechs)  
        plugintools.add_item(action="play", title='[COLOR gold][I]['+seeds+'/'+leechs+'][/I][/COLOR] [COLOR white] '+match_title+' [/COLOR] [COLOR lightyellow][I]['+size + '][/I][/COLOR]', url=magnet_url, thumbnail = logo , fanart = fanart , show = show , extra = show , folder=False, isPlayable=False)

                            

def bitsnoop0(params):
    plugintools.log("[black.box.tv 0.3.0].BitSnoop" +repr(params))

    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Black Box TV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # http://bitsnoop.com/search/all/the+strain+spanish/c/d/1/
            url = 'http://bitsnoop.com/search/all/'+texto+'/c/d/1/'
            params["url"]=url            
            url = params.get("url")
            referer = 'http://www.bitsnoop.com'
            bitsnoop1(params)
    except:
         pass    




def bitsnoop1(params):
    plugintools.log("black.box.tv BitSnoop Results "+repr(params))

    thumbnail = 'http://upload.wikimedia.org/wikipedia/commons/9/97/Bitsnoop.com_logo.png'
    fanart = 'http://wallpoper.com/images/00/41/86/68/piracy_00418668.jpg'
    show = 'movies'

    plugintools.add_item(action="", title= '[COLOR green][B]Bit[/COLOR][COLOR gold][I]Snoop[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://bitsnoop.com/'

    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    results = plugintools.find_single_match(data, '<ol id="torrents" start="1">(.*?)</ol>')
    matches = plugintools.find_multiple_matches(results, '<span class="icon cat_(.*?)</div></td>')
    i = 0
    for entry in matches:
        plugintools.log("entry= "+entry)
        i = i + 1
        print i
        page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
        title_url = plugintools.find_single_match(entry, 'a href="(.*?)</a>')
        title_url = title_url.replace(page_url, "").replace("<span class=srchHL>", "").replace('">', "").replace("<b class=srchHL>", "[COLOR lightyellow][B]").replace("</b>", "[/COLOR][/B]").strip()
        page_url = 'http://bitsnoop.com'+page_url
        plugintools.log("title_url= "+title_url)
        plugintools.log("page_url= "+page_url)
        seeders = plugintools.find_single_match(entry, 'title="Seeders">(.*?)</span>')
        plugintools.log("seeders= "+seeders)
        leechers = plugintools.find_single_match(entry, 'title="Leechers">(.*?)</span>')
        size = plugintools.find_single_match(entry, '<tr><td align="right" valign="middle" nowrap="nowrap">(.*?)<div class="nfiles">')
        plugintools.log("size= "+size)
        plugintools.log("leechers= "+leechers)        
        if seeders == "":  # Verificamos el caso en que no haya datos de seeders/leechers
            seeders = "0"
        if leechers == "":
            leechers = "0"            
        stats = '[COLOR lightyellow][I]['+seeders+'/'+leechers+'][/I][/COLOR]'
        plugintools.add_item(action="bitsnoop2", title= stats+'  '+title_url+' [COLOR lightgreen][I]['+size+'][/I][/COLOR]', url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)        
        



def bitsnoop2(params):
    plugintools.log("black.box.tv BitSnoop GetLink "+repr(params))

    
    url = params.get("url")
    referer = 'https://bitsnoop.com/'
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    magnet_match = urllib.quote_plus(magnet_match).strip()    
    addon_magnet = plugintools.get_setting("addon_magnet")    
    if addon_magnet == "0":  # Stream (por defecto)
        magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "1":  # Pulsar
        magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "2":  # KMediaTorrent
        magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
        magnet_url = magnet_url.strip()

    plugintools.log("magnet_url= "+magnet_url)
    play(magnet_url)



def isohunt0(params):
    plugintools.log("black.box.tv Isohunt "+repr(params))

    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg'    
    show = 'movies'
    
    try:
        texto = "";
        texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Black Box TV","Por favor, introduzca el canal a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://isohunt.to/torrents/?ihq='+texto+'&Torrent_sort=seeders.desc'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://isohunt.to'
            isohunt1(params)
    except:
         pass       


def isohunt1(params):
    plugintools.log("black.box.tv Isohunt Results "+repr(params))

    thumbnail = 'http://www.userlogos.org/files/logos/dfordesmond/isohunt%201.png'
    fanart = 'http://2.bp.blogspot.com/_NP40rzexJsc/TMGWrixybJI/AAAAAAAAHCU/ij1--_DQEZo/s1600/Keep_Seeding____by_Carudo.jpg' 
    show = 'movies'

    plugintools.add_item(action="", title= '[COLOR blue][B]Iso[/COLOR][COLOR lightblue][I]Hunt[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://isohunt.to/'

    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    #plugintools.log("data= "+data)
    matches = plugintools.find_multiple_matches(data, '<tr data-key="(.*?)</td></tr>')    
    for entry in matches:
        plugintools.log("entry= "+entry)
        page_url = plugintools.find_single_match(entry, '<a href="([^"]+)')
        page_url = 'https://isohunt.to'+page_url
        title_url = plugintools.find_single_match(entry, '<span>(.*?)</span>')
        plugintools.log("title_url= "+title_url)
        plugintools.log("page_url= "+page_url)
        size = plugintools.find_single_match(entry, '<td class="size-row">(.*?)</td>')
        plugintools.log("size= "+size)
        category = plugintools.find_single_match(entry, 'title="([^"]+)')
        plugintools.log("category= "+category)
        if entry.find("Verified Torrent") >= 0:
            verified = '[COLOR lightgreen][I][Verified][/I][/COLOR]'
            plugintools.log("verified yes")
            if category != "":
                if category == "movies":
                    category = "Películas"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "series & tv":
                    category = "Series TV"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "books":
                    category = "Libros/Comics"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "adult":
                    category = "Adultos"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "anime":
                    category = "Anime"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "other":
                    category = "Otros"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)                                        
            else:                
                plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url+'  '+verified, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
        else:
            if category != "":
                if category == "movies":
                    category = "Películas"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "series & tv":
                    category = "Series TV"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "books":
                    category = "Libros/Comics"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "adult":
                    category = "Adultos"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "anime":
                    category = "Anime"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
                elif category == "other":
                    category = "Otros"
                    plugintools.add_item(action="isohunt2", title= '[COLOR gold][B]'+category+'[/B][/COLOR] '+title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)
            else:
                plugintools.add_item(action="isohunt2", title= title_url, url = page_url , thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable = False)        
            
            

def isohunt2(params):
    plugintools.log("black.box.tv IsoHunt GetLink "+repr(params))
    
    url = params.get("url")
    referer = 'https://isohunt.to/'
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    magnet_match = urllib.quote_plus(magnet_match).strip()    
    addon_magnet = plugintools.get_setting("addon_magnet")    
    if addon_magnet == "0":  # Stream (por defecto)
        magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "1":  # Pulsar
        magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "2":  # KMediaTorrent
        magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
        magnet_url = magnet_url.strip()

    plugintools.log("magnet_url= "+magnet_url)
    play(magnet_url)



def monova0(params):
    plugintools.log("black.box.tv Isohunt "+repr(params))

    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    show = 'movies'
    
    try:
        texto = "";
        texto='the strain spanish'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()
        if texto == "":
            errormsg = plugintools.message("Black Box TV","Por favor, introduzca el término a buscar")
            #return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            
            # https://isohunt.to/torrents/?ihq=the+strain+spanish
            url = 'https://www.monova.org/search.php?sort=5&term='+texto+'&verified=1'
            params["url"]=url            
            url = params.get("url")
            referer = 'https://monova.org'
            monova1(params)
    except:
         pass       


def monova1(params):
    plugintools.log("black.box.tv Monova.org Results "+repr(params))

    thumbnail = 'http://upload.wikimedia.org/wikipedia/en/f/f4/Monova.jpg'
    fanart = 'http://www.gadgethelpline.com/wp-content/uploads/2013/10/Digital-Piracy.png'    
    show = 'movies'

    plugintools.add_item(action="", title= '[COLOR blue][B]M[/COLOR][COLOR lightblue][I]onova.org[/I][/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    
    url = params.get("url")
    referer = 'https://monova.org/'

    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    block_matches = plugintools.find_single_match(data, '<table id="resultsTable"(.*?)<div id="hh"></div>')
    plugintools.log("block_matches= "+block_matches)
    matches = plugintools.find_multiple_matches(block_matches, '<div class="torrentname(.*?)</div></td></tr>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        if entry.find("Direct Download") >= 0:  # Descartamos resultados publicitarios 'Direct Download' que descargan un .exe
            plugintools.log("Direct Download = Yes")
        else:
            plugintools.log("Direct Download = No")
            page_url = plugintools.find_single_match(entry, 'a href="([^"]+)')
            title_url = plugintools.find_single_match(entry, 'title="([^"]+)')
            size_url = plugintools.find_single_match(entry, '<div class="td-div-right pt1">(.*?)</div>')
            seeds = plugintools.find_single_match(entry, '<td class="d">(.*?)<td align="right" id="encoded-')
            seeds = seeds.replace("</td>", "")
            seeds = seeds.split('<td class="d">')
            #seeds = seeds.replace('<td align="right" id="encoded-10"', "")
            #seeds = seeds.replace('<td id="encoded-10" align="right"', "")
            try:
                print 'seeds',seeds
                if len(seeds) >= 2:
                    semillas = '[COLOR lightyellow][I]['+seeds[0]+'/'+seeds[1]+'][/I][/COLOR]'
                    plugintools.log("semillas= "+semillas)                
            except:
                pass
        
            plugintools.log("page_url= "+page_url)
            plugintools.log("title_url= "+title_url)
            plugintools.log("size_url= "+size_url)
            plugintools.add_item(action="monova2", title = semillas+'  '+title_url+' [COLOR lightgreen][I][ '+size_url+'][/I][/COLOR] ', url = page_url , thumbnail = thumbnail , fanart = fanart , folder = True, isPlayable = False)  
            
            

def monova2(params):
    plugintools.log("black.box.tv Monova.org GetLink "+repr(params))
    
    url = params.get("url")
    referer = 'https://monova.org/'
    data = gethttp_referer_headers(url,referer)  #Todo: Añadir modo de vista (show)
    plugintools.log("data= "+data)
    magnet_match = plugintools.find_single_match(data, '<a href="magnet([^"]+)')
    magnet_match = 'magnet'+magnet_match
    plugintools.log("Magnet: "+magnet_match)
    magnet_match = urllib.quote_plus(magnet_match).strip()    
    addon_magnet = plugintools.get_setting("addon_magnet")    
    if addon_magnet == "0":  # Stream (por defecto)
        magnet_url = 'plugin://plugin.video.stream/play/'+magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "1":  # Pulsar
        magnet_url = 'plugin://plugin.video.pulsar/play?uri=' + magnet_match
        magnet_url = magnet_url.strip()
    elif addon_magnet == "2":  # KMediaTorrent
        magnet_url = 'plugin://plugin.video.kmediatorrent/play/' + magnet_match
        magnet_url = magnet_url.strip()

    plugintools.log("magnet_url= "+magnet_url)
    play(magnet_url)    

    

def gethttp_headers(url):
    plugintools.log("black.box.tv-0.3.0.gethttp_referer_headers "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return data

def gethttp_referer_headers(url,referer):
    plugintools.log("black.box.tv-0.3.0.gethttp_referer_headers "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer",referer])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return data
        


def parser_title(title):
    plugintools.log("[black.box.tv-0.3.0].parser_title " + title)

    cyd = title

    cyd = cyd.replace("[COLOR lightyellow]", "")
    cyd = cyd.replace("[COLOR green]", "")
    cyd = cyd.replace("[COLOR red]", "")
    cyd = cyd.replace("[COLOR blue]", "")    
    cyd = cyd.replace("[COLOR royalblue]", "")
    cyd = cyd.replace("[COLOR white]", "")
    cyd = cyd.replace("[COLOR pink]", "")
    cyd = cyd.replace("[COLOR cyan]", "")
    cyd = cyd.replace("[COLOR steelblue]", "")
    cyd = cyd.replace("[COLOR forestgreen]", "")
    cyd = cyd.replace("[COLOR olive]", "")
    cyd = cyd.replace("[COLOR khaki]", "")
    cyd = cyd.replace("[COLOR lightsalmon]", "")
    cyd = cyd.replace("[COLOR orange]", "")
    cyd = cyd.replace("[COLOR lightgreen]", "")
    cyd = cyd.replace("[COLOR lightblue]", "")
    cyd = cyd.replace("[COLOR lightpink]", "")
    cyd = cyd.replace("[COLOR skyblue]", "")
    cyd = cyd.replace("[COLOR darkorange]", "")    
    cyd = cyd.replace("[COLOR greenyellow]", "")
    cyd = cyd.replace("[COLOR yellow]", "")
    cyd = cyd.replace("[COLOR yellowgreen]", "")
    cyd = cyd.replace("[COLOR orangered]", "")
    cyd = cyd.replace("[COLOR grey]", "")
    cyd = cyd.replace("[COLOR gold]", "")
    cyd = cyd.replace("[COLOR=FF00FF00]", "")  
                
    cyd = cyd.replace("[/COLOR]", "")
    cyd = cyd.replace("[B]", "")
    cyd = cyd.replace("[/B]", "")
    cyd = cyd.replace("[I]", "")
    cyd = cyd.replace("[/I]", "")
    cyd = cyd.replace("[Auto]", "")
    cyd = cyd.replace("[Parser]", "")    
    cyd = cyd.replace("[TinyURL]", "")
    cyd = cyd.replace("[Auto]", "")

    # Control para evitar filenames con corchetes
    cyd = cyd.replace(" [Lista M3U]", "")
    cyd = cyd.replace(" [Lista PLX]", "")
    cyd = cyd.replace(" [Multilink]", "")

    title = cyd
    title = title.strip()
    if title.endswith(" .plx") == True:
        title = title.replace(" .plx", ".plx")
        
    plugintools.log("title_parsed= "+title)
    return title        



