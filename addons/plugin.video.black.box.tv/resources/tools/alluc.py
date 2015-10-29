# -*- coding: utf-8 -*-
#
# intenta no cambiar la parte en naranja
#
# si quieres,te paso el php (allucin.php) para subirlo a tu servidor
# solo funciona con este user-agent,que es el nombre del plugin en base64...
#
# borra esto


import plugintools
import xbmc, xbmcgui
from __main__ import *


'''##########################################################################################################'''
baseurl='http://www.alluc.com/';ua='YXJlbmErcHJlbWl1bQ==';
'''##########################################################################################################'''
thumbnail = 'http://1.bp.blogspot.com/-zDHZTpb5bNk/UqSswOXCT5I/AAAAAAAABPU/1ulseXlRinA/s1600/alluc_plus_logo.png'
fanart = 'http://d3thflcq1yqzn0.cloudfront.net/024723778_prevstill.jpeg'

def alluc_getsearch(params):    
 try:
        texto = "";
        #texto='riddick'
        texto = plugintools.keyboard_input(texto)
        plugintools.set_setting("alluc_search",texto)
        params["plot"]=texto
        texto = texto.lower()        
        if texto == "": errormsg = plugintools.message("Black Box TV","Por favor, introduzca el canal a buscar");return errormsg
        else:
            texto = texto.lower().strip()
            texto = texto.replace(" ", "+")
            url = 'http://www.alluc.com/stream/'+texto+'+lang%3Aes'
            #url = 'http://www.alluc.com/stream/'+texto+'++lang:es'
            #url=baseurl+'stream/?q='+texto+'&stream=Streams'
            #url=baseurl+'stream/'+texto
            params["url"]=url
            url = params.get("url")
            referer = 'http://www.alluc.to'
            alluc(params)
            
 except: pass
 
def alluc(params):
    texto=params.get("plot");url=params.get("url");
    plugintools.add_item(action="", title= '[COLOR royalblue][B] ALLUC.INANTE /[/B][/COLOR] [COLOR white]Resultados de la búsqueda: [I][B]"'+texto+'"[/B][/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)

    #Paginación de resultados (Botón siguiente)
    if url.find("=") >= 0:
        page_active = url.split("=")
        page_active = page_active[1]
        print 'page_active',page_active
        next_page = url.split("=")
        if int(page_active) <= 9:
            page_active = int(page_active)+1
        next_page = next_page[0]+'='+str(page_active)
        print 'page_active',page_active
        plugintools.add_item(action="alluc", title = '[COLOR lightyellow]>>> Siguiente [I](Pág. '+str(page_active)+')[/I][/COLOR]' , plot = texto , thumbnail = thumbnail , fanart = fanart , url = next_page , folder = True, isPlayable = False)
        params["plot"]=texto
    else:
        next_page = url+'?page=2'
        plugintools.add_item(action="alluc", title = '[COLOR lightyellow]>>> Siguiente [I](Pág. 2)[/I][/COLOR]' , plot = texto , thumbnail = thumbnail , fanart = fanart , url = next_page , folder = True, isPlayable = False)
        params["plot"]=texto
        
    request_headers=[]
    request_headers.append(["User-Agent",ua.decode('base64')])
    url='http://arenaplus.byethost4.com/allucin.php?inc='+url.encode('base64')
    print url
    #url='http://cipromario.net84.net/allucin.php?inc='+url.encode('base64')
    data,heads=plugintools.read_body_and_headers(url,headers=request_headers);#print data
    match = plugintools.find_single_match(data, 'ponsoredlink(.*?)<div class=pagination>')
    if match == "":
        match = plugintools.find_single_match(data, 'ponsoredlink(.*?)<div class=\"pagination\">')
    print match
    matches = plugintools.find_multiple_matches(match, 'div style=\"margin-bottom(.*?){SOURCEATITLE}')
    i = 0
    for entry in matches:
        i = i + 1
        #plugintools.log("entry= "+entry)
        title = plugintools.find_single_match(entry, 'target=_blank>(.*?)</a>')
        if title == "":
            title = plugintools.find_single_match(entry, 'target=\"_blank\">(.*?)</a>')
        #plugintools.log("title="+title)
        server = plugintools.find_single_match(entry, 'stream online on (.*?)"')
        if server == "":
            server = plugintools.find_single_match(media2, 'target=\"_blank\">(.*?)</a>')
        #plugintools.log("server="+server)        
        url = plugintools.find_single_match(entry, 'href="([^"]+)')
        url = 'http://www.alluc.com'+url
        #plugintools.log("url= "+url)
        plugintools.add_item(action="getlink_alluc", title=title + ' [COLOR lightyellow][I]['+server+'][/I][/COLOR]', plot = texto , url=url, thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = True)

        


def getlink_alluc(params):
    plugintools.log("[black.box.tv] getlink_alluc "+repr(params))

    url = params.get("url")
    url = url.encode('base64').replace("=", "").replace("\n", "").strip()
    url='http://arenaplus.byethost4.com/allucin.php?inc='+url
    plugintools.log("URL= "+url)
    #url='http://cipromario.net84.net/allucin.php?inc='+url.encode('base64')
    request_headers=[]
    request_headers.append(["User-Agent",ua.decode('base64')])
    data,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    print data    
    #Buscamos el enlace...
    match = plugintools.find_single_match(data, '<div class="linktitleurl">(.*?)</div>')
    if match == "":
        match = plugintools.find_single_match(data, '<div class=linktitleurl>(.*?)</div>')
    plugintools.log("match= "+match)
    link = plugintools.find_single_match(match, '<a href="([^"]+)').strip()
    if link == "":
        match2 = plugintools.find_single_match(data, '<div id=emd_player class=emd_player>(.*?)</div>')
        plugintools.log("match2= "+match2)
        link = plugintools.find_single_match(match2, 'href="([^"]+)').strip()
        if link == "":
            link = plugintools.find_single_match(match2, 'this.select();">(.*?)</textarea>')

    url = link.strip()
    plugintools.log("URL= "+url)
    params = plugintools.get_params()
    if url.find("allmyvideos") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        allmyvideos(params)
    elif url.find("vidspot") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        vidspot(params)
    elif url.find("played.to") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        playedto(params)
    elif url.find("streamcloud") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        streamcloud(params)
    elif url.find("veehd") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        veehd(params)
    elif url.find("vk.com") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        vk(params)
    elif url.find("streamin.to") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        streaminto(params)
    elif url.find("tumi") >= 0:
        params["url"]=url
        plugintools.log("Launching Alluc video... "+repr(params))
        tumi(params)
    else:
        plugintools.play_resolved_url(link)
    
            
    



    
def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body

