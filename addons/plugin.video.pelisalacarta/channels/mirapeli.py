# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para mirapeli
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "mirapeli"
__category__ = "F"
__type__ = "generic"
__title__ = "mirapeli"
__language__ = "ES"
__creationdate__ = "20150604"

DEBUG = config.get_setting("debug")
    
def isGeneric():
    return True

def mainlist(item):
    logger.info("channels.mirapeli mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Listado por género", action="genre"))
    itemlist.append( Item(channel=__channel__, title="Buscar..." , action="search") )

    return itemlist
	
def genre(item):
    logger.info("channels.mirapeli genre")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Acción", action="list", url="http://mirapeli.com/peliculas/accion/"))
    itemlist.append( Item(channel=__channel__, title="Animación", action="list", url="http://mirapeli.com/peliculas/animacion/"))
    itemlist.append( Item(channel=__channel__, title="Aventura", action="list", url="http://mirapeli.com/peliculas/aventura/"))
    itemlist.append( Item(channel=__channel__, title="Bélico Guerra", action="list", url="http://mirapeli.com/peliculas/belico-guerra/"))
    itemlist.append( Item(channel=__channel__, title="Biográfia", action="list", url="http://mirapeli.com/peliculas/biografia/"))
    itemlist.append( Item(channel=__channel__, title="Ciencia Ficción", action="list", url="http://mirapeli.com/peliculas/ciencia-ficcion/"))
    itemlist.append( Item(channel=__channel__, title="Comedia", action="list", url="http://mirapeli.com/peliculas/comedia/"))
    itemlist.append( Item(channel=__channel__, title="Crimen", action="list", url="http://mirapeli.com/peliculas/crimen/"))
    itemlist.append( Item(channel=__channel__, title="Documentales", action="list", url="http://mirapeli.com/peliculas/documentales/"))
    itemlist.append( Item(channel=__channel__, title="Drama", action="list", url="http://mirapeli.com/peliculas/drama/"))
    itemlist.append( Item(channel=__channel__, title="Familiar", action="list", url="http://mirapeli.com/peliculas/familiar/"))
    itemlist.append( Item(channel=__channel__, title="Fantasia", action="list", url="http://mirapeli.com/peliculas/fantasia/"))
    itemlist.append( Item(channel=__channel__, title="Intriga", action="list", url="http://mirapeli.com/peliculas/intriga/"))
    itemlist.append( Item(channel=__channel__, title="Musical", action="list", url="http://mirapeli.com/peliculas/musical/"))
    itemlist.append( Item(channel=__channel__, title="Romance", action="list", url="http://mirapeli.com/peliculas/romance/"))
    itemlist.append( Item(channel=__channel__, title="Suspenso", action="list", url="http://mirapeli.com/peliculas/suspenso/"))
    itemlist.append( Item(channel=__channel__, title="Terror", action="list", url="http://mirapeli.com/peliculas/terror/"))
    itemlist.append( Item(channel=__channel__, title="Thriller", action="list", url="http://mirapeli.com/peliculas/thriller/"))    

    return itemlist

def list(item):
    logger.info("channels.mirapeli list")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas de la pagina seleccionada
    #patron = '<td class=.*?<a href="([^"]+)"><img src="([^"]+)" alt="([^"]+)"'
    patron = '<div class="item">.*?<a href="([^"]+)" title="([^"]+)">.*?<img src="([^"]+)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedurl = match[0]
        scrapedtitle = match[1].strip()
        scrapedthumbnail = match[2]
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )
           
    # Extrae la marca de siguiente página
    next_page = scrapertools.find_single_match(data,"href='([^']+)'>Siguiente")
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="list", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page).replace("/../../","/"), folder=True) )

    return itemlist

def list_from_search(item):
    logger.info("channels.mirapeli list_from_search")

    # Descarga la página
    data = scrapertools.cachePage(item.url)

    # Extrae las entradas de la pagina seleccionada
    patron = '<img class="imx" style="margin-top:0px;" src="([^"]+)".*?<a href="([^"]+)">(.*?)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)
    itemlist = []
    for match in matches:
        scrapedurl = match[1]
        scrapedtitle = match[2].strip()
        scrapedthumbnail = match[0]
        scrapedplot = ""
        logger.info(scrapedtitle)

        # Añade al listado
        itemlist.append( Item(channel=__channel__, action="findvideos", title=scrapedtitle , fulltitle=scrapedtitle, url=scrapedurl , thumbnail=scrapedthumbnail , plot=scrapedplot , viewmode="movie", folder=True) )
           
    # Extrae la marca de siguiente página
    next_page = scrapertools.find_single_match(data,"href='([^']+)'>Siguiente")
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="list", title=">> Página siguiente" , url=urlparse.urljoin(item.url,next_page).replace("/../../","/"), folder=True) )

    return itemlist
	
def search(item,texto):
    logger.info("channels.mirapeli search")
    itemlist = []

    texto = texto.replace(" ","+")
    try:
        # Series
        item.url="http://mirapeli.com/?s=%s"
        item.url = item.url % texto
        item.extra = ""
        itemlist.extend(list_from_search(item))
        itemlist = sorted(itemlist, key=lambda Item: Item.title) 
        
        return itemlist
        
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []
   
