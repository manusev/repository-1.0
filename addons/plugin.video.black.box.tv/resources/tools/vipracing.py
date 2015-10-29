# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Black Box TV Parser de Vipracing.org
# Version 0.1 (02.11.2014)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a Juarrox


from __main__ import *
from resources.tools.msg import *
#from resources.tools.direct2watch import *
#from direct2watch import *
from resources.regex.miplayernet import *

#<ul class="nav navbar-nav navbar-right">.*?<\/ul>.*?<\/ul>.*?<\/ul>.*?<\/ul>

def vip0(params):
    plugintools.modo_vista("list")

    thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg'
    fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg'

    plugintools.add_item(action="", title= '[COLOR blue][B]Eventos Deportivos SD[/B][/COLOR]', url = "", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False) 
    plugintools.add_item(action="vipr_channels", title= '[COLOR white][B]Mostrar Canales... [/B][/COLOR]',url=params['url'], thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)
    #plugintools.add_item(action="vipr_schedule", title= '[COLOR white] Programacion [/COLOR]',url=params['url'], thumbnail = thumbnail , fanart = fanart, folder = True, isPlayable = False)
    plugintools.add_item(action="", title= '',url="", thumbnail = thumbnail , fanart = fanart, folder = False, isPlayable = False)
    vipr_schedule(params)
    
    
        
        

def vipr_channels(params):
    plugintools.modo_vista("list")
    thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg'
    fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg'
    url = params.get("url");
    referer = 'http://www.vipracing.org'
    data = gethttp_referer_headers(url,referer)
    plugintools.modo_vista("list")
    match = plugintools.find_single_match(data, 'var channels = (.*?)}}')
    plugintools.log("match= "+match)
    option=plugintools.find_multiple_matches(match, '"(name|shortcut)":"([^"]+)');
    tit={}
    for i in range(0,len(option),2):
        name=option[i][1].replace("\u00f3n","on").replace('-','').replace('\\','');shortcut=option[i+1][1];
        if name not in tit: tit.update({name:'http://www.vipracing.tv/channel/'+shortcut});
    try: from collections import OrderedDict;tit=OrderedDict(sorted(tit.items()));
    except: tit=dict(sorted(tit.items()));#possible solution for spmc?!?
    for k,v in tit.iteritems(): plugintools.add_item(action='geturl_vipracing',title=k,url=v,thumbnail=thumbnail,fanart=fanart,isPlayable=False,folder=False);
    plugintools.modo_vista("list")

    
        


def server_vipracing(url_vipracing):
    #plugintools.log("[black.box.tv-0.3.0].server_rtmp " + url_vipracing)
    plugintools.modo_vista("list")
    
    if url_vipracing.find("iguide.to") >= 0:
        server = 'iguide'
        return server

    elif url_vipracing.find("direct2watch.com") >= 0:
        server = 'direct2watch'
        return server

    elif url_vipracing.find("freetvcast.pw") >= 0:
        server = 'freetvcast'
        return server

    elif url_vipracing.find("miplayer.net") >= 0:
        server = 'miplayernet'
        return server      

    elif url_vipracing.find("9stream") >= 0:
        server = '9stream'
        return server

    elif url_vipracing.find("freebroadcast") >= 0:
        server = 'freebroadcast'
        return server 

    elif url_vipracing.find("goodgame.ru") >= 0:
        server = 'goodgame.ru'
        return server 

    elif url_vipracing.find("hdcast") >= 0:
        server = 'hdcast'
        return server  

    elif url_vipracing.find("sharecast") >= 0:
        server = 'sharecast'
        return server 

    elif url_vipracing.find("cast247") >= 0:
        server = 'cast247'
        return server 

    elif url_vipracing.find("castalba") >= 0:
        server = 'castalba'
        return server       

    elif url_vipracing.find("vaughnlive") >= 0:
        server = 'vaughnlive'
        return server 

    elif url_vipracing.find("gameso.tv") >= 0:
        server = 'gameso.tv'
        return server   

    elif url_vipracing.find("totalplay") >= 0:
        server = 'totalplay'
        return server     

    elif url_vipracing.find("shidurlive") >= 0:
        server = 'shidurlive'
        return server        
    
    elif url_vipracing.find("everyon") >= 0:
        server = 'everyon'
        return server  

    elif url_vipracing.find("iviplanet") >= 0:
        server = 'iviplanet'
        return server    

    elif url_vipracing.find("cxnlive") >= 0:
        server = 'cxnlive'
        return server      

    elif url_vipracing.find("ucaster") >= 0:
        server = 'ucaster'
        return server  

    elif url_vipracing.find("mediapro") >= 0:
        server = 'mediapro'
        return server  

    elif url_vipracing.find("veemi") >= 0:
        server = 'veemi'
        return server  

    elif url_vipracing.find("yukons") >= 0:
        server = 'yukons'
        return server      

    elif url_vipracing.find("janjua") >= 0:
        server = 'janjua'
        return server 

    elif url_vipracing.find("mips") >= 0:
        server = 'mips'
        return server 

    elif url_vipracing.find("zecast") >= 0:
        server = 'zecast'
        return server 

    elif url_vipracing.find("vertvdirecto") >= 0:
        server = 'vertvdirecto'
        return server 

    elif url_vipracing.find("9stream") >= 0:
        server = '9stream'
        return server 

    elif url_vipracing.find("filotv") >= 0:
        server = 'filotv'
        return server 

    elif url_vipracing.find("dinozap") >= 0:
        server = 'dinozap'
        return server    

    elif url_vipracing.find("ezcast") >= 0:
        server = 'ezcast'
        return server 

    elif url_vipracing.find("flashstreaming") >= 0:
        server = 'flashstreaming'
        return server 

    elif url_vipracing.find("shidurlive") >= 0:
        server = 'shidurlive'
        return server 

    elif url_vipracing.find("multistream") >= 0:
        server = 'multistream'
        return server 

    elif url_vipracing.find("playfooty") >= 0:
        server = 'playfooty'
        return server 

    elif url_vipracing.find("flashtv") >= 0:
        server = 'flashtv'
        return server 

    elif url_vipracing.find("04stream") >= 0:
        server = '04stream'
        return server 

    elif url_vipracing.find("vercosas") >= 0:
        server = 'vercosas'
        return server 

    elif url_vipracing.find("dcast") >= 0:
        server = 'dcast'
        return server 

    elif url_vipracing.find("playfooty") >= 0:
        server = 'playfooty'
        return server 

    elif url_vipracing.find("pvtserverz") >= 0:
        server = 'pvtserverz'
        return server 
    
    else:
        server = 'undefined'
        return server 
        

def canal_vipracing(canal):
    #plugintools.log("[black.box.tv-0.3.0].canal_vipracing "+canal);#'http://vipracing.tv/index.php?/channel/opcion-2' ;#'http://vipracing.org/channel/opcion-1'
    plugintools.modo_vista("list")

    if canal.find("1") >= 0:
        canal = "opcion-1"
    elif canal.find("2") >= 0:
        canal = "opcion-2"
    elif canal.find("3") >= 0:
        canal = "opcion-3"
    elif canal.find("4") >= 0:
        canal = "opcion-4"
    elif canal.find("5") >= 0:
        canal = "opcion-5"
    elif canal.find("6") >= 0:
        canal = "opcion-6"
    elif canal.find("7") >= 0:
        canal = "opcion-7"
    elif canal.find("8") >= 0:
        canal = "opcion-8"
    elif canal.find("9") >= 0:
        canal = "opcion-9"
    elif canal.find("10") >= 0:
        canal = "opcion-10"
    elif canal.find("11") >= 0:
        canal = "opcion-11"
    elif canal.find("12") >= 0:
        canal = "opcion-12"          

    plugintools.log("canal= "+canal)
    
    try:
        if canal.startswith("http") == False: url = 'http://www.vipracing.tv/channel/'+canal
        else: url = "Nada";print "No se ha encontrado canal"
        if url: return url
    
    except: plugintools.log("Error al parsear Vipracing")


def vipracing2(params):
    plugintools.modo_vista("list")
    lista_canales = params.get("plot")
    lista_canales = lista_canales.split(", ")
    title = params.get("title")
    print lista_canales

    dia = plugintools.selector(lista_canales, title)
    ch = lista_canales[dia]

    url = canal_vipracing(ch);referer = 'http://vipracing.tv/'        
    url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url+'%26referer='+referer
    plugintools.log("U R L = "+url)
    play_vipracing(url)
    
    
    
    

    
def direct2watch(url,ref):
 plugintools.log("%s, %s " % (url,ref))
 #print params,params['page'];sys.exit(); 
 p='(embed\/|\&width=|\&height=)(\d{1,3})';match=plugintools.find_multiple_matches(url,p);
 url='http://www.direct2watch.com/embedplayer.php?width='+match[1][1]+'&height='+match[2][1]+'&channel='+match[0][1]+'&autoplay=true' 
 body=gethttp_referer_headers(url,ref);print body;playpath=plugintools.find_single_match(body, 'file: "([^"]+)');print playpath;
 if playpath.endswith("m3u8") == True:
	plugintools.play_resolved_url(playpath)
	return playpath
 else:
    try:
         p='window\.open\("([^"]+)';match=plugintools.find_multiple_matches(body,p)[1];m=match.split('/')[5];
         #print match.replace(m,'')+m.split('-')[2].replace(' ','_');sys.exit();
         #if match: body=gethttp_referer_headers(match.replace(m,'')+m.split('-')[2].replace(' ','_'),url);
    except: pass
    #print body;sys.exit()
    p='(\$\.getJSON\(|streamer\'?"?:?\s?|file\'?"?:?\s?|flash\'?"?,\s?src:?\s?)\'?"?([^\'"]+)'
    match=plugintools.find_multiple_matches_multi(body,p);
    tokserv = match[0][1];strmr = match[1][1].replace("\\","");plpath = match[2][1].replace(".flv","");swf = match[3][1];request_headers=[]
    request_headers.append(["User-Agent","Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)"]);request_headers.append(["Referer",url])
    body,response_headers = plugintools.read_body_and_headers(tokserv, headers=request_headers);p=':\'?"?([^\'"]+)';tok=plugintools.find_single_match(body,p)
    media_url=strmr+"/"+plpath+" swfUrl="+swf+" live=1 token="+tok+" timeout=15 swfVfy=1 pageUrl="+url;
    return media_url

def geturl_vipracing(params):
    plugintools.modo_vista("list")

    url=params.get("url");i=1;params["ref"]=url;
    referer = 'http://vipracing.tv/' ;
    url = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url='+url+'%26referer='+referer
    plugintools.log("U R L = "+url)
    play_vipracing(url)
        
    
  

def gethttp_referer_headers(url,referer):
    plugintools.log("[%s %s].gethttp_referer_headers( %s,%s) " % (addonName, addonVersion, url, referer));
    plugintools.modo_vista("list")
    request_headers=[]
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
    return body
	
	
def menu2_vipracing(params):
    #plugintools.log("[black.box.tv-0.3.0].menu2_vipracing "+repr(params))
    
    menu2 = plugintools.find_single_match(body, '<map name="Map2" id="Map2">(.*?)</map>')
    #plugintools.log("menu2= "+menu2)
    matches = plugintools.find_multiple_matches(menu2, 'href=\"(.*?)\"')    
    
    for entry in matches:
        referer='http://vipracing.tv/'
        #plugintools.log("Canal: "+entry)
        
        try:
            # <script type="text/javascript" src="http://www.gameso.tv/embed.php?id=max22a2&width=653&height=410&autoplay=true"></script>
            canal = gethttp_referer_headers(entry,referer)
            url = plugintools.find_single_match(canal, 'http://www.direct2watch.com/embed/(.*?)\"')
            url = url.strip()
            ch = plugintools.find_single_match(url,'(.*?)\&')
            width = plugintools.find_single_match(url,'width=(.*?)\&')
            height = plugintools.find_single_match(url,'height=(.*?)\&')
            url_vipracing = 'rtmp://watch1.direct2watch.com:1935/direct2watch/ pageUrl=http://www.direct2watch.com/embedplayer.php?width='+width+'&height='+height+'&channel='+ch+'&autoplay=true swfUrl=http://www.direct2watch.com/player/player_embed_iguide.swf referer=' + entry
            plugintools.log("URL direct2watch: "+url_vipracing)
            server = server_vipracing(url_vipracing)
            plugintools.add_item(action="launch_rtmp", title = "[COLOR white]Canal "+str(i)+'[/COLOR][COLOR green] [' + server + '][/COLOR]', url=url_vipracing, thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg' , fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg' , folder = False, isPlayable=True)
            i = i + 1
            if url == "":
                url = plugintools.find_single_match(canal, 'src=\"http://www.gameso.tv/(.*?[^"]+)')
                plugintools.log("Somago encontrado: "+url)
                ch = plugintools.find_single_match(url,'(.*?)\&')
                width = plugintools.find_single_match(url,'width=(.*?)\&')
                height = plugintools.find_single_match(url,'height=(.*?)\&')                
                url_vipracing = 'rtmp://go.gameso.tv/fasts playpath='+playpath+' swfUrl=http://www.gameso.tv/player/player_embed.swf pageUrl='+url+' token=#ed%h0#w18723jdsahjkDHFbydmo'
                plugintools.log("URL somago: "+url_vipracing)
                server = server_vipracing(url_vipracing)
                plugintools.add_item(action="launch_rtmp", title = "[COLOR red]Canal "+str(i) +'[/COLOR][COLOR green] [' + server + '][/COLOR]', url=url_vipracing, thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg' , fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg' , folder = False, isPlayable=True)
                i = i + 1                
        except:
            pass

def vipr_schedule(params):
    plugintools.modo_vista("list")
    url = 'http://vipracing.net/programacion/programacion.html'
    referer = 'http://www.vipracing.org'
    datamovie = {}

    prog = gethttp_referer_headers(url,referer)
    plugintools.modo_vista("list")
    plugintools.log("programación?= "+prog)

    # Obtenemos lista de canales y su clave
    canales_dict = {}
    canales = plugintools.find_single_match(prog, 'stm_bp(.*?)stm_ep')
    plugintools.log("programación?= "+canales)
    matches = plugintools.find_multiple_matches(canales, 'stm_aix\(\"(.*?)\);')
    for entry in matches:
        #plugintools.log("entry= "+entry)
        entry = entry.replace('"]', "")
        entry = entry.split(',')
        try:
            code_channel = entry[0].replace('"', "")
            name_channel = entry[3].replace('"', "")
            #plugintools.log("num_channel= "+code_channel)
            #plugintools.log("name_channel= "+name_channel)
            canales_dict[code_channel]=name_channel
            #print canales_dict
        except: pass

    # Obtenemos fechas de la programación
    # stm_aix("p0i7","p0i6",[0,"LUNES","","",-1,-1,0,"","_self","","","arrow011.gif","icon_65.gif",0,15,0,"","",0,0]);
    date = plugintools.find_multiple_matches(prog, '\"p0i7\",\"p0i6\"(.*?)\);')
    for entry in date:
        #plugintools.log("date= "+entry)        
        entry = entry.replace("0", "")
        entry = entry.replace("[", "")
        entry = entry.replace("]", "")
        entry = entry.replace('""', "")
        entry = entry.replace(",,", "")
        entry = entry.split('"')
        #print entry[0]
        #print entry[1]
        date = entry[1]
        plugintools.add_item(action="", title = '[COLOR red][B]'+date+'[/B][/COLOR]' , url="" , thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg' , fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg', folder = False, isPlayable = False )

        num_items = len(entry)
        i = 0
        while i < num_items :
            if entry[i].isupper() == True:
                date = entry[i]
                #print date
                i = i + 1
                continue
            else:
                i = i + 1
                continue


    # Listamos eventos por día...
    eventos_dia = plugintools.find_single_match(prog, 'stm_ep(.*?)stm_em')
    eventos_dia = eventos_dia.split("stm_ep();")
    num_items = len(eventos_dia)
    anterior = ""  # Control para evitar duplicidad entradas en eventos con más de un canal
    lista_canales = ""  # String de canales del evento    

    i = 0
    while i < num_items:
        evento = eventos_dia[i]
        #plugintools.log("EVENTO= "+evento)
        evento = evento.replace(".gif","")
        evento = evento.split('"')
        j = 0
        
        while j < len(evento):
            item_evento = evento[j].strip()
            if item_evento.find(":") >=0:
                evento_final = item_evento
                evento_final = evento_final.replace("\'", "'")
                #plugintools.log("EVENTO= "+evento_final)
                j = j + 1
                while j < len(evento):
                    item_evento = evento[j]
                    item_evento = item_evento.strip()
                    if item_evento in canales_dict :
                        canal = canales_dict[item_evento]
                        #plugintools.log("CANAL= "+canal)
                        # Función para buscar la URL del canal
                        url = canal_vipracing(canal)
                        plugintools.log("URL= "+url)
                                                
                        if anterior != evento_final:
                            plugintools.log("Nuevo evento: "+evento_final)
                            title_fixed = '[COLOR lightyellow]'+anterior+' [/COLOR]'
                            datamovie["Plot"] = lista_canales
                            plugintools.add_item(action="vipracing2", title = title_fixed , url=url , thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg' , info_labels = datamovie , plot = lista_canales , fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg', folder = False, isPlayable = False )
                            lista_canales = canal
                            anterior = evento_final                            
                        else:
                            lista_canales = lista_canales + ', ' + canal
                                                                                    
                        print lista_canales
                        j = j + 1                        
                        continue
                    
                    else:
                        j = j + 1
                        continue

            elif item_evento.find(".") >=0:
                evento_final = item_evento
                evento_final = evento_final.replace("\'", "'")
                #plugintools.log("EVENTO= "+evento_final)
                j = j + 1
                while j < len(evento):
                    item_evento = evento[j]
                    item_evento = item_evento.strip()
                    if item_evento in canales_dict :
                        canal = canales_dict[item_evento]
                        #plugintools.log("CANAL= "+canal)
                        # Función para buscar la URL del canal
                        url = canal_vipracing(canal);print url
                        if url:
                            plugintools.log("URL= "+url)
                            plugintools.add_item(action="vipracing2", title = '[COLOR white][B]'+evento_final+' [/B][/COLOR][COLOR blue][B]['+canal+'][/B][/COLOR]' , plot=canal , url=url , thumbnail = 'http://i18.servimg.com/u/f18/19/08/63/44/evento10.jpg' , fanart = 'http://i18.servimg.com/u/f18/19/08/63/44/agenda10.jpg', folder = False, isPlayable = True )
                            j = j + 1
                            continue
                        else:
                            j = j + 1
                            continue
                    else:
                        j = j + 1
                        continue                    
            else:
                j = j + 1
                continue
            
        i = i + 1

def play_vipracing(url):
    plugintools.modo_vista("list")
    plugintools.log("URL SportsDevil= "+url)
    xbmc.executebuiltin('XBMC.RunPlugin(' + url +')')  
  

    
    
