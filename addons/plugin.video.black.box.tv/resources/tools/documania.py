# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de documaniatv.com
# Version 0.1 (18.10.2014)
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

import plugintools, requests
from resources.tools.resolvers import *


playlists = xbmc.translatePath(os.path.join('special://userdata/playlists', ''))
temp = xbmc.translatePath(os.path.join('special://userdata/playlists/tmp', ''))

addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

thumb_docus = 'http://www.documaniatv.com/uploads/xcustom-logo.png.pagespeed.ic.FSHzD0Pwtr.png'
#fanart = 'http://www.andreygoodkov.obe4u.com/wp-content/uploads/2014/07/documentary-film-the-phase-5.jpg'
fanart_docus = 'http://www.utne.com/~/media/Images/UTR/Editorial/Articles/Magazine%20Articles/2012/03-01/Documentary%20Filmmaking%20Truth%20or%20Fiction/Documentary-Filmmaking.jpg'



################################################################
from xml.sax.saxutils import escape, unescape
html_escape_table={'a':"&aacute;",'e':"&eacute;",'n':'&ntilde;','i':"&iacute;",'o':"&oacute;",'u':"&uacute;",'"':"&quot;","'":"&apos;","&":"&amp;"};html_unescape_table={v:k for k,v in html_escape_table.items()}#conservar esta orden,el '&' tiene que ser el ultimo en el dict,para no cambiar los de antes,que tambien llevan '&' !!!
def html_unescape(text): return unescape(text,html_unescape_table);

#################################################################

def documania0(params):
    plugintools.log("[%s %s] documaniatv.com parser %s " % (addonName, addonVersion, repr(params)))
    plugintools.modo_vista("tvshows")
    fanart = 'http://www.utne.com/~/media/Images/UTR/Editorial/Articles/Magazine%20Articles/2012/03-01/Documentary%20Filmmaking%20Truth%20or%20Fiction/Documentary-Filmmaking.jpg'
    plugintools.add_item(action="", title = '[COLOR yellow]DocumaniaTV.com[/COLOR]', url = "", thumbnail = thumb_docus , fanart = fanart_docus , folder = False, isPlayable = False)

    url = params.get("url")
    body = plugintools.read(url)
    channels = plugintools.find_single_match(body, "<ul id='ul_categories'>(.*?)</ul>")

    kanal = plugintools.find_multiple_matches(channels, '<li class="">(.*?)</li>')
    for entry in kanal:
        plugintools.log("entry= "+entry)
        url_canal = plugintools.find_single_match(entry, '<a href="([^"]+)')
        #url_canal = 'http://www.documaniatv.com/'+url_canal
        plugintools.log("url_canal= "+url_canal)
        title_canal = plugintools.find_single_match(entry, '<a href[^>]+([^<]+)')
        title_canal = title_canal.replace(">", "").strip();plugintools.log("title_canal= "+title_canal)
        plugintools.add_item(action="documania1", title='[COLOR white]'+title_canal+'[/COLOR]', url=url_canal, thumbnail = thumb_docus, fanart=fanart_docus, folder=True, isPlayable=False)



def documania1(params):
    plugintools.log("[%s %s] documania1 %s " % (addonName, addonVersion, repr(params)))
    plugintools.modo_vista("tvshows")
    datamovie = {}
    
    plugintools.add_item(action="", title='[COLOR gold][B]Documaniatv.com / '+params.get("title")+'[/B][/COLOR]', url="", thumbnail = thumb_docus, fanart=fanart_docus, folder=False, isPlayable=False)    

    url = params.get("url");ref='http://www.documaniatv.com';body = gethttp_referer_headers(url,ref);plugintools.log("body= "+body);plugintools.modo_vista("tvshows")
    bloque_docus = plugintools.find_single_match(body, '<div class="pm-li-video">(.*?)<div class="pagination pagination-centered">')
    plugintools.log("bloque_docus= "+bloque_docus)
    matches = plugintools.find_multiple_matches(bloque_docus, '<li>(.*?)</li>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        title_docu = plugintools.find_single_match(entry, 'alt="([^"]+)')
        url_docu = plugintools.find_single_match(entry, '<a href="([^"]+)')
        thumb_docu = plugintools.find_single_match(entry, '<img src="http://www.documaniatv.com/([^"]+)')
        length_docu = plugintools.find_single_match(entry, '<span class="pm-label-duration border-radius3 opac7">([^<]+)');length_docu=length_docu.replace("&iacute;", "í").strip()
        visitors_docu = plugintools.find_single_match(entry, '<span class="pm-video-attr-numbers"><small>([^<]+)');visitors_docu = visitors_docu.strip()
        published_docu = plugintools.find_single_match(entry, '<time datetime[^>]+>(.*?)</time>')
        #linea_sinopsis = '[COLOR lightblue]['+visitors_docu+'] [/COLOR]COLOR lightgreen][I]('+length_docu+')[/COLOR] [COLOR orange]'+published_docu+'[/I][/COLOR]\n'
        linea_sinopsis = '[COLOR white]Visitas: [COLOR lightblue]'+visitors_docu+'[/COLOR][COLOR white] Duracion: [COLOR lightgreen][I]'+length_docu+'[/COLOR] [COLOR white]Subido: [COLOR orange]'+published_docu+'[/I][/COLOR]\n'
        
        if thumb_docu.startswith("data") == True:
            thumb_docu = thumb_docus
        elif thumb_docu.find("xviews") >= 0:
            thumb_docu = 'http://www.documaniatv.com/uploads/xcustom-logo.png.pagespeed.ic.FSHzD0Pwtr.png'
        else:
            thumb_docu = thumb_docu.replace(".webp", "")
            if thumb_docu.endswith("png") == True:
                pass
            else:
                thumb_docu=thumb_docu+'.png';thumb_docu=thumb_docu.strip();thumb_docu='http://www.documaniatv.com/'+thumb_docu
                
        sinopsis_docu = plugintools.find_single_match(entry, '<p class="pm-video-attr-desc">(.*?)</p>');sinopsis_docu=linea_sinopsis+sinopsis_docu+'... [COLOR lightyellow][I](sigue)[/I][/COLOR]';
        sinopsis_docu=sinopsis_docu.decode('utf-8');datamovie["Plot"]=html_unescape(sinopsis_docu)  # Resuelve problema de codificación de caracteres en Python
        plugintools.log("published_docu= "+published_docu)
        plugintools.log("title_docu= "+title_docu)
        plugintools.log("url_docu= "+url_docu)
        plugintools.log("thumb_docu= "+thumb_docu)
        try:plugintools.log("sinopsis_docu= "+sinopsis_docu)
        except:pass
        plugintools.add_item(action="documania2", title='[COLOR white]'+title_docu+'[/COLOR] [COLOR lightyellow][I]'+length_docu+' [COLOR orange]('+visitors_docu+')[/I][/COLOR]', url=url_docu, thumbnail = thumb_docu, info_labels=datamovie, fanart=fanart_docus, folder=False, isPlayable=True)


def documania2(params):
    plugintools.log("[%s %s] documania1 %s " % (addonName, addonVersion, repr(params)))

    plugintools.modo_vista("tvshows")
    datamovie = {}

    # http://www.documaniatv.com/ajax.php?p=video&do=getplayer&vid=bba54697f&aid=3&player=detail
    # http://www.documaniatv.com/arte-y-cine/ciencia-ficcion-y-paranoia-video_3f443717c.html
    # http://www.documaniatv.com/arte-y-cine/la-noche-tematica-ciudadano-welles-2-la-guerra-de-los-mundos-video_eb00e6a6a.html
    url = params.get("url");plugintools.log("url= "+url);url=url.split("video_");id=url[1];id=id.replace(".html","");print id
    offer_php = 'http://www.documaniatv.com/ajax.php?p=video&do=getplayer&vid='+id+'&aid=2&player=detail';print offer_php
    ref='http://www.documaniatv.com/'
    body = gethttp_referer_headers(offer_php,ref);plugintools.modo_vista("tvshows");url=plugintools.find_single_match(body, '<iframe src="([^"]+)');url=url.replace("embed-","").replace(".html","").strip();print url
    play_url(url)



    
def gethttp_referer_headers(url,ref):
    plugintools.modo_vista("tvshows")
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Accept-Charset","utf-8"])
    request_headers.append(["Referer", ref])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)      
    #plugintools.log("body= "+body)
    return body        


        

def play_url(url):
    plugintools.log('[%s %s].play %s' % (addonName, addonVersion, url))	
	
    plugintools.modo_vista("tvshows")
    params = plugintools.get_params()
    show = params.get("page")
    if show == "":
        show = "list"
    plugintools.modo_vista(show)
    
    # Notificación de inicio de resolver en caso de enlace RTMP
    url = url.strip()

    if url.startswith("http") == True:
        if url.find("allmyvideos") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            allmyvideos(params)
        elif url.find("streamcloud") >= 0 :
            params["url"]=url
            params["title"]=title
            params = plugintools.get_params() 
            streamcloud(params)
        elif url.find("vidspot") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            vidspot(params)
        elif url.find("played.to") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            playedto(params)
        elif url.find("vk.com") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            vk(params)
        elif url.find("nowvideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            nowvideo(params)
        elif url.find("tumi") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)
        elif url.find("streamin.to") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            streaminto(params)
        elif url.find("veehd") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            veehd(params)
        elif url.find("novamov") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            novamov(params)
        elif url.find("gamovideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            gamovideo(params)
        elif url.find("movshare") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            movshare(params)
        elif url.find("powvideo") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            powvideo(params)
        elif url.find("mail.ru") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            mailru(params)
        elif url.find("tumi.tv") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            tumi(params)
        elif url.find("videobam") >= 0 :
            params = plugintools.get_params()
            params["url"]=url
            videobam(params)            
            
        else:
            url = url.strip()
            plugintools.play_resolved_url(url)

    elif url.startswith("rtp") >= 0:  # Control para enlaces de Movistar TV
        plugintools.play_resolved_url(url)
       
    else:
        plugintools.play_resolved_url(url)

    plugintools.modo_vista("tvshows")
        
    
    

    

    

    


