# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Sports On Demand parser para Black Box TV
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




def sod0(params):
    plugintools.log("[black.box.tv 0.3.3].Sports on Demand "+repr(params))

    thumbnail = "http://nba.lemons.se/gfx/nbadavkabt.gif"
    fanart = "http://www.acrossthenba.com/wp-content/uploads/2015/01/NBA-Logo-Wallpaper-HD.jpg"

    plugintools.add_item(action="davka0", title='[COLOR white]Davka BT [/COLOR][I][COLOR lightgreen](Basketball) [/I][/COLOR]', url = 'http://bt.davka.info/', thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](Hockey) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/hockey.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](European Football/Soccer) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/soccer.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](Basketball) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/basketball.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)    
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](AFL/Gaelic Football) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/gaelic.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](Rugby) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/rugby.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](American Football) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/americanfootball.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](Basketball) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/rugby.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="sv_hockey0", title='[COLOR white]Sport-Video [/COLOR][I][COLOR lightgreen](Baseball) [/I][/COLOR]', url = 'http://www.sport-video.org.ua/baseball.html' , thumbnail = thumbnail, fanart = fanart, folder = True, isPlayable = False)

    
    
    
    
    



def davka0(params):
    plugintools.log("[black.box.tv 0.3.3].Davka BT "+repr(params))

    thumbnail = "http://nba.lemons.se/gfx/nbadavkabt.gif"
    fanart = "http://www.acrossthenba.com/wp-content/uploads/2015/01/NBA-Logo-Wallpaper-HD.jpg"
    
    url = params.get("url")    
    referer = url
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)

    matches = plugintools.find_multiple_matches(data, "<TD>name</TD>(.*?)</A></TD>")
    for entry in matches:
        plugintools.log("entry= "+entry)
        url_match = plugintools.find_single_match(entry, "<TD colspan=7><B><A href='(.*?)</A></B></TD>")
        plugintools.log("url_match= "+url_match)
        url_match = url_match.split("'>")
        url = url_match[0]
        url = 'http://bt.davka.info/'+url
        title_match = url_match[1]
        title_match_fixed = title_match.split("(")
        if len(title_match_fixed)>= 2:
            title_match_fixed = title_match_fixed[0]
        date = plugintools.find_single_match(title_match, '\((.*?)\)')
        date = date.split(".")
        month = date[0];day=date[1]
        title_fixed = '[COLOR gold][B]'+day+'/'+month+' [/B][/COLOR]'+title_match_fixed
        extra = plugintools.find_multiple_matches(entry, '<FONT color=white>(.*?)</FONT></TD>')
        for entri in extra:
            plugintools.log("entri= "+entri)
            title_fixed = title_fixed + '  [COLOR lightyellow][I]['+entri+'][/I][/COLOR]'

        plugintools.log("url= "+url)
        plugintools.log("title_match= "+title_match)        
        plugintools.add_item(action="sport_launchtorrent", title=title_fixed, url = url, thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)
        


def sport_launchtorrent(params):
    plugintools.log("Set URL to launch torrent: "+repr(params))

    url = params.get("url")
    url = url.replace(" ", "%20")
    plugintools.log("url= "+url)    
    #url = urllib.quote_plus(url)
    addon_torrent = plugintools.get_setting("addon_torrent")
    plugintools.log("addon_torrent= "+addon_torrent)
    if addon_torrent == "0":  # Stream (por defecto)
        url = urllib.quote_plus(url)
        url = 'plugin://plugin.video.stream/play/'+url
    elif addon_torrent == "1":  # Pulsar
        url = 'plugin://plugin.video.pulsar/play?uri=' + url
    else:
        url = 'plugin://plugin.video.stream/play/'+url
        
    plugintools.log("url= "+url)
    plugintools.play_resolved_url(url)


def sv_hockey0(params):
    plugintools.log("[black.box.tv 0.3.3].Sport-video Hockey "+repr(params))

    thumbnail = 'http://www.mytinyphone.com/uploads/users/hockeyfan49/189572.jpg'
    
    
    url = params.get("url")
    if url.endswith("gaelic.html") == True:
        title = '[COLOR gold][B]Sport-Video Gaelic Football[/B][/COLOR]'
        fanart = 'http://gaa.eircom.ie/image/var/files/experience-speaks/Football-tackles/PIC_2.jpg'
    elif url.endswith("hockey.html") == True:
        title = '[COLOR gold][B]Sport-Video Hockey[/B][/COLOR]'
        fanart = 'http://www.thesportsdb.com/images/media/team/fanart/vtrqwu1421535548.jpg'
    elif url.endswith("rugby.html") == True:
        title = '[COLOR gold][B]Sport-Video Rugby[/B][/COLOR]'
        fanart = 'http://static.trueachievements.com/customimages/012874.jpg'
    elif url.endswith("americanfootball.html") == True:
        title = '[COLOR gold][B]Sport-Video American Football[/B][/COLOR]'
        fanart = 'http://s1.picswalls.com/wallpapers/2014/07/25/awesome-rugby-wallpaper_041253717_99.jpg'
    elif url.endswith("soccer.html") == True:
        title = '[COLOR gold][B]Sport-Video European Football (Soccer)[/B][/COLOR]'
        fanart = 'http://images5.alphacoders.com/481/481998.jpg'
    elif url.endswith("baseball.html") == True:
        title = '[COLOR gold][B]Sport-Video Baseball[/B][/COLOR]'
        fanart = 'http://3.bp.blogspot.com/-toqMAo5-7WM/TpAeLJsqCDI/AAAAAAAACYQ/FGXLGdNo47I/s1600/The-best-top-desktop-baseball-wallpapers+baseball-america-wallpaper2012.jpg'
    elif url.endswith("basketball.html") == True:
        title = '[COLOR gold][B]Sport-Video Basketball[/B][/COLOR]'
        fanart = 'http://www.hdwallpaperscool.com/wp-content/uploads/2013/11/basketball-hd-wallpapers-beautiful-desktop-backgrounds-widescreen.jpg'

    plugintools.add_item(action="", title=title, url = "", thumbnail = thumbnail, fanart = fanart , folder = False, isPlayable = True)        
    
    referer = url
    data = gethttp_referer_headers(url,referer)
    plugintools.log("data= "+data)

    #Paginación
    matches = plugintools.find_multiple_matches(data, '<span style="color:#000000(.*?)</a></strong></span></div>')
    for entry in matches:
        #plugintools.log("entry= "+entry)
        page_matches = plugintools.find_multiple_matches(entry, '<a href="([^"]+)')
        for entry in page_matches:
            entry = entry.strip()
            if entry.endswith(".html") == True:
                plugintools.log("entry= "+entry)
                

    #Resultados de partidos
    matches = plugintools.find_multiple_matches(data, '<a href="javascript:popupwnd(.*?)</span></a></div>')
    for entry in matches:
        plugintools.log("entry= "+entry)
        title_match = plugintools.find_single_match(entry, 'title="([^"]+)')
        thumbnail_match = plugintools.find_single_match(entry, 'img src="(.*?)" id="Image')
        thumbnail_match = 'http://www.sport-video.org.ua/'+thumbnail_match
        url_match = plugintools.find_single_match(entry, '<a href="./(.*?).torrent"')        
        url = plugintools.find_single_match(url_match, '<a href="([^"]+)')
        url = url.replace("./", "http://www.sport-video.org.ua/")
        url = url.replace(" ", "%20").replace("%2F", "/").replace("%3A", ":").strip()
        if url != "":
            url = url + '.torrent'
            plugintools.log("title_match= "+title_match)
            plugintools.log("thumbnail_match= "+thumbnail_match)
            plugintools.log("url= "+url)
            plugintools.add_item(action="sport_launchtorrent", title=title_match, url = url, thumbnail = thumbnail_match , fanart = fanart, folder = False, isPlayable = True)
        else:
            xbmc.executebuiltin("Notification(%s,%s,%i,%s)" % ('Black Box TV', "URL no encontrada...", 3 , art+'icon.png'))

            

        # http://www.sport-video.org.ua/Detroit%20Red%20Wings%20-%20Carolina%20Hurricanes%2007.04.15.mkv.torrent
        # http://www.sport-video.org.ua/Ottawa%20Senators%20-%20Pittsburgh%20Penguins%2007.04.15.mkv

    



    
def gethttp_referer_headers(url,referer):
    plugintools.log("black.box.tv 0.3.3 Gethttp_referer_headers "+url)
    request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])    
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers)
    return body
