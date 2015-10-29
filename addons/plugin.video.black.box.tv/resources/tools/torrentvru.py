# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de torrent-tv.ru
# Version 0.0.3 (01.01.2015)
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


home = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.black.box.tv/', ''))
tools = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.black.box.tv/resources/tools', ''))
addons = xbmc.translatePath(os.path.join('special://home/addons/', ''))
resources = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.black.box.tv/resources', ''))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.black.box.tv/art', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.black.box.tv/tmp', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/playlists', ''))

icon = art + 'icon.png'
fanart = 'fanart.jpg'


def torrentvru(params):
    plugintools.log("[black.box.tv-0.3.0].Torrent-TV.ru Playlist Sport Channels( "+repr(params))
    plugintools.add_item(action="", title = '[B][COLOR white]Sports Torrent Acestream[/B][/COLOR]', url = "", thumbnail = 'http://dl.dropbox.com/s/zytssf54x0eo3qf/Eventos%20Inter.jpg' , fanart = 'http://www.desktopicts.com/wp-content/uploads/2014/10/champions%20league%20wallpaper-hVsb.jpg' , folder = True, isPlayable = False)    

    url = params.get("url")
    thumbnail = params.get("thumbnail")
    fanart = params.get("fanart")
    title = params.get("title")
    plugintools.log("title= "+title)
    data = plugintools.read(url)
    #plugintools.log("data= "+data)
    match = plugintools.find_single_match(data, 'cat=4(.*?)</ul></li>')
    plugintools.log("match sports= "+match)
    matches = plugintools.find_multiple_matches(match, '<a href="(.*?)</li>')

    for entry in matches:
        entry = entry.split('"')
        url = 'http://www.torrent-tv.ru' + entry[0]
        url = url.strip()
        url = torrentvru_channels(url)
        title = entry[1]
        title= title.replace("</a>", "")
        title= title.replace(">", "")
        title = title.strip()
        title_fixed = title.replace(" ", "+")
        url = 'plugin://plugin.video.p2p-streams/?url=' + url + '&mode=1&name=' + title_fixed
        plugintools.log("url= "+url)
        plugintools.add_item(action="torrentvru_channels", title = title, url = url, thumbnail = 'http://dl.dropbox.com/s/zytssf54x0eo3qf/Eventos%20Inter.jpg' , fanart = 'http://www.desktopicts.com/wp-content/uploads/2014/10/champions%20league%20wallpaper-hVsb.jpg' , folder = False, isPlayable = True)



def torrentvru_channels(url):
    plugintools.log("[black.box.tv-0.3.0].Torrent-tv.ru getAcestream: "+url)

    data = plugintools.read(url)
    plugintools.log("data= "+data)
    match = plugintools.find_single_match(data, 'this.loadPlayer(.*?),{autoplay:')
    match = match.replace('"', "")
    match = match.replace("(", "")
    url = match.strip()
    plugintools.log("ace= "+url)
    return url
        
        
