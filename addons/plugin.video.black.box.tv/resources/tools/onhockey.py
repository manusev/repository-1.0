# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de onhockey.tv
# Version 0.1 (01.12.2014)
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

import re,urllib,urllib2,sys
import plugintools,ioncube


thumbnail = 'http://cs419622.vk.me/v419622246/ad9a/6lhLpe59E2Q.jpg'
fanart = 'http://www.visitwatertownsd.com/wp-content/uploads/Hockey.jpg'



def onhockey(params):
    plugintools.log("[black.box.tv 0.3.0].Onhockey")

    plugintools.add_item(action="", title= '[COLOR red][B] O N  [/COLOR][COLOR blue] H O C K E Y[/COLOR][COLOR white]  T V[/COLOR]   [/B][COLOR lightyellow][I]By Juarrox[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    plugintools.add_item(action="", title= '[COLOR lightgreen][B]03.01.15 [/B][/COLOR][I][COLOR lightyellow]Operativos SOLO los enlaces de Sawlive y Castalba[/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)    

    # Vamos a obtener la programación de VipRacing
    url = 'http://onhockey.tv/schedule_table_eng.php'
    referer = 'http://www.onhockey.tv/'

    schedule = gethttp_referer_headers(url,referer)
    #plugintools.log("programación?= "+schedule)

    # Obtenemos lista de canales y su clave
    eventos = plugintools.find_multiple_matches(schedule, '<tr>(.*?)</tr>')
    for entry in eventos:
        canales_dict = []
        tipo_dict = []
        plugintools.log("EVENTO= "+entry)
        #<tr><td><text class="game_hour" align="left">00</text>:00</td><td>Philadelphia - New Jersey</td>
        hora = plugintools.find_single_match(entry, '<td>(.*?)</td><td>')
        hora = hora.replace("<text class='game_hour' align='left'>","")
        hora = hora.replace("</text>", "")
        plugintools.log("hora= "+hora)
        partido = plugintools.find_single_match(entry, '</td><td>(.*?)</td><td align="right">')
        title_fixed = partido.replace(" \x96 "," vs ")
        title_fixed = title_fixed.replace(" - "," vs ")
        partido = partido.replace("vs","")
        partido = partido.replace("-","")
        partido = partido.replace("\x96","")
        partido = partido.replace(" ","")
        plugintools.log("partido= "+partido)
        file = open(tmp + partido + '.txt', "wb")
        channels = plugintools.find_multiple_matches(entry, "<a(.*?)<br>")
        # Guardamos lista de canales en un txt
        try:
            for entry in channels:
                entry = entry.replace("'","")
                plugintools.log("channels= "+entry)                
                url_option = plugintools.find_single_match(entry, 'href=(.*?) target')
                plugintools.log("url_option= "+url_option)
                tipo = plugintools.find_single_match(entry, "target=player_frame>(.*?)</a>")
                plugintools.log("tipo= "+tipo)
                if tipo.startswith("torrentstream") == True:
                    tipo = url_opcion.replace('torrentstream.php?channel=', "")
                    canales_dict.append('ace:'+url_option)
                    tipo_dict.append('[Acestream]')
                    file.write('ace:'+url_option+'---'+tipo+',')
                else:
                    canales_dict.append('http://onhockey.tv/'+url_option)
                    tipo_dict.append('['+tipo+']')
                    file.write('http://onhockey.tv/'+url_option+'---'+tipo+',')
        except TypeError:
            pass
            
        print canales_dict,tipo_dict
        file = open(tmp + partido + '.txt', "r")
        file.seek(0)
        data = file.readline()
        if data != "":
            plugintools.add_item(action="multihockey", title= '[COLOR orange][B]'+hora+'[/B][/COLOR][COLOR lightyellow] '+title_fixed+'[/COLOR]', url=title_fixed, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)
            file.close()
        else:
            file.close()
            print ("Sin enlaces para el partido: "+title_fixed)
                
    

                                     
def multihockey(params):
    plugintools.log("[black.box.tv-0.3.1].multihockey "+repr(params))

    title = params.get("url")
    title_fixed = params.get("url")
    title = title.replace("\x96", "")
    title = title.replace("vs", "")
    title = parser_title(title)
    title = title.replace(" ","")
    title = title.replace("-","")
    plugintools.log("title= "+title+'.txt')
    fh = open(tmp + title + '.txt', "r")
    fh.seek(0)
    data = fh.readline()

    # Controlamos el caso en que no haya enlaces
    if data.strip() != "":
        #print 'data',data
        data = data.split(",")
        num_items = len(data) - 1
        
        menu_seleccion=[]
        i = 1
        while i <= num_items:
            url_option = data[i-1]
            url_tipo = url_option.split("---")
            url_option = url_tipo[0]            
            tipo_link = url_tipo[1]
            title_option = 'Op.'+str(i)+': [COLOR orange][B]'+title_fixed + ' [/B][/COLOR][COLOR lightgreen][I]['+tipo_link+'][/I][/COLOR]'
            menu_seleccion.append([title_option,url_option,tipo_link])
            i = i + 1
            print i

        print 'menu_seleccion',menu_seleccion
        print 'num_items',num_items
        
        try:
            dialog_hockey = xbmcgui.Dialog()
            
            if num_items == 0:
                print num_items
                selector = 0
            if num_items == 1:
                print num_items
                print 'menu',menu_seleccion[0][0]
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0]])
            elif num_items == 2:
                print num_items
                print 'menu',menu_seleccion[0][0],menu_seleccion[1][0]
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0]])
            elif num_items == 3:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0]])
            elif num_items == 4:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0]])
            elif num_items == 5:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0]])
            elif num_items == 6:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0]])
            elif num_items == 7:
                print num_items
                print 'menu',menu_seleccion[0][0],menu_seleccion[1][0],menu_seleccion[2][0],menu_seleccion[6][0]
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0]])
            elif num_items == 8:
                print num_items
                print 'menu',menu_seleccion[0][0],menu_seleccion[1][0],menu_seleccion[2][0],menu_seleccion[6][0]
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0]])
            elif num_items == 9:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0]])
            elif num_items == 10:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0] , menu_seleccion[9][0]])
            elif num_items == 11:
                print num_items
                selector = dialog_hockey.select(title_fixed, [menu_seleccion[0][0] , menu_seleccion[1][0] , menu_seleccion[2][0] , menu_seleccion[3][0] , menu_seleccion[4][0] , menu_seleccion[5][0] , menu_seleccion[6][0] , menu_seleccion[7][0] , menu_seleccion[8][0] , menu_seleccion[9][0] , menu_seleccion[10][0]])

            if selector == 0:
                print menu_seleccion[0][2]
                url_onhockey(menu_seleccion[0][1], menu_seleccion[0][2])
                #xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Black Box TV', "Sin enlaces disponibles", 3 , art+'icon.png'))
            if selector == 1:
                print menu_seleccion[1][2]
                url_onhockey(menu_seleccion[1][1], menu_seleccion[1][2])
            elif selector == 2:
                print menu_seleccion[2][2]
                url_onhockey(menu_seleccion[2][1], menu_seleccion[2][2])
            elif selector == 3:
                print menu_seleccion[3][2]
                url_onhockey(menu_seleccion[3][1], menu_seleccion[3][2])
            elif selector == 4:
                print menu_seleccion[4][2]
                url_onhockey(menu_seleccion[4][1], menu_seleccion[4][2])
            elif selector == 5:
                print 'menu_seleccion',menu_seleccion[5][2]
                url_onhockey(menu_seleccion[5][1], menu_seleccion[5][2])
            elif selector == 6:
                print menu_seleccion[6][2]
                url_onhockey(menu_seleccion[6][1], menu_seleccion[6][2])
            elif selector == 7:
                print 'menu_seleccion',menu_seleccion[7][2]
                url_onhockey(menu_seleccion[7][1], menu_seleccion[7][2])
            elif selector == 8:
                print menu_seleccion[8][2]
                url_onhockey(menu_seleccion[8][1], menu_seleccion[8][2])
            elif selector == 9:
                print menu_seleccion[9][2]
                url_onhockey(menu_seleccion[9][1], menu_seleccion[9][2])
            elif selector == 10:
                print menu_seleccion[10][2]
                url_onhockey(menu_seleccion[10][1], menu_seleccion[10][2])
            elif selector == 11:
                print menu_seleccion[11][2]
                url_onhockey(menu_seleccion[11][1], menu_seleccion[11][2])                
            
        except TypeError:
            pass

    else:
        plugintools.log("No hay enlaces disponibles para "+title_fixed)
        xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Black Box TV', "Sin enlaces disponibles", 3 , art+'icon.png'))
        
        

                    
def url_onhockey(url,tipo):
    plugintools.log("[black.box.tv-0.3.0.URL_onHockey "+url)
    plugintools.log("tipo?= "+tipo)
    plugintools.log("url?= "+url)
    referer = 'http://www.onhockey.tv/'
    data = gethttp_referer_headers(url, referer)
    print data
    if data != -1:
        #plugintools.log("data= "+data)
        final_url = plugintools.find_single_match(data, '<iframe src="([^")]+)')
        if final_url == "":
            final_url = plugintools.find_single_match(data, 'SRC=\'(.*?)\'>')
            plugintools.log("final_url= "+final_url)
        else:
            plugintools.log("final_url= "+final_url)
            if final_url.find("sawlive") >= 0:
                referer = 'http://www.onhockey.tv/'
                from sawlive import *
                wizz1(final_url, referer)
            if url.find("castalba") >= 0:
                #http://castalba.tv/embed.php?cid=24411&wh=640&ht=410&r=onhockey.tv
                if final_url.find("channel") >= 0:
                    cid = final_url.split("=")
                    print cid
                    if len(final_url) >= 2:
                        cid = cid[1]
                        plugintools.log("cid= "+cid)
                else:
                    final_url = plugintools.find_single_match(data, 'src=\'(.*?)\'>')
                    channel = final_url.split("channel=")
                    print cid
                    if len(final_url) >= 2:
                        cid = cid[1]
                if cid != "":
                    final_url = 'swfUrl=http://static.castalba.tv/player5.9.swf pageUrl=http://castalba.tv/embed.php?cid='+cid+'&wh=640&ht=410&r=onhockey.tv'
                    from castalba import *
                    params = plugintools.get_params()
                    params["url"]=final_url
                    castalba(params)
                
    else:
        plugintools.log("Error URL del canal")
        
   

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


