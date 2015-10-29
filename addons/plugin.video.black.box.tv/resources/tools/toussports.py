# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Parser de TousSports.info para Black Box TV
# Version 0.1 (05.05.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a Juarrox


import plugintools, xbmcplugin, datetime

from __main__ import *

from resources.tools.msg import *

__icons__ = art + '/icons/'


def tous0(params):
    plugintools.modo_vista("list")
    plugintools.log("[%s %s] Toussports.info " % (addonName, addonId))

    #thumbnail = 'https://lh3.googleusercontent.com/-y0hsXXgY85s/Us0yFusFBOI/AAAAAAAABIA/8nbdAE7SajA/s630-fcrop64=1,00000000fe89ffff/CoverG%252BA.jpg'
    thumbnail = 'https://pbs.twimg.com/profile_images/378800000787122282/8cd4058b9b1d6e28fd930ff335b566f7.jpeg'
    #fanart = 'http://hdwallpapersmart.com/wp-content/uploads/2014/10/bein-sports1.jpg'
    #fanart = 'http://www.pix2.tv/wp-content/uploads/2013/09/BEIN-Sport-12.jpg'
    fanart = 'http://www.desktopwallpaperhd.net/wallpapers/22/a/sports-wallpapers-miscellaneous-savers-screen-baseball-images-220010.jpg'

    plugintools.add_item(action="", title= '[COLOR blue][B]Tous [COLOR white]Sports [/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    plugintools.add_item(action="tous2", title= '[COLOR white][B]Canales De Prueba[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)

    url = 'http://www.streaming-foot.info/schedule.php'
    referer = 'http://www.toussports.info'

    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    matches = plugintools.find_single_match(data, '<ul>(.*?)</ul>')
    #plugintools.log("matches= "+matches)

    event = plugintools.find_multiple_matches(matches, '<li class="list-group-item"(.*?)</li>')
    jornada = ""  # Control para imprimir día del evento una sola vez
    sin_eventos = 0  # Control para evitar impresión del día sin eventos programados
    for entry in event:
        plugintools.log("entry= "+entry)
        time_event = plugintools.find_single_match(entry, '<span style="display:none">(.*?)</span>')
        time_event = time_event.strip()
        plugintools.log("time_event= "+time_event)
        time_fixed = time_event.split(" ")
        if len(time_fixed) >= 2:
            time_fixed = time_fixed[0]
            time_fixed = time_fixed.split("-")
            time_event = time_fixed[2]+"/"+time_fixed[1]
            plugintools.log("time_event= "+time_event)

        if jornada == "" or jornada != time_event:
            plugintools.add_item(action="",title='[COLOR red][B][ '+time_event+' ][/B][/COLOR]',url="", thumbnail = thumbnail, fanart = fanart , folder=False, isPlayable=False)
            jornada = time_event
            plugintools.log("jornada= "+jornada)
            
        hora_event = plugintools.find_single_match(entry, '<span style="">(.*?)</span>')
        categ_event = plugintools.find_single_match(entry, '<span class="categorie">(.*?)</span>')
        name_event = plugintools.find_single_match(entry, '<span class="name_match">(.*?)</span>')
        ch_event = plugintools.find_single_match(entry, '<span class="links">(.*?)</span>')
        ch_event_fixed = ch_event.replace(" -", "").strip()
        title_fixed = '[COLOR green][B]'+hora_event.strip()+'[COLOR white]'+categ_event+'[COLOR blue] '+name_event+' [COLOR green]['+ch_event_fixed+'][/B][/COLOR]'
        channels = ch_event_fixed.split(" ")
        canales = []
        for item in channels:
            canales.append(item)
        datamovie = {}
        
        if title_fixed.find("Stream 24/24 7/7 gratuit")< 0:
            if ch_event_fixed != "":
                title_fixed = '[COLOR green][B]'+hora_event.strip()+' [COLOR white]'+categ_event+': [COLOR blue]'+name_event+'  [COLOR green][ '+ch_event_fixed+' ][/B][/COLOR]'
                datamovie["Plot"] = '[COLOR white][B]'+categ_event+': [COLOR blue]'+name_event+'\n[COLOR green][ '+ch_event_fixed+' ][/B][/COLOR]'
                datamovie["Plot"] = datamovie["Plot"].replace("&nbsp;", "").strip()
                #title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "[COLOR orange][24h][/COLOR]")
            else:
                title_fixed = '[COLOR green][B]'+hora_event.strip()+'  [COLOR white]'+categ_event+': [COLOR blue]'+name_event+'  [COLOR red][Sin enlaces][/B][/COLOR]'
                datamovie["Plot"] = '[COLOR white][B]'+categ_event+': [COLOR blue]'+name_event+'[/B][/COLOR]'
                datamovie["Plot"] = datamovie["Plot"].replace("&nbsp;", "").strip()
                #title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "[COLOR orange][24h][/COLOR]")

            thumbnail = set_icon(categ_event)

            title_fixed = title_fixed.replace("&nbsp;", "").strip() 
            plugintools.add_item(action="tous1", title=title_fixed, url="", thumbnail = thumbnail, info_labels = datamovie, fanart = fanart, folder = False, isPlayable=True)
            


   



def tous1(params):
    plugintools.modo_vista("tvshows")
    plugintools.log("[%s %s] tous1 " % (addonName, addonId))

    canales = [];referer = 'http://www.toussports.info';ref=referer
    title = params.get("title");plugintools.log("title= "+title)
    chs = plugintools.find_multiple_matches(title, 'Ch[0-9]+ ')
    for entry in chs:
        plugintools.log("entry= "+entry)
        canales.append(entry)

    print 'canales',canales

    try:
        plugintools.modo_vista("tvshows")
        dia = plugintools.selector(canales, 'Toussports.info')
        ch = canales[dia]
        ch = ch.replace("Ch", "http://www.toussports.info/lecteur.php?id=").strip();print ch
        datos='''data=gethttp_referer_headers(ch,referer);referer=ch;p='src="([^"]+)';ch=plugintools.find_single_match(data,p);#print data,url,referer''';
        exec(datos);exec(datos);exec(datos);exec(datos);
        datos='''data=gethttp_referer_headers(ch,referer);p='src="([^"]+)';rurl=ch;ch=plugintools.find_single_match(data,p);''';exec(datos);exec(datos);
		###DINOZAP###
        hidd='type="hidden".*?value="([^"]*)';hidd=plugintools.find_multiple_matches(data,hidd);
        try:
		 y=hidd[0].decode('base64');x=hidd[1].decode('base64');w='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';
		 z=plugintools.find_single_match(x,'(vod.*)');
		 
        except: xbmcgui.Dialog().ok('Aviso','Cambios En La Web,\No Puedo Sacar El Enlace!');plugintools.modo_vista("tvshows");pass;
        try: q=x+' app='+z+' playpath='+y+' swfUrl='+w+' swfVfy=true live=true token=@@stop-stole@@ flashver=WIN\2013,0,0,214 timeout=15 pageUrl='+rurl;
        except: xbmcgui.Dialog().ok('Aviso','Este Canal No Emite!');sys.exit();plugintools.modo_vista("tvshows");pass;
        print q;plugintools.play_resolved_url(q);plugintools.modo_vista("tvshows");sys.exit();

    except KeyboardInterrupt: pass;
    except IndexError: raise;
    except: pass


    


def tous2(params):
    plugintools.modo_vista("tvshows")    
    url = 'http://www.streaming-foot.info/schedule.php'
    referer = 'http://www.toussports.info'
    thumbnail = 'https://pbs.twimg.com/profile_images/378800000787122282/8cd4058b9b1d6e28fd930ff335b566f7.jpeg'
    fanart = 'http://www.desktopwallpaperhd.net/wallpapers/22/a/sports-wallpapers-miscellaneous-savers-screen-baseball-images-220010.jpg'
    
    plugintools.add_item(action="", title= '[COLOR blue][B]Tous [COLOR white]Sports [/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)

    data = gethttp_referer_headers(url,referer)
    #plugintools.log("data= "+data)

    matches = plugintools.find_single_match(data, '<ul>(.*?)</ul>')
    #plugintools.log("matches= "+matches)

    event = plugintools.find_multiple_matches(matches, '<li class="list-group-item"(.*?)</li>')
    for entry in event:
        plugintools.log("entry= "+entry)
        time_event = plugintools.find_single_match(entry, '<span style="display:none">(.*?)</span>')
        time_event = time_event.strip()
        plugintools.log("time_event= "+time_event)
        time_fixed = time_event.split(" ")
        if len(time_fixed) >= 2:
            time_fixed = time_fixed[0]
            time_fixed = time_fixed.split("-")
            time_event = time_fixed[2]+"/"+time_fixed[1]
            plugintools.log("time_event= "+time_event)
            
        hora_event = plugintools.find_single_match(entry, '<span style="">(.*?)</span>')
        categ_event = plugintools.find_single_match(entry, '<span class="categorie">(.*?)</span>')
        name_event = plugintools.find_single_match(entry, '<span class="name_match">(.*?)</span>')
        ch_event = plugintools.find_single_match(entry, '<span class="links">(.*?)</span>')
        ch_event_fixed = ch_event.replace(" -", "").strip()
        title_fixed = '[COLOR green][B]'+hora_event.strip()+'[COLOR white]'+categ_event+' '+name_event+' [COLOR green][ '+ch_event_fixed+' ][/B][/COLOR]'
        channels = ch_event_fixed.split(" ")
        canales = []
        for item in channels:
            canales.append(item)
        print canales   
        
        if title_fixed.find("Stream 24/24 7/7 gratuit") >= 0:
            if ch_event_fixed[0] != "":
                title_fixed = '[COLOR lightyellow][B]'+name_event+' [COLOR green][ '+ch_event_fixed+' ][/B][/COLOR]'
                title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "")
            else:
                title_fixed = '[COLOR white][B]'+name_event+' [COLOR red][Sin enlaces][/B][/COLOR]'
                title_fixed = title_fixed.replace("Stream 24/24 7/7 gratuit", "")

            title_fixed = title_fixed.replace("&nbsp;", "").strip()
            plugintools.add_item(action="tous1", title=title_fixed, url="", thumbnail = thumbnail, fanart = fanart, folder = False, isPlayable=False)
            

        

def set_icon(sport):
    plugintools.modo_vista("tvshows")
    sport = sport.replace("&nbsp;", "").lower()
    plugintools.log("sport: "+sport)
    
    if sport.find("football") >= 0:
        thumbnail = __icons__ + 'futbol.png'
    elif sport.find("basketball") >= 0:
        thumbnail = __icons__ + 'basketball.png'
    elif sport.find("hockey") >= 0:
        thumbnail = __icons__ + 'hockey.png'
    elif sport.find("judo") >= 0:
        thumbnail = __icons__ + 'judo.gif'
    elif sport.find("darts") >= 0:
        thumbnail = __icons__ + 'dardos.png'
    elif sport.find("tennis") >= 0:
        thumbnail = __icons__ + 'tenis.png'
    elif sport.find("volleyball") >= 0:
        thumbnail = __icons__ + 'voleibol.png'
    elif sport.find("rugby") >= 0:
        thumbnail = __icons__ + 'rugby.png'
    elif sport.find("cyclisme") >= 0:
        thumbnail = __icons__ + 'ciclismo.png'
    elif sport.find("formule") >= 0:
        thumbnail = __icons__ + 'formula1.png'
    elif sport.find("handball") >= 0:
        thumbnail = __icons__ + 'handball.png'
    elif sport.find("boxe") >= 0:
        thumbnail = __icons__ + 'boxeo.png'         
    else:
        thumbnail = 'https://pbs.twimg.com/profile_images/378800000787122282/8cd4058b9b1d6e28fd930ff335b566f7.jpeg'

    plugintools.modo_vista("tvshows")
    return thumbnail

	
def gethttp_referer_headers(url,referer):
    plugintools.modo_vista("tvshows");request_headers=[]
    request_headers.append(["User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31"])
    request_headers.append(["Referer", referer])
    body,response_headers = plugintools.read_body_and_headers(url, headers=request_headers);
    try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
    except: pass
    try: r='\'location\',\s\'([^\']+)';loc=plugintools.find_single_match(str(response_headers),r);
    except: pass
    if loc:
     request_headers.append(["Referer",url]);
     if jar: request_headers.append(["Cookie",jar]);#print jar
     body,response_headers=plugintools.read_body_and_headers(loc,headers=request_headers);
     try: r='\'set-cookie\',\s\'([^;]+.)';jar=plugintools.find_single_match(str(response_headers),r);jar=getjad(jar);
     except: pass
     plugintools.modo_vista("tvshows")
    return body
