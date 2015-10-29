# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
import time

from core import scrapertools
from core import config
from core import logger
from core.item import Item
from servers import servertools

import xbmc
import xbmcgui

logger.info("tvalacarta.service_subscription First time launch")

while not xbmc.abortRequested:

    logger.info("tvalacarta.service_subscription Checking for new items in subscriptions")

    # TODO
    '''
    item = Item(channel="clantve", url="http://www.rtve.es/infantil/series/tickety-toc/videos/", action="download_all_episodes", extra="episodios", show="Tickety Toc", folder=False)
    from platformcode.xbmc import launcher
    from tvalacarta.channels import clantve as channel_module
    launcher.download_all_episodes(item,channel_module,silent=True)

    item = Item(channel="clantve", url="http://www.rtve.es/infantil/series/peppa-pig/videos/", action="download_all_episodes", extra="episodios", show="Peppa Pig", folder=False)
    from platformcode.xbmc import launcher
    from tvalacarta.channels import clantve as channel_module
    launcher.download_all_episodes(item,channel_module,silent=True)

    item = Item(channel="clantve", url="http://www.rtve.es/infantil/series/pac-man-aventuras-fantasmales/videos/", action="download_all_episodes", extra="episodios", show="Pac Man Aventuras Fantasmales", folder=False)
    from platformcode.xbmc import launcher
    from tvalacarta.channels import clantve as channel_module
    launcher.download_all_episodes(item,channel_module,silent=True)
    '''
    
    espera = 8*60*60 # Espera 8 horas (en segundos) antes de volver
    logger.info("tvalacarta.service_subscription Done, waiting for the expected lapse...")
    while not xbmc.abortRequested and espera > 0:
        # Cada segundo se comprueba si XBMC esta cerrándose, hasta que ha pasado el tiempo
        xbmc.sleep(1000)
        espera = espera - 1

    if espera==0:
        logger.info("tvalacarta.service_subscription Wait finished")

logger.info("tvalacarta.service_subscription XBMC Abort requested")
