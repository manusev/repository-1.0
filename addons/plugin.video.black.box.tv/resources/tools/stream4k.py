# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV parser de mebuscan.net
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

import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import plugintools


thumbnail = 'http://www.mebuscan.net/Imagenes/Cabecerogeneral.jpg'
fanart = 'http://metcalfmultisports.co.uk/images/bg.jpg'



def stream4k0(params):
    plugintools.log("Stream4k "+repr(params))
    plugintools.add_item(action="", title = '[B][I][COLOR lightyellow]Stream4k Schedule[/B][/I][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart , folder = False, isPlayable = False)    

    url = params.get("url")
    data = plugintools.read(url)
    plugintools.log("data= "+data)


    
