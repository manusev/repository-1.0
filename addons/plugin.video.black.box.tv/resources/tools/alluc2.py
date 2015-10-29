# -*- coding: utf-8 -*-
#

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
        
    request_headers=[];request_headers.append(["User-Agent",ua.decode('base64')])
    params['page']=url;url='http://cipromario.net84.net/allucin.php?inc='+url.encode('base64');
    data,heads=plugintools.read_body_and_headers(url,headers=request_headers);
    matches = plugintools.find_multiple_matches(data, 'margin-bottom(.*?)source')    
    for entry in matches:
        #plugintools.log("entry= "+entry);
        '''
        title = plugintools.find_single_match(entry,'target=\"_blank\">(.*?)<\/a>');# 'target=_blank>(.*?)</a>')
        if title == "":
            title = plugintools.find_single_match(entry,'target=_blank>(.*?)<\/a>');# 'target=_blank>(.*?)</a>')
        page_url = 'http://www.alluc.com'+plugintools.find_single_match(entry, '<a href="([^"]+)')
        thumb = 'http://www.alluc.com' + plugintools.find_single_match(entry,'<img.*?src="([^"]+)');# '<img src="([^"]+)')
        media = plugintools.find_single_match(entry,'<div class="hoster">(.*?)<\/div>');# '<div class="hoster">(.*?)</div>')
        if media == "":
            media = plugintools.find_single_match(entry, '<div class=hoster>(.*?)<\/div>');# '<div class="hoster">(.*?)</div>')
        server = plugintools.find_single_match(media, 'target="_blank">(.*?)<\/a>');# 'target=_blank>(.*?)</a>')
        if server == "":
            server = plugintools.find_single_match(media, 'target=_blank>(.*?)<\/a>');# 'target=_blank>(.*?)</a>')
        #url = geturl(page_url)
        #url = url.strip()
        '''
        try:
         r='<div class=title><a href="([^"]+).*?>([^<]+).*?<img.*?src="([^"]+).*?target=\_blank>([^<]+)';
         w=plugintools.find_multiple_matches(entry,r);url=baseurl+w[0][0];
         url='http://cipromario.net84.net/allucin.php?inc='+url.encode('base64');
         data,heads=plugintools.read_body_and_headers(url,headers=request_headers);params['page']=url
         try:
          q='<div\sclass=div_info_rawlinks>.*?<textarea\sonClick="this\.select\(\);">([^<\s]+)';url=plugintools.find_single_match(data,q);		 
          #q='<div\sid="emd_player"\sclass="emd_player">.*?<iframe\ssrc="([^"]+)';url=plugintools.find_single_match(data,q);print '€€€€€',url
          try:
           q='<div class="block block-source">.*?<table(.*?)<\/table>';table=plugintools.find_single_match(data,q);
           g='<td><b>Description.*?<td>([^<]+)';extra=plugintools.find_single_match(table,g);print extra
           g='<td><b>Tags.*?<td>(.*?)<\/td>';tags=plugintools.find_single_match(table,g);
           g='<a\sclass="?text"?.*?>(.*?)<\/a>';tags=plugintools.find_multiple_matches(tags,g);tags=list(set(tags));print tags
          except: pass
         except: pass
         tit=w[0][1]+' [COLOR lightyellow][I]['+w[0][3]+'][/I][/COLOR]';thumb=baseurl+w[0][2]; 
         plugintools.add_item(action="play",title=tit,plot=texto,url=url,thumbnail=thumb,fanart=fanart,folder=False,isPlayable=True)
        except: pass
    print params;#sys.exit();
    # Botón "Anterior" hasta un máximo de 10 páginas de resultados
    if url.find("=") >= 0:
        page_active = url.split("=")
        page_active = page_active[1]
        next_page = url.split("=")
        if int(page_active) >= 2:
            page_active = int(page_active)-1
        next_page = next_page[0]+'='+str(page_active)
        print 'page_active',page_active
        plugintools.add_item(action="alluc", title = '[COLOR lightyellow]<<< Anterior [I](Pág. '+str(page_active)+')[/I][/COLOR]' , plot = texto , thumbnail = thumbnail , fanart = fanart , url = next_page , folder = True, isPlayable = False)
        params["plot"]=texto
       



def geturl(page_url):
    plugintools.log("[black.box.tv-0.3.05].geturl "+page_url)
    referer = 'http://www.alluc.com'
    body = gethttp_referer_headers(page_url, referer)
    plugintools.log("body= "+body)
    match = plugintools.find_single_match(body, '<div class="linktitleurl">(.*?)</div>')
    link = plugintools.find_single_match(match, '<a href="([^"]+)').strip()
    plugintools.log("link= "+link)
    return link



def gethttp_referer_headers(url,referer):
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
