# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinemax_rs
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "cinemax_rs"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Filme-noi.com"
__language__ = "ES"
__creationdate__ = "20131223"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.cinemax_rs mainlist")
    item.url="http://www.cinemaxx.ro/newvideos.html";
    return novedades(item)

def novedades(item):
    logger.info("pelisalacarta.channels.cinemax_rs novedades")
    itemlist = []
	
    # Download page
    data = scrapertools.cachePage(item.url)

    '''
    <li>
    <a href="http://www.cinemaxx.ro/tomorrowland-2015_d908479d6.html">
    <span class="dummy"></span>
    <span class="title">Tomorrowland (2015)</span>
    <img src="http://www.cinemaxx.ro/uploads/thumbs/d908479d6-1.jpg" alt="Tomorrowland (2015)"/>
    </a>
    <div class="meta">Adaugat <time datetime="2015-06-22T16:17:58-0400" title="Monday, June 22, 2015 4:17 PM">1 luna in urma</time></div>
    </li>
    '''
    patron  = '<li[^<]+<a href="([^"]+)"[^<]+'
    patron += '<span class="dummy[^<]+</span[^<]+'
    patron += '<span class="title"[^<]+</span[^<]+'
    patron += '<img src="([^"]+)" alt="([^"]+)"'
	
    # Extract elements
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
	
    for scrapedurl,scrapedthumbnail,scrapedtitle in matches:
        scrapedplot=""
        if (DEBUG): logger.info("url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], title=["+scrapedtitle+"]")
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )

    # Next page
    next_page_url = scrapertools.find_single_match(data,'<li[^<]+<a href="([^"]+)">\&raquo\;</a>')
    if next_page_url!="":
       itemlist.append( Item(channel=__channel__, action="novedades", title=">> Next page" , url=next_page_url , folder=True) )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si está ok el canal.
def test():
    # mainlist
    novedades_items = mainlist(Item())
    # Da por bueno el canal si alguno de los vídeos de "Novedades" devuelve mirrors
    bien = False
    for singleitem in novedades_items:
        mirrors_items = findvideos( item=singleitem )
        for mirror_item in mirrors_items:
            video_items = play(mirror_item)
            if len(video_items)>0:
                return True

    return False
