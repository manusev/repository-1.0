# -*- coding: utf-8 -*-
import urlparse,urllib2,urllib,re
import os
import sys
from core import config
from core import logger
from core.item import Item

DEBUG = True
CHANNELNAME = "channelselector"

def getmainlist(preferred_thumb=""):
    logger.info("channelselector.getmainlist")
    itemlist = []

    # Obtiene el idioma, y el literal
    idioma = config.get_setting("languagefilter")
    logger.info("channelselector.getmainlist idioma=%s" % idioma)
    langlistv = [config.get_localized_string(30025),config.get_localized_string(30026),config.get_localized_string(30027),config.get_localized_string(30028),config.get_localized_string(30029)]
    try:
        idiomav = langlistv[int(idioma)]
    except:
        idiomav = langlistv[0]

    # Añade los canales que forman el menú principal
    itemlist.append( Item(title=config.get_localized_string(30130) , channel="novedades" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_novedades.png") ) )
    itemlist.append( Item(title=config.get_localized_string(30118) , channel="channelselector" , action="channeltypes", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales.png") ) )
    itemlist.append( Item(title=config.get_localized_string(30103) , channel="buscador" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_buscar.png")) )
    #if config.is_xbmc(): itemlist.append( Item(title=config.get_localized_string(30128) , channel="trailertools" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_trailers.png")) )
    itemlist.append( Item(title=config.get_localized_string(30102) , channel="favoritos" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_favoritos.png")) )
    itemlist.append( Item(title=config.get_localized_string(30131) , channel="wiideoteca" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_biblioteca.png")) )
    if config.get_platform()=="rss":itemlist.append( Item(title="pyLOAD (Beta)" , channel="pyload" , action="mainlist" , thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"pyload.png")) )
    itemlist.append( Item(title=config.get_localized_string(30101) , channel="descargas" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_descargas.png")) )

    if "xbmceden" in config.get_platform():
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_configuracion.png"), folder=False) )
    else:
        itemlist.append( Item(title=config.get_localized_string(30100) , channel="configuracion" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_configuracion.png")) )

    #if config.get_setting("fileniumpremium")=="true":
    #	itemlist.append( Item(title="Torrents (Filenium)" , channel="descargasfilenium" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(),"torrents.png")) )

    #if config.get_library_support():
    if config.get_platform()!="rss": itemlist.append( Item(title=config.get_localized_string(30104) , channel="ayuda" , action="mainlist", thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_ayuda.png")) )
    return itemlist

# TODO: (3.1) Pasar el código específico de XBMC al laucher
def mainlist(params,url,category):
    logger.info("channelselector.mainlist")

    # Verifica actualizaciones solo en el primer nivel
    if config.get_platform()!="boxee":
        try:
            from core import updater
        except ImportError:
            logger.info("channelselector.mainlist No disponible modulo actualizaciones")
        else:
            if config.get_setting("updatecheck2") == "true":
                logger.info("channelselector.mainlist Verificar actualizaciones activado")
                try:
                    updater.checkforupdates()
                except:
                    import xbmcgui
                    dialog = xbmcgui.Dialog()
                    dialog.ok("No se puede conectar","No ha sido posible comprobar","si hay actualizaciones")
                    logger.info("channelselector.mainlist Fallo al verificar la actualización")
                    pass
            else:
                logger.info("channelselector.mainlist Verificar actualizaciones desactivado")

    itemlist = getmainlist()
    for elemento in itemlist:
        logger.info("channelselector.mainlist item="+elemento.title)
        addfolder(elemento.title , elemento.channel , elemento.action , thumbnail=elemento.thumbnail, folder=elemento.folder)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def getchanneltypes(preferred_thumb=""):
    logger.info("channelselector getchanneltypes")
    itemlist = []
    itemlist.append( Item( title=config.get_localized_string(30121) , channel="channelselector" , action="listchannels" , category="*"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_todos")))
    itemlist.append( Item( title=config.get_localized_string(30122) , channel="channelselector" , action="listchannels" , category="F"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_peliculas")))
    itemlist.append( Item( title=config.get_localized_string(30123) , channel="channelselector" , action="listchannels" , category="S"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_series")))
    itemlist.append( Item( title=config.get_localized_string(30124) , channel="channelselector" , action="listchannels" , category="A"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_anime")))
    itemlist.append( Item( title=config.get_localized_string(30125) , channel="channelselector" , action="listchannels" , category="D"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_documentales")))
    itemlist.append( Item( title=config.get_localized_string(30136) , channel="channelselector" , action="listchannels" , category="VOS" , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_vos")))
    #itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="M"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_musica")))
    itemlist.append( Item( title="Bittorrent" , channel="channelselector" , action="listchannels" , category="T"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_torrent")))
    itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="L"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_latino")))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title=config.get_localized_string(30126) , channel="channelselector" , action="listchannels" , category="X"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_adultos")))
    #itemlist.append( Item( title=config.get_localized_string(30127) , channel="channelselector" , action="listchannels" , category="G"   , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"thumb_canales_servidores")))
    #itemlist.append( Item( title=config.get_localized_string(30134) , channel="channelselector" , action="listchannels" , category="NEW" , thumbnail=urlparse.urljoin(get_thumbnail_path(preferred_thumb),"novedades")))
    return itemlist
    
def channeltypes(params,url,category):
    logger.info("channelselector.mainlist channeltypes")

    lista = getchanneltypes()
    for item in lista:
        addfolder(item.title,item.channel,item.action,item.category,item.thumbnail,item.thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category="" )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def listchannels(params,url,category):
    logger.info("channelselector.listchannels")

    lista = filterchannels(category)
    for channel in lista:
        if channel.type=="xbmc" or channel.type=="generic":
            if channel.channel=="personal":
                thumbnail=config.get_setting("personalchannellogo")
            elif channel.channel=="personal2":
                thumbnail=config.get_setting("personalchannellogo2")
            elif channel.channel=="personal3":
                thumbnail=config.get_setting("personalchannellogo3")
            elif channel.channel=="personal4":
                thumbnail=config.get_setting("personalchannellogo4")
            elif channel.channel=="personal5":
                thumbnail=config.get_setting("personalchannellogo5")
            else:
                thumbnail=channel.thumbnail
                if thumbnail == "":
                    thumbnail=urlparse.urljoin(get_thumbnail_path(),channel.channel+".png")
            addfolder(channel.title , channel.channel , "mainlist" , channel.channel, thumbnail = thumbnail)

    # Label (top-right)...
    import xbmcplugin
    xbmcplugin.setPluginCategory( handle=int( sys.argv[ 1 ] ), category=category )
    xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_NONE )
    xbmcplugin.endOfDirectory( handle=int( sys.argv[ 1 ] ), succeeded=True )

    if config.get_setting("forceview")=="true":
        # Confluence - Thumbnail
        import xbmc
        xbmc.executebuiltin("Container.SetViewMode(500)")

def filterchannels(category,preferred_thumb=""):
    returnlist = []

    if category=="NEW":
        channelslist = channels_history_list()
        for channel in channelslist:
            channel.thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
            returnlist.append(channel)
    else:
        try:
            idioma = config.get_setting("languagefilter")
            logger.info("channelselector.filterchannels idioma=%s" % idioma)
            langlistv = ["","ES","EN","IT","PT"]
            idiomav = langlistv[int(idioma)]
            logger.info("channelselector.filterchannels idiomav=%s" % idiomav)
        except:
            idiomav=""

        channelslist = channels_list()
    
        for channel in channelslist:
            # Pasa si no ha elegido "todos" y no está en la categoría elegida
            if category<>"*" and category not in channel.category:
                #logger.info(channel[0]+" no entra por tipo #"+channel[4]+"#, el usuario ha elegido #"+category+"#")
                continue
            # Pasa si no ha elegido "todos" y no está en el idioma elegido
            if channel.language<>"" and idiomav<>"" and idiomav not in channel.language:
                #logger.info(channel[0]+" no entra por idioma #"+channel[3]+"#, el usuario ha elegido #"+idiomav+"#")
                continue
            if channel.thumbnail == "":
                channel.thumbnail = urlparse.urljoin(get_thumbnail_path(preferred_thumb),channel.channel+".png")
            channel.plot = channel.category.replace("VOS","Versión original subtitulada").replace("F","Películas").replace("S","Series").replace("D","Documentales").replace("A","Anime").replace(",",", ")
            returnlist.append(channel)

    return returnlist

def channels_history_list():
    itemlist = []
    return itemlist

def channels_list():
    itemlist = []
    
    # En duda
    #itemlist.append( Item( title="Descarga Cine Clásico" , channel="descargacineclasico"  , language="ES"    , category="F,S"     , type="generic"  ))
    #itemlist.append( Item( title="Asia-Team"             , channel="asiateam"             , language="ES"    , category="F,S"     , type="generic"  ))
    #itemlist.append( Item( title="Buena Isla"            , channel="buenaisla"            , language="ES"    , category="A,VOS"       , type="generic"  ))

    itemlist.append( Item( viewmode="movie", title="Tengo una URL"         , channel="tengourl"   , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname") , channel="personal" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel2")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname2") , channel="personal2" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel3")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname3") , channel="personal3" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel4")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname4") , channel="personal4" , language="" , category="" , type="generic"  ))
    if config.get_setting("personalchannel5")=="true":
        itemlist.append( Item( title=config.get_setting("personalchannelname5") , channel="personal5" , language="" , category="" , type="generic"  ))
    itemlist.append( Item( title="Animeflv"                , channel="animeflv"           , language="ES" , category="A"       , type="generic"  ))
    itemlist.append( Item( title="Animeid"                 , channel="animeid"            , language="ES" , category="A"       , type="generic"  ))
    itemlist.append( Item( title="Aquitorrent"             , channel="aquitorrent"        , language="ES" , category="T,F,S,D,A,VOS"       , type="generic" ))
    itemlist.append( Item( title="Bajui"                   , channel="bajui"              , language="ES" , category="F,S,D,VOS" , type="generic"    ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Beeg"               , channel="beeg"            , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Bricocine"               , channel="bricocine"          , language=""   , category="T,F,S" , type="generic" , thumbnail="http://s6.postimg.org/9u8m1ep8x/bricocine.jpg"    ))
    itemlist.append( Item( title="Cineblog01 (IT)"         , channel="cineblog01"         , language="IT" , category="F,S,A,VOS"   , type="generic"  ))
    itemlist.append( Item( title="Cinehanwer"              , channel="cinehanwer"         , language="ES" , category="F"   , type="generic"  ))
    itemlist.append( Item( title="Cinemaxx (RO)"           , channel="cinemax_rs"         , language="RU" , category="F"   , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Cinetemagay" , channel="cinetemagay"          , language="ES"    , category="X,F" , type="generic"    )) # sdfasd 15/4/2012
    itemlist.append( Item( title="Cinetux"                 , channel="cinetux"            , language="ES" , category="L,F" , type="generic"  ))# jesus 16/7/2012
    itemlist.append( Item( title="Cuevana"                 , channel="cuevana"            , language="ES" , category="F"     , type="generic"  ))
    itemlist.append( Item( title="Cuelgame"                , channel="cuelgame"           , language="ES" , category="T,F,A,D,VOS" , type="generic"  ))
    itemlist.append( Item( title="Discoverymx"             , channel="discoverymx"        , language="ES" , category="L,D"       , type="generic"  ))
    itemlist.append( Item( title="Divxatope"               , channel="divxatope"          , language="ES" , category="T,F,S"       , type="generic"  ))
    itemlist.append( Item( title="DocumaniaTV"             , channel="documaniatv"        , language="ES" , category="D"       , type="generic"  ))
    itemlist.append( Item( title="El señor del anillo"     , channel="elsenordelanillo"   , language="ES" , category="L,F"       , type="xbmc"  ))
    itemlist.append( Item( title="Elite Torrent"           , channel="elitetorrent"       , language="ES" , category="T,F,S,D"       , type="xbmc"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Filesmonster Catalogue"    , channel="filesmonster_catalogue"           , language="es"    , category="X,F"   , type="generic"     ))
    itemlist.append( Item( title="Film per tutti (IT)"     , channel="filmpertutti"       , language="IT" , category="F,S,A"   , type="generic"     ))
    itemlist.append( Item( title="Film Senza Limiti (IT)"  , channel="filmsenzalimiti"    , language="IT" , category="F,S"       , type="generic"     ))
    itemlist.append( Item( title="Gnula"                   , channel="gnula"              , language="ES" , category="L,F" , type="generic"  )) # vcalvo 15/12/2011
    itemlist.append( Item( title="HDFull"                  , channel="hdfull"             , language="ES" , category="F,S" , type="generic"  )) # jesus 14/12/2014
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Hentai FLV"    , channel="hentaiflv"           , language="es"    , category="X,A"   , type="generic"     ))
    itemlist.append( Item( title="ItaliaFilms.tv (IT)"     , channel="italiafilm"         , language="IT" , category="A"   , type="generic"     ))
    itemlist.append( Item( title="JKanime"                 , channel="jkanime"            , language="ES" , category="A" , type="generic"  )) # jesus 15/10/2012
    itemlist.append( Item( title="La Guarida valencianista", channel="guaridavalencianista",language="ES" , category="D"       , type="generic"  ))
    itemlist.append( Item( title="Mega HD"                 , channel="megahd"             , language="ES" , category="F,S,D,A"       , type="generic"  ))
    itemlist.append( Item( title="Megaforo"                , channel="megaforo"           , language="ES" , category="F,S,D"       , type="generic"  ))
    itemlist.append( Item( title="Megaspain"               , channel="megaspain"          , language="ES" , category="F,S,D"       , type="generic"  ))
    itemlist.append( Item( title="Mejor Torrent"           , channel="mejortorrent"       , language="ES" , category="T,F,S,D"       , type="xbmc"  ))
    itemlist.append( Item( title="Mirapeli"                , channel="mirapeli"           , language="ES" , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Mitube"                  , channel="mitube"             , language="ES" , category=""       , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="MocosoftX", channel="mocosoftx"            , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Newpct"                  , channel="newpct"             , language="ES" , category="F,S,D,A"       , type="generic"  )) # jesus 08/03/2013
    itemlist.append( Item( title="Newpct1"                 , channel="newpct1"            , language="ES" , category="F,S,A"       , type="generic"  )) # jesus 08/03/2013
    itemlist.append( Item( title="Oranline"                , channel="oranline"           , language="ES" , category="L,F,D"        , type="generic" ))# jesus 16/7/2012
    itemlist.append( Item( title="Peliculasaudiolatino"    , channel="peliculasaudiolatino",language="ES" , category="L,F"       , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PeliculasEroticas" , channel="peliculaseroticas"    , language="ES" , category="X,F" , type="xbmc"  ))
    itemlist.append( Item( title="PeliculasDK"             , channel="peliculasdk"        , language="ES" , category="F" , type="generic" , thumbnail="http://s29.postimg.org/wzw749oon/pldklog.jpg"  )) 
    itemlist.append( Item( title="PeliculasMX"             , channel="peliculasmx"        , language="ES" , category="L,F"       , type="generic"  ))
    itemlist.append( Item( title="Pelis24"                 , channel="pelis24"            , language="ES" , category="L,F,VOS"        , type="generic"  ))
    itemlist.append( Item( title="Pelisadicto"             , channel="pelisadicto"        , language="ES" , category="F,L"        , type="generic"  ))
    itemlist.append( Item( title="Peliserie"               , channel="peliserie"          , language="ES" , category="F,S", type="generic"))
    itemlist.append( Item( title="PelisPekes"              , channel="pelispekes"         , language="ES" , category="F"        , type="generic"  ))
    itemlist.append( Item( title="Pirate Streaming (IT)"   , channel="piratestreaming"    , language="IT" , category="F" , type="generic"    )) # jesus 16/7/2012
    itemlist.append( Item( title="Pordede"                 , channel="pordede"            , language="ES" , category="F,S" , type="generic"    )) # jesus 16/6/2014
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PornoActricesX"            , channel="pornoactricesx"          , language="ES" , category="X,F" , type="generic"    ))
    if config.get_setting("enableadultmode") == "true": itemlist.append(Item( title="PornHub", channel="pornhub", language="ES" , category="X,F" , type="generic" ,thumbnail="http://s22.postimg.org/5lzcocfqp/pornhub_logo.jpg" )) # superberny 19/01/2015
    itemlist.append( Item( title="Quebajamos"              , channel="quebajamos"         , language="ES" , category="F,S,D" , type="generic"  )) # jesus 16/06/2014
    itemlist.append( Item( title="Quiero Dibujos Animados" , channel="quierodibujosanimados",language="ES", category="S" , type="generic"  )) # jesus 12/11/2012
    itemlist.append( Item( title="Reyanime"                , channel="reyanime"           , language="ES" , category="A"          , type="generic"  ))
    itemlist.append( Item( title="Robinfilm (IT)"          , channel="robinfilm"          , language="IT" , category="F"          , type="generic"  )) # jesus 16/05/2011
    itemlist.append( Item( title="Seriesadicto"            , channel="seriesadicto"       , language="ES" , category="S,A"          , type="generic" ))
    itemlist.append( Item( title="Seriesblanco"            , channel="seriesblanco"       , language="ES" , category="S,VOS"          , type="generic" ))
    itemlist.append( Item( title="Seriesdanko"             , channel="seriesdanko"        , language="ES" , category="S,VOS"          , type="generic" ))
    itemlist.append( Item( title="Seriesflv"               , channel="seriesflv"          , language="ES" , category="S,A"      , type="generic"  ))
    itemlist.append( Item( title="Series.ly"               , channel="seriesly"           , language="ES" , category="F,S,A,VOS"        , type="generic"  ))
    itemlist.append( Item( title="SeriesMu"                , channel="seriesmu"           , language="ES" , category="F,S,A,VOS"   , type="generic",  thumbnail="http://s17.postimg.org/jcasctj0v/smlogo.jpg"  ))
    itemlist.append( Item( title="Seriesyonkis"            , channel="seriesyonkis"       , language="ES" , category="S,A,VOS"        , type="generic" , extra="Series" ))
    itemlist.append( Item( title="Serie TV Sub ITA"        , channel="serietvsubita"      , language="IT" , category="S"        , type="generic" , extra="Series" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Serviporno", channel="serviporno"          , language="ES" , category="X,F" , type="generic"    ))
    itemlist.append( Item( title="Shurweb"                 , channel="shurweb"            , language="ES" , category="F,S,D,A" , type="generic"    ))
    itemlist.append( Item( title="Sinluces"                , channel="sinluces"           , language="ES" , category="F" , type="generic" , thumbnail="http://s14.postimg.org/cszkmr7a9/sinluceslogo.jpg"   ))
    #itemlist.append( Item( title="Somosmovies"             , channel="somosmovies"        , language="ES" , category="F,S"    , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Submit Your Flicks", channel="submityouflicks" , language="ES" , category="X,F" , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Submit Your Tapes", channel="submityourtapes" , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Teledocumentales"        , channel="teledocumentales"   , language="ES" , category="D"          , type="generic" )) # mrfloffy 19/10/2011
    itemlist.append( Item( title="Trailers ecartelera"     , channel="ecarteleratrailers" , language="ES" , category="F"       , type="generic"  ))
    itemlist.append( Item( title="Torrentestrenos"         , channel="torrentestrenos"    , language="ES" , category="T,F,S,D"          , type="generic" , thumbnail="http://s6.postimg.org/lq96iccb5/torrentestrenos.jpg" ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="tubehentai" , channel="tubehentai" , language="ES" , category="X,F" , type="xbmc"  ))
    itemlist.append( Item( title="Tus Novelas"             , channel="tusnovelas"         , language="ES" , category="S"        , type="generic" ))# jesus 3/7/2012
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="tuporno.tv" , channel="tupornotv" , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Txibitsoft"              , channel="txibitsoft"         , language="ES" , category="T,S,F"        , type="generic", thumbnail="http://s27.postimg.org/hx5ohryxf/tblogo.jpg" ))# neno 17/02/2015
    itemlist.append( Item( title="Unsoloclic"              , channel="unsoloclic"         , language="ES" , category="F,S" , type="generic"  ))# jesus 3/7/2012
    itemlist.append( Item( title="VePelis"                 , channel="vepelis"            , language="ES" , category="L,F" , type="generic"  ))# jjchao 28/05/2013
    itemlist.append( Item( title="Ver Telenovelas"         , channel="vertelenovelas"     , language="ES" , category="S" , type="generic"  ))
    if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="xhamster"           , channel="xhamster"             , language="ES" , category="X,F" , type="generic"  ))
    itemlist.append( Item( title="Yaske.net"               , channel="yaske"              , language="ES" , category="L,F"       , type="generic"  ))
    itemlist.append( Item( title="YouAnime HD"             , channel="youanimehd"         , language="ES" , category="A"       , type="generic"  ))
    itemlist.append( Item( title="V Series"                , channel="vseries"            , language="ES" , category="F,S"       , type="generic"  ))
    itemlist.append( Item( title="Zentorrents"             , channel="zentorrents"        , language="ES" , category="T,F,S" , type="xbmc" , thumbnail="http://s6.postimg.org/9zv90yjip/zentorrentlogo.jpg"  ))
    itemlist.append( Item( title="Zpeliculas"              , channel="zpeliculas"         , language="ES" , category="F"       , type="generic"  ))

    #itemlist.append( Item( title="Biblioteca XBMC"       , channel="libreria"             , language=""      , category="F,S,D,A" , type="wiimc"    ))
    #itemlist.append( Item( title="Cine-online.eu"        , channel="cineonlineeu"         , language="ES" , category="F" , type="generic"    )) # jesus 16/7/2012
    #itemlist.append( Item( title="Cinegratis"            , channel="cinegratis"           , language="ES"    , category="F" , type="generic"  ))
    #itemlist.append( Item( title="Cinetube"              , channel="cinetube"             , language="ES"    , category="F,S,A,D,VOS" , type="generic"  ))
    #itemlist.append( Item( title="Cinemastreaming (IT)"  , channel="cinemastreaming"      , language="IT" , category="F,S,A" , type="generic"  )) # jesus 5/11/2012
    #itemlist.append( Item( title="CineVOS"               , channel="cinevos"             , language="ES"    , category="F,A,D,VOS" , type="generic"  ))
    #itemlist.append( Item( title="dibujosanimadosgratis" , channel="dibujosanimadosgratis", language="ES"    , category="A"       , type="generic"  ))
    #itemlist.append( Item( title="Descargaya"           , channel="descargaya"          , language="ES"    , category="F,S"       , type="generic"  ))
    #itemlist.append( Item( title="Divx Online"           , channel="divxonline"           , language="ES"    , category="F"       , type="generic"  ))
    #itemlist.append( Item( title="DL-More (FR)"          , channel="dlmore"               , language="FR"    , category="S"       , type="generic"  ))
    #itemlist.append( Item( title="Enlacia"               , channel="enlacia"              , language="ES"    , category="F,S,D"       , type="generic"  ))
    # DESACTIVADO - SIN CONTENIDOS itemlist.append( Item( title="Filmixt"               , channel="filmixt"              , language="ES"    , category="F"       , type="generic"  ))
    #itemlist.append( Item( title="FilmesOnlineBr"        , channel="filmesonlinebr"       , language="PT"    , category="F"       , type="generic"     ))
    #itemlist.append( Item( title="Filmenoi (RO)"        , channel="filmenoi"       , language="RU"    , category="F"       , type="generic"     ))
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Gaypornshare"             , channel="gaypornshare"            , language="ES" , category="F" , type="generic"  ))
    #itemlist.append( Item( title="Goear"                   , channel="goear"                , language="ES" , category="M" , type="generic"  )) # vcalvo 15/12/2011
    #itemlist.append( Item( title="Instreaming (IT)" , channel="instreaming"          , language="IT"    , category="F,S"       , type="generic"  )) 
    #itemlist.append( Item( title="Internapoli City (IT)" , channel="internapoli"          , language="IT"    , category="F"       , type="generic"  )) 
    #itemlist.append( Item( title="Justin.tv"              , channel="justintv"            , language=""      , category="G"       , type="generic"  ))
    #itemlist.append( Item( title="La Guarida de bizzente", channel="documentalesatonline2", language="ES"    , category="D"       , type="generic"  ))
    #itemlist.append( Item( title="LetMeWatchThis"        , channel="letmewatchthis"       , language="EN"    , category="F,S,VOS"     , type="generic"  ))
    #itemlist.append( Item( title="lossimpsonsonline.com.ar", channel="los_simpsons_online"       , language="ES"    , category="S"     , type="generic"  ))
    #itemlist.append( Item( title="Malvin.tv"               , channel="malvin"              , language="ES"    , category="F,D"       , type="generic"  ))
    #itemlist.append( Item( title="Megapass"               , channel="megapass"             , language="ES"    , category="F,S,D"       , type="generic"  ))
    #itemlist.append( Item( title="MCAnime"               , channel="mcanime"              , language="ES"    , category="A"       , type="generic"  ))
    #itemlist.append( Item( title="Moviepremium"          , channel="moviepremium"             , language="ES"    , category="F"     , type="generic" )) # yorel 04/08/2013
    #itemlist.append( Item( title="Moviezet"              , channel="moviezet"             , language="ES"    , category="F,S,VOS"     , type="generic" )) # mrfluffy 01/10/2011
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="myhentaitube"         , channel="myhentaitube"         , language="ES" , category="F" , type="generic"  ))
    #itemlist.append( Item( title="NewDivx"               , channel="newdivx"              , language="ES"    , category="F,D"     , type="generic"  ))
    #itemlist.append( Item( title="Newdivxonline"         , channel="newdivxonline"              , language="ES"    , category="F"     , type="generic"  ))
    #itemlist.append( Item( title="NewHD"                 , channel="newhd"                , language="ES"    , category="F,VOS"       , type="generic" )) # xextil 05/05/2011
    #itemlist.append( Item( title="Novelas de TV"          , channel="novelasdetv", language="ES" , category="S" , type="generic"  )) # jesus 12/11/2012   
    #itemlist.append( Item( title="Nukety"                 , channel="nukety"          , language="ES"    , category="F,S"       , type="generic"  )) 
    #itemlist.append( Item( title="NKI"                   , channel="nki"                  , language="ES"    , category="S"       , type="generic" ))
    #itemlist.append( Item( title="No Megavideo"          , channel="nomegavideo"          , language="ES"    , category="F"       , type="xbmc"  ))
    # DESACTIVADO - SIN CONTENIDOS itemlist.append( Item( title="NoloMires"             , channel="nolomires"            , language="ES"    , category="F"       , type="xbmc"  ))
    #itemlist.append( Item( title="Peliculas Online FLV"  , channel="peliculasonlineflv"   , language="ES"    , category="F,D"     , type="generic"  ))
    # DESACTIVADO - SIN CONTENIDOS itemlist.append( Item( title="Peliculas21"           , channel="peliculas21"          , language="ES"    , category="F"       , type="xbmc"  ))
    #itemlist.append( Item( title="Peliculamos (IT)"      , channel="peliculamos"          , language="IT" , category="F,S,A" , type="generic"  )) # jesus 5/11/2012
    #itemlist.append( Item( title="peliculashd.pro"       , channel="peliculashdpro"       , language="ES" , category="F" , type="generic"  )) # jesus 12/11/2012
    #itemlist.append( Item( title="Peliculasfull"         , channel="peliculasfull"          , language="ES"    , category="F"       , type="generic"  ))
    #itemlist.append( Item( title="Peliculasid"           , channel="peliculasid"          , language="ES"    , category="F,VOS"       , type="xbmc"  ))
    #itemlist.append( Item( title="Peliculaspepito"       , channel="peliculaspepito" , language="ES"    , category="F"   , type="generic" ))
    #itemlist.append( Item( title="Peliculasyonkis"       , channel="peliculasyonkis_generico" , language="ES"    , category="F,VOS"   , type="generic" ))
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="PelisX"               , channel="pelisx"          , language="ES"    , category="F"       , type="generic"  )) # ZeDinis 01/02/2013
    #itemlist.append( Item( title="Playmax"               , channel="playmax"      , language="ES" , category="F,S" , type="generic"    )) # jesus 16/7/2012
    #itemlist.append( Item( title="PelisFlv"              , channel="pelisflv"             , language="ES" , category="F"          , type="xbmc"  ))
    # YA NO EXISTE itemlist.append( Item( title="Redes.tv"              , channel="redestv"              , language="ES" , category="D"          , type="xbmc"  ))
    #itemlist.append( Item( title="Seriematic"            , channel="seriematic"           , language="ES" , category="S,D,A"      , type="generic"  ))
    #itemlist.append( Item( title="Serieonline"           , channel="serieonline"          , language="ES" , category="F,S,D"      , type="generic"  ))
    #itemlist.append( Item( title="Series ID"             , channel="seriesid"             , language="ES" , category="S,VOS" , type="generic"  )) # vcalvo 15/12/2011
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Series Hentai"         , channel="serieshentai"         , language="ES" , category="F" , type="generic"  )) # kira 10/04/2011
    # DESACTIVADO - SIN CONTENIDO itemlist.append( Item( title="Series21"              , channel="series21"             , language="ES" , category="S"          , type="xbmc"  ))
    #itemlist.append( Item( title="Series Online TV"     , channel="seriesonlinetv", language="ES" , category="S" , type="generic"  )) # jesus 12/11/2012
    #itemlist.append( Item( title="Seriespepito"          , channel="seriespepito"         , language="ES" , category="S,VOS"          , type="generic" ))
    #itemlist.append( Item( title="ShurHD"       , channel="shurhd"             , language="ES"      , category="F,S" , type="generic"    ))
    #itemlist.append( Item( title="Sintonizzate"       , channel="sintonizzate"             , language="ES"      , category="F,S,D,A" , type="generic"    ))
    #itemlist.append( Item( title="Sipeliculas"       , channel="sipeliculas"             , language="ES"      , category="F" , type="generic"    )) # miguel 2/3/2012
    #itemlist.append( Item( title="Sofacine"              , channel="sofacine"             , language="ES" , category="F"          , type="generic"  ))
    #itemlist.append( Item( title="Sonolatino"            , channel="sonolatino"           , language=""   , category="M"          , type="xbmc"  ))
    #itemlist.append( Item( title="Stagevu"               , channel="stagevusite"          , language=""   , category="G"          , type="xbmc"  ))
    #itemlist.append( Item( title="Stormtv"          , channel="stormtv"         , language="ES" , category="S,A,VOS"        , type="generic" , extra="Series" )) 
    #itemlist.append( Item( title="Tibimate"      , channel="tibimate"     , language="ES" , category="F"          , type="generic" )) # mrfloffy 19/10/2011
    #itemlist.append( Item( title="Terror y Gore"         , channel="terrorygore"          , language="ES,EN" , category="F"       , type="xbmc"  ))
    #if config.get_setting("enableadultmode") == "true": itemlist.append( Item( title="Tube8"                 , channel="tube8"                , language="EN" , category="G"          , type="generic" ))
    #itemlist.append( Item( title="tu.tv"                 , channel="tutvsite"             , language="ES" , category="G"          , type="generic" ))
    #itemlist.append( Item( title="Tu butaka de cine"     , channel="tubutakadecine"       , language="ES" , category="F"        , type="generic" ))
    #itemlist.append( Item( title="Tu Mejor TV"         , channel="tumejortv"            , language="ES" , category="F,S"        , type="generic" ))
    #itemlist.append( Item( title="TVShack"               , channel="tvshack"              , language="EN" , category="F,S,A,D,M"  , type="xbmc"  ))
    #itemlist.append( Item( title="Vagos"                 , channel="vagos"                , language="ES" , category="F,S" , type="xbmc"  ))
    #itemlist.append( Item( title="Veocine"               , channel="veocine"              , language="ES" , category="F,A,D" , type="xbmc"  ))
    #itemlist.append( Item( title="Ver-anime"             , channel="veranime"             , language="ES" , category="A" , type="generic"  ))
    #itemlist.append( Item( title="Ver-series"            , channel="verseries"            , language="ES" , category="S" , type="generic"  )) # 15/12/2011 jesus
    #itemlist.append( Item( title="Vox filme online (RO)", channel="voxfilme" , language="RU" , category="S" , type="generic"  ))
    #itemlist.append( Item( title="Watchanimeon"          , channel="watchanimeon"         , language="EN" , category="A" , type="xbmc"  ))
    #itemlist.append( Item( title="Watch Cartoon Online"  , channel="watchcartoononline"   , language="EN" , category="F,S", type="generic" )) # jesus 23/11/2012
    #itemlist.append( Item( title="XO (RO)"  , channel="xo"   , language="RU" , category="F,S", type="generic" )) # jesus 23/11/2012
    #itemlist.append( Item( title="Yotix"                 , channel="yotix"                , language="ES" , category="A" , type="generic" ))
    #itemlist.append( Item( title="Zate.tv"              , channel="zatetv"         , language="ES"    , category="F,S"       , type="generic"  ))
    #itemlist.append( Item( title="Dospuntocerovision"    , channel="dospuntocerovision"   , language="ES" , category="F,S" , type="xbmc"  ))
    #itemlist.append( Item( title="Pintadibujos"          , channel="pintadibujos"         , language="ES" , category="F,A" , type="xbmc"  ))
    #itemlist.append( Item( title="Film Streaming"        , "filmstreaming"        , language="IT" , "F,A" , type="xbmc"  ))
    #itemlist.append( Item( title="Pelis-Sevillista56"    , "sevillista"           , language="ES" , "F" , type="xbmc"))
    #itemlist.append( Item( title="SoloSeries"            , "soloseries"           , language="ES" , "S" , type="xbmc"  ))
    #itemlist.append( Item( title="seriesonline.us"       , "seriesonline"         , language="ES" , "S" , type="xbmc" ))
    #itemlist.append( Item( title="Animetakus"            , channel="animetakus"           , language="ES" , category="A" , type="generic" ))
    #itemlist.append( Item( title="Documentalesatonline"  , channel="documentalesatonline" , language="ES" , category="D" , type="xbmc"  ))
    #itemlist.append( Item( title="Programas TV Online"   , channel="programastv"          , language="ES" , category="D" , type="xbmc"  ))
    #itemlist.append( Item( title="Futbol Virtual"        , "futbolvirtual"        , language="ES" , "D" , type="xbmc"  ))
    #channelslist.append([ "Eduman Movies" , "edumanmovies" , "" , "ES" , "F" ])
    #channelslist.append([ "SesionVIP" , "sesionvip" , "" , "ES" , "F" ])
    #channelslist.append([ "Newcineonline" , "newcineonline" , "" , "ES" , "S" ])
    #channelslist.append([ "PeliculasHD" , "peliculashd" , "" , "ES" , "F" ])
    #channelslist.append([ "Wuapi" , "wuapisite" , "" , "ES" , "F" ])
    #channelslist.append([ "Frozen Layer" , "frozenlayer" , "" , "ES" , "A" ])
    #channelslist.append([ "Ovasid"                , "ovasid"               , "" , "ES" , "A" , "xbmc"  ])
    return itemlist

def addfolder(nombre,channelname,accion,category="",thumbnailname="",thumbnail="",folder=True):
    if category == "":
        try:
            category = unicode( nombre, "utf-8" ).encode("iso-8859-1")
        except:
            pass
    
    import xbmc
    import xbmcgui
    import xbmcplugin
    listitem = xbmcgui.ListItem( nombre , iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    itemurl = '%s?channel=%s&action=%s&category=%s' % ( sys.argv[ 0 ] , channelname , accion , category )
    xbmcplugin.addDirectoryItem( handle = int(sys.argv[ 1 ]), url = itemurl , listitem=listitem, isFolder=folder)

def get_thumbnail_path(preferred_thumb=""):

    WEB_PATH = ""
    
    if preferred_thumb=="":
        thumbnail_type = config.get_setting("thumbnail_type")
        if thumbnail_type=="":
            thumbnail_type="2"
        
        if thumbnail_type=="0":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/posters/"
        elif thumbnail_type=="1":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/banners/"
        elif thumbnail_type=="2":
            WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/squares/"
    else:
        WEB_PATH = "http://media.tvalacarta.info/pelisalacarta/"+preferred_thumb+"/"

    return WEB_PATH