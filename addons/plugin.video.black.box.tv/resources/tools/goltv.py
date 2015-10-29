# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para Black Box TV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
#  cipromario(at)gmail(dot)com
# Version 0.0.4 (29.11.2014)
#   !!! Intentar NO compartir este archivo !!!
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *
from datetime import datetime
thumbnail="http://media.tumblr.com/tumblr_mdqvf64PSX1rvmlus.jpg";fanart="http://marcvilarnau.com/wp-content/uploads/2013/12/gol-stadium-950x600.png"
baseurl='http://golstadium.es/'
ethumb="http://www.goltelevision.com/public_data/css/images/logo_gol_t_r2.png";efan="http://imgur.com/yGR3lIg.png"
fan="http://static.goltelevision.com/web_gol/img/interiores/fondo-nuevo-iniesta.jpg"
messs='plugintools.message("ERROR","[COLOR=yellow]Cambios en la web[/COLOR]","[COLOR=red](avisar en el foro)[/COLOR]")'
nolink='plugintools.message("ATENCION","[COLOR=yellow]Canal sin emicion[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'
nocode='plugintools.message("ATENCION","[COLOR=yellow]Faltan diccionarios para los enlaces[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'

def goltv0(params):
  xbmcgui.Dialog().notification('ESPERE','Buscando enlaces...',icon,3000)
  akamai='';epgc='[COLOR=orange]Programacion completa '+time.strftime("%d-%m-%Y")+'[/COLOR]';#epgc=time.strftime("%A,%d-%B-%Y");
  url=baseurl+'index.php';ref=baseurl;body='';body,heads=curl_frame(url,ref,body);ref=url;
  url=baseurl+'login.php?cache_id=1';body,heads=curl_frame(url,ref,body);ref=url;
  logurl=baseurl+'comprobar_login.php';
  if login(logurl)==-1: dialog=xbmcgui.Dialog();ok=dialog.ok("ATENCION", "Debes añadir los datos de usuario en configuración");settings.openSettings()
  else:
   akamai=''
   pars='src:\sescape\(\'?"?([^\'"]+).*?system:\s\'?"?([^\'"]+).*?username:\s\'?"?([^\'"]+).*?transcode:\s\'?"?([^\'"]+).*?title:\s\'?"?([^\'"]+).*?cdn:\s\'?"?([^\'"]+).*?param1:\s\'?"?([^\'"]+).*?(cache_id=[^\'"]+)';#pars=plugintools.find_multiple_matches(akamai,pars)
   p = re.compile(ur'src:\sescape\(\'?"?([^\'"]+).*?system:\s\'?"?([^\'"]+).*?username:\s\'?"?([^\'"]+).*?transcode:\s\'?"?([^\'"]+).*?title:\s\'?"?([^\'"]+).*?cdn:\s\'?"?([^\'"]+).*?param1:\s\'?"?([^\'"]+).*?(cache_id=[^\'"]+)', re.DOTALL|re.MULTILINE)
   strobes=re.findall(p,akamai)
   #for strobe in strobes: print strobe
  try:
   repg=epg();repg=re.split("\n",repg);show=repg[0];episode=repg[1];
   plugintools.add_item(action="",title=repg[0],url="",thumbnail=ethumb,fanart=efan,isPlayable=False,folder=False)
   plugintools.add_item(action="",title=repg[1],url="",thumbnail=ethumb,fanart=efan,isPlayable=False,folder=False)
  except: pass
  plugintools.add_item(action="tepg",title=epgc,url="",thumbnail=ethumb,fanart=efan,isPlayable=False,folder=True)

def enlaces(params):
    #Read again to bypass user selection delay!!! (links expires in seconds)
    url = params.get("url");
    url=url.lower().replace("_mb_","_MB_");
    part = plugintools.find_single_match(url,'_MB_([^\/]+)');
    usrxxx=plugintools.get_setting('otro_user');passxxx=plugintools.get_setting('otro_pwd');
    if params['page']>0: ref=params['page']
    else: ref='http://golstadium.es/login.php?cache_id=1';
    opts = {'cache_id':'1','email2':usrxxx,'password2':passxxx,'submit':'Acceder a Tu Cuenta',}
    data = urllib.urlencode(opts)
    headers = {'Referer': ref,}
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))

    # Send Request
    opener.addheader = headers
    opener.open('http://golstadium.es/comprobar_login.php', data)

    # Check
    response = opener.open('http://golstadium.es/gol_en_directo.php?cache_id=1')
    akamai=response.read();#print akamai;sys.exit();print url;
    pars='src:\sescape\("([^\'"]+)';akamai=plugintools.find_single_match(akamai,pars);#print pars;sys.exit();
    ref='';body='';url=akamai;body,heads=curl_frame(url,ref,body);
    akamai=plugintools.read(akamai);#print akamai;sys.exit();
    stream=re.findall(re.compile(ur'(http.*?_MB_'+part+'.*)\s?'),akamai);
    params['title']="GolTV"+part+" GolTV"
    plugintools.play_resolved_url(stream[0]);sys.exit();
    #plugintools.play_resolved_url(str(stream[0]));sys.exit();
    #print part;print "SSS\n";print stream;sys.exit();
    park=re.findall(re.compile(ur'(http.*?)chunklist'),stream[0]);#print park;#print park[0];sys.exit();
    m3u8man=plugintools.read(stream[0]);#print m3u8man;sys.exit();
    piecedur=re.findall(re.compile(ur'TARGETDURATION:(.*?)\s'),m3u8man);
    pieceseq=re.findall(re.compile(ur'MEDIA-SEQUENCE:(.*?)\s'),m3u8man)[0];
    piecepat=re.findall(re.compile(ur'(media-?_?.*?)\s'),m3u8man);
    rep=piecepat[0].replace(pieceseq,"€€€");
    piecepat=park[0]+rep;
    out=playlists+'tmp.m3u8';
    #print out;
    extinf=re.findall(re.compile(ur'(\#EXTINF.*)', re.DOTALL),m3u8man);
    for i in extinf:
     m3u8man=m3u8man.replace(i,"")
    m3u8man=m3u8man.replace("CACHE:NO","CACHE:YES").replace("CACHE:NO","CACHE:YES");
    #print piecepat;print rep;print piecepat[0];print pieceseq;print piecedur[0];print m3u8man;print extinf
    if os.path.exists(out):
	 os.chmod(out, 0777);os.remove(out);
    file=open(out,'a');file.write(m3u8man);
    piece=''
    for i in range(0,100):
	 piece=piecepat.replace("€€€",str(pieceseq));#print piece
	 j=i*10
	 segment='\n#EXTINF:'+str(j)+',\n'+str(piece)
	 file.write(segment);
	 i+=1
	 pieceseq=int(pieceseq)+1
    file.close();#os.chmod(out,stat.S_IRUSR);
    plugintools.play_resolved_url(out);sys.exit();
    #xbmcgui.ListItem.setInfo("Title")= title
    plugintools.play_resolved_url(url)
    xbmc.Player().play(item=url,listitem=xbmcgui.ListItem(params['title']))

def file_put_contents(out, mode, data):
	file = open(filename, mode)
	file.write(data)
	file.close()

def strip(params):
 ref='';q=[];y=[];body='';ref=baseurl;akamai,heads=curl_frame(params['url'],ref,body);
 rex='BANDWIDTH=([0-9]{6,7}).*?\s+(http.*?[^\s$]+)';streams=plugintools.find_multiple_matches(akamai,rex);
 tit="[COLORred][B]GOL [/B][COLORorange]Stadium [COLORred]LIVE[/COLOR]";
 for i in streams:
   bandwith=str(i[0]);stream=str(i[1]);#print "Stream:\n"+str(stream)
   #title="[COLOR=orange] GolTV [COLOR=cyan]calidad:[COLOR=yellow] "+str(bandwith)+ "[/COLOR][/COLOR]";
   #plugintools.add_item(action="enlaces",title=title,url=str(stream),thumbnail=ethumb,fanart=fan,isPlayable=True,folder=False)
   q.append("[COLORcyan]calidad : [COLORyellow] "+str(bandwith)+ "[/COLOR]");y.append(stream);
 #print q;print tip;print y
 if len(q)==0: exec(nolink);sys.exit();
 try:
  index=0;ch=0;
  index=plugintools.selector(q,title=tit);
  ch=y[index];
  if ch:
   if index>-1: params={"title":tit,"fanart":fan,"page":'',"thumbnail":thumbnail,"url":ch};enlaces(params);
 except KeyboardInterrupt: pass;
 except IndexError: raise;
		
def curl_frame(url,ref,body):
 request_headers=[];
 request_headers.append(["User-Agent","Chrome/26.0.1410.65 Safari/537.31"])
 request_headers.append(["Referer",ref])
 body,response_headers=plugintools.read_body_and_headers(url,headers=request_headers);
 try: r='\'set-cookie\',\s\'([^;]+)';cook=plugintools.find_single_match(str(response_headers),r);
 except: pass
 try: r='\'location\',\s\'([^\']+)';loc=plugintools.find_single_match(str(response_headers),r);
 except: pass
 if loc:
  request_headers.append(["Referer",url]);
  if cook: request_headers.append(["Cookie",cook]);
  body,response_headers=plugintools.read_body_and_headers(baseurl+loc,headers=request_headers);
 return body,response_headers

#def login_new(logurl):
 #trimitere la php cu ua,cookie,etc
 #php returneaza def login(logurl) entero
def login(logurl):
 try:
    usrxxx=plugintools.get_setting('otro_user');passxxx=plugintools.get_setting('otro_pwd');
    ref='http://golstadium.es/login.php?cache_id=1';
    opts = {'cache_id':'1','email2':usrxxx,'password2':passxxx,'submit':'Acceder a Tu Cuenta',}
    data = urllib.urlencode(opts)
    headers = {'Referer': ref,}
    jar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    # Send Request
    opener.addheader = headers
    opener.open(logurl, data)
    # Check
    response = opener.open('http://golstadium.es/gol_en_directo.php?cache_id=1')
    akamai=response.read()
    if akamai.find('Debes acceder a tu cuenta para visualizar contenidos')>=0: xbmcgui.Dialog().ok('ERROR','Ususario/contraseña no valida')
    try:
	 r='href=\'?"?(octogol_en_directo.php[^\'"]+)';octo=plugintools.find_single_match(akamai,r);#print 'octo',octo
	 ref='http://golstadium.es/';response=opener.open(ref+octo);octo=response.read();
    except: pass
    try:
	 r='<a\shref="(otros_partidos[^"]+)';otros=plugintools.find_single_match(akamai,r);
	 r='cache_id=([^\'"\&]+)';cache=plugintools.find_single_match(akamai,r);#print 'otros',otros
    except: pass
    try: response=opener.open(baseurl+otros);otrs=response.read()
    except: pass
    pars='src:\sescape\("([^\'"]+)';akamai=plugintools.find_single_match(akamai,pars);#strip(akamai)
    tit1="[B][COLORred]GOL TeleVision [COLORgreen](GolTV)[/COLOR][/B]";tit2="[COLORred]NEW! [COLORcyan]OctoGol[/COLOR]";
    tit3="[COLORred]NEW! [COLORgold]Otros partidos LIVE[/COLOR]";tit4="[COLORred]NEW! [COLORpurple]Resumenes[/COLOR]";
    tit5="[COLORred]NEW! [COLORorange]Programas[/COLOR]";pgr='resumenesYT.php?accion=listar&evento=resumen&id=2&cache='+cache;
    l=baseurl+'listar_';pgp='programas.php?programa=1&cache_id='+cache;
    plugintools.add_item(title=tit1,url=akamai,thumbnail=thumbnail,fanart=fanart,isPlayable=True,folder=False,action='strip')
    if otros: plugintools.add_item(title=tit3,url=baseurl+otros,page=otrs,extra=akamai,thumbnail=thumbnail,fanart=fanart,isPlayable=False,folder=True,action='goltv2')
    if octo: plugintools.add_item(title=tit2,url=cache,page=str(octo),thumbnail=thumbnail,fanart=fanart,isPlayable=False,folder=True,action='goltv1')
    if octo: plugintools.add_item(title=tit5,url=l,page=pgr,thumbnail=thumbnail,fanart=fanart,isPlayable=False,folder=True,action='goltv5')
    if octo: plugintools.add_item(title=tit4,url=l,page=pgp,thumbnail=thumbnail,fanart=fanart,isPlayable=False,folder=True,action='goltv4')
 except ValueError: return -1 

def epg():
 epg=plugintools.read("http://www.golstadium.es/programacion.php")
 #print int(time.time()+300)
 timestp=int(time.time())#+60*60
 ora=datetime.fromtimestamp(timestp).strftime('%H:%M')
 today=datetime.fromtimestamp(timestp).strftime('%d/%m/%Y')
 #print today;print ora;print int(time.mktime(time.strptime(today+'04:30',"%d/%m/%Y%H:%M")))
 p = re.compile(ur'<div class="TabbedPanelsContent">.*?<ul>(.*?)<\/ul>.*?<\/div>', re.DOTALL|re.MULTILINE);epg=re.findall(p,epg);#print epg[0]
 p = re.compile(ur'<li>(.*?)<\/li>', re.DOTALL|re.MULTILINE);epg=re.findall(p,epg[0]);#print epg;sys.exit();
 event=[];hora=[];repg='';
 for i in epg:
  ora='>(.*?)(<|$)';ddd=plugintools.find_multiple_matches(i,ora);ora=ddd[0][0];meci=ddd[1][0];orat=ora.replace("h","")
  hora.append(orat);event.append(meci);
 j=0;timestpe='';
 for i in epg:
  timestpg=int(time.mktime(time.strptime(today+hora[j],"%d/%m/%Y%H:%M")))
  if timestpg>=timestp:
   if timestp>=timestpe:
    #print timestpe;print timestpg
    repg="[COLOR=green]AHORA: [/COLOR][COLOR=yellow]"+event[j-1]+" [/COLOR]("+hora[j-1]+"-"+hora[j]+")\n[COLOR=grey](Despues: "+event[j]+")[/COLOR]"
    break;
  j+=1;timestpe=timestpg
 return(repg)
 
def tepg(params):
 epg=plugintools.read("http://www.golstadium.es/programacion.php")
 timestp=int(time.time());plot='';
 ora=datetime.fromtimestamp(timestp).strftime('%H:%M')
 today=datetime.fromtimestamp(timestp).strftime('%d/%m/%Y')
 p = re.compile(ur'<div class="TabbedPanelsContent">.*?<ul>(.*?)<\/ul>.*?<\/div>', re.DOTALL|re.MULTILINE);epg=re.findall(p,epg);#print epg[0]
 p = re.compile(ur'<li>(.*?)<\/li>', re.DOTALL|re.MULTILINE);epg=re.findall(p,epg[0]);#print epg;sys.exit();
 for i in epg:
  ora='>(.*?)(<|$)';ddd=plugintools.find_multiple_matches(i,ora);ora=ddd[0][0];meci=ddd[1][0];orat=ora.replace("h","")
  tpg="[COLOR=yellow]"+orat+" [/COLOR]"+meci;plot+='[CR]'+tpg;
  plugintools.add_item(action="",title=tpg,url="",thumbnail=ethumb,fanart=efan,isPlayable=False,folder=False)
  
def goltv1(params):
  xbmcgui.Dialog().notification('ESPERE','buscando enlaces...',icon,3000)
  r='OVERON_OCTOSHAPE.*?\'sec\'\s+:\s\'([^\']+).*?escape\(\'([^\']+)';octogol=plugintools.find_multiple_matches(params['page'],r)
  print octogol;sys.exit();
  ref='http://www.golstadium.es/gol_en_directo.php?cache_id='+params['url'];body='';body,heads=curl_frame(baseurl+params['page'],ref,body);
  print '€€€€€€€€€€€€',body,heads,baseurl+params['page'],ref;sys.exit();
  '''
  http://cdn.octoshape.net/resources/player/jwflvplayer/5/jwplayer-octoshape-mediaprovider2.swf
  sec=l4OFh2GfqZKFh3JlpbCVh46Fae3OvauUpYjBo7enoaJhssWpmJSqjMf0loOEgrKf
  1LbIwafX19W4joFj4urXuLW%2Fp53lyMfDxZzQ5sqBwreonuPKt72zpOHllL%2B9yJme3NHJg7WcoKXGtcaF
  http://www.golstadium.es/octogol_en_directo.php?cache_id=1427123019K3qF9PHYwF playpath=1LbIwafX19W4joFj4urXuLW%2Fp53lyMfDxZzQ5sqBwreonuPKt72zpOHllL%2B9yJme3NHJg7WcoKXGtcaF swfUrl=http://cdn.octoshape.net/resources/player/jwflvplayer/5/jwplayer-octoshape-mediaprovider2.swf
  http://streams.octoshape.net/streamlink/mediapro/live/flv/ch1/abr3
  http://www.golstadium.es/ticket.php?OctoshapeAuthid=-1279822199&octoshapestream=octoshape%3A%2F%2Fstreams%2Eoctoshape%2Enet%2Fmediapro%2Flive%2Fflv%2Fch1%2Fabr3&rand=30494411264&OctoshapeSiteUrl=http%3A%2F%2Fwww%2Egolstadium%2Ees%2Foctogol_en_directo%2Ephp%3Fcache_id%3D1427124640sFykCfx49Y
  http://statsrvs.octoshape.net/statservers/0905.xml?time=443
  '''
  url=baseurl+'index.php';ref=baseurl;body='';body,heads=curl_frame(url,ref,body);ref=url;
  url=baseurl+'login.php?cache_id=1';body,heads=curl_frame(url,ref,body);ref=url;
  logurl=baseurl+'comprobar_login.php';
  if login(logurl)==-1: dialog=xbmcgui.Dialog();ok=dialog.ok("ATENCION", "Debes añadir los datos de usuario en configuración");settings.openSettings()
  
def goltv2(params):
  try:
   r='<table.*?class="escudo"><img src="([^"]+).*?class="fecha">([^h]+).*?class="escudo"><img src="([^"]+).*?class="equipos">([^<]+).*?class="button button_verde" href="([^"]+).*?<\/table>';
   otros=plugintools.find_multiple_matches(params['page'],r);
  except: eval(messs);sys.exit();
  if not otros: eval(noevent);sys.exit();
  for i in range(0,len(otros)):
   tit=otros[i][1].replace(' a las ',',').replace('&','').replace('acute;','')
   tit='[COLORgreen]'+tit+' [COLORyellow]'+otros[i][3]+'[/COLOR]';
   plugintools.add_item(title=tit,url=params['extra'],page=params['url'],extra=str(i+1),thumbnail=baseurl+otros[i][0],fanart=baseurl+otros[i][2],isPlayable=True,folder=False,action='goltv3')
   #plugintools.add_item(title=tit,url=baseurl+otros[i][4],page=params['url'],extra=str(i+1),thumbnail=baseurl+otros[i][0],fanart=baseurl+otros[i][2],isPlayable=True,folder=False,action='goltv3')
  
def goltv3(params):
 ref=params['page'];q=[];y=[];body='';ref=baseurl;akamai,heads=curl_frame(params['url'],ref,body);
 print akamai,heads,params['url'],params['page'],'extra',params['extra'];#sys.exit();
 rex='BANDWIDTH=([0-9]{6,7}).*?\s+(http.*?[^\s$]+)';streams=plugintools.find_multiple_matches(akamai,rex);
 tit=params['title'];
 for i in streams:
   bandwith=str(i[0]);stream=str(i[1]);
   q.append("[COLORcyan]calidad : [COLORyellow] "+str(bandwith)+ "[/COLOR]");y.append(stream.replace('24h',params['extra']+'livestream'));
 print q;print 'stream',y
 if len(q)==0: exec(nolink);sys.exit();
 try:
  index=0;ch=0;
  index=plugintools.selector(q,title=tit);
  ch=y[index];
  if ch:
   if index>-1: plugintools.play_resolved_url(ch);sys.exit();#params={"title":tit,"fanart":fan,"page":'',"thumbnail":thumbnail,"url":ch};enlaces(params);
 except KeyboardInterrupt: pass;
 except IndexError: raise;
  
	  
def goltv4(params):
  body='';url=params['url']+params['page'];ref=baseurl;
  body,heads=curl_frame(url,ref,body);ref=url;
  r='href="\#">RES\&Uacute;MENES.*?href="\#">PROGRAMAS<';w=plugintools.find_single_match(body,r);
  r='(<!--)?<li>.*?href="([^"]+).*?>([^<]+)';w=plugintools.find_multiple_matches(w,r);
  for i in w:
   if not i[0]=='':
    prefix='[COLORred] (OFF)[/COLOR]'
    if not i[1]=='#': plugintools.add_item(title=i[2]+prefix,url=baseurl+i[1],page=url,thumbnail=thumbnail,fanart=fan,folder=False,isPlayable=False,action='')
   else:
    prefix='';
    if not i[1]=='#': plugintools.add_item(title=i[2]+prefix,url=baseurl+i[1],page=url,thumbnail=thumbnail,fanart=fan,isPlayable=False,action='goltv6')
	
def goltv5(params):
  body='';url=params['url']+params['page'];ref=baseurl;
  body,heads=curl_frame(url,ref,body);ref=url;
  r='href="\#">PROGRAMAS<.*?>EL\sCL';w=plugintools.find_single_match(body,r);
  r='(<!--)?<li>.*?href="([^"]+).*?>([^<]+)';w=plugintools.find_multiple_matches(w,r);
  for i in w:
   if not i[0]=='':
    prefix='[COLORred] (OFF)[/COLOR]'
    if not i[1]=='#': plugintools.add_item(title=i[2]+prefix,url=baseurl+i[1],page=url,thumbnail=thumbnail,fanart=fan,folder=False,isPlayable=False,action='')
   else:
    prefix='';
    if not i[1]=='#': plugintools.add_item(title=i[2]+prefix,url=baseurl+i[1],page=url,thumbnail=thumbnail,fanart=fan,isPlayable=False,action='goltv8')
	
def goltv6(params):
  body='';url=params['url'];ref=params['page'];body,heads=curl_frame(url,ref,body);
  r='<div class="right listado">.*?<div class="limpiar">';w=plugintools.find_single_match(body,r);
  try: r='background-image:url\(([^\)]+).*?javascript:cambiar\(\'([^\']+).*?<h6>([^<]+)';q=plugintools.find_multiple_matches(w,r);
  except:
   try: r='background-image:url\(([^\)]+).*?href="([^\"]+).*?<h6>([^<]+)';q=plugintools.find_multiple_matches(w,r);
   except: exec(messs);sys.exit();
  if not q: tit,resumen=enlaces3(params);q=[];q=[(params['thumbnail'],resumen,tit)];
  for i in q:
   if i[1].startswith('http')>0:
    plugintools.add_item(title=i[2],url=i[1],plot=params['title'],thumbnail=i[0],fanart=fanart,isPlayable=True,folder=False,action='play')
   else:
    purl='plugin://plugin.video.youtube/play/?video_id='+i[1]
    plugintools.add_item(title=i[2],url=purl,page=url,thumbnail=i[0],fanart=fanart,isPlayable=True,folder=False,action='play')
	
def goltv8(params):
  body='';url=params['url'];ref=params['page'];body,heads=curl_frame(url,ref,body);ref=url;
  #http://www.golstadium.es/ver_programa.php?accion=ver&evento=programa&id=2143&tipo=7&cache_id=14268713014tFS64K4Zg
  #http://golstadium.es/listar_programas.php?programa=7&amp;cache_id=1426871204pnen6h9XVR
  r='<div class="right listado">.*?<div class="limpiar">';w=plugintools.find_single_match(body,r);
  try: r='background-image:url\(([^\)]+).*?javascript:cambiar\(\'([^\']+).*?<h6>([^<]+)';q=plugintools.find_multiple_matches(w,r);
  except: pass
  try: r='background-image:url\(([^\)]+).*?href="([^\"]+).*?<h6>([^<]+)';q=plugintools.find_multiple_matches(w,r);
  except: exec(messs);sys.exit();
  if not q: eval(noevent);sys.exit();
  for i in q:
   if i[1].startswith('login')>0:
    purl=baseurl+i[1];plugintools.add_item(title=i[2],url=purl,page=url,thumbnail=i[0],fanart=fanart,isPlayable=True,folder=False,action='enlaces2')
   else:
    purl='plugin://plugin.video.youtube/play/?video_id='+i[1]
    plugintools.add_item(title=i[2],url=purl,page=url,thumbnail=thumbnail,fanart=i[0],isPlayable=True,folder=False,action='play')
   
def enlaces2(params):
    ref=params['url'];cache_id=plugintools.find_single_match(ref,'cache_id=(.*)');
    usrxxx=plugintools.get_setting('otro_user');passxxx=plugintools.get_setting('otro_pwd');
    opts={'cache_id':cache_id,'email2':usrxxx,'password2':passxxx,}
    data=urllib.urlencode(opts);headers={'Referer': ref,};jar=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    opener.addheader=headers;response=opener.open('http://golstadium.es/comprobar_login.php',data)
    response=opener.open(params['page']);akamai=response.read();
    r='(<div class="partido.*?<\/div>.*?<\/div>)';akamai=plugintools.find_multiple_matches(akamai,r);#print akamai,params['title'];sys.exit();
    for i in range(len(akamai)):
	 a=params['thumbnail'].replace('/','\/').replace('.','\.').replace('?','\?');
	 try:
	  a=plugintools.find_single_match(akamai[i],a);
	  if a: k=i;
	 except: pass;
    try: r='href="([^"]+)';akamai=plugintools.find_single_match(akamai[k],r);print akamai,params['title']
    except: eval(noevent);sys.exit();
    response=opener.open(baseurl+akamai);akamai=response.read();#print akamai;sys.exit();
    r='sources:\s?\[\s+\{\s+file:\s?\'?"?([^\'"]+)';
    try: programa=plugintools.find_single_match(akamai,r);play(programa);
    except: eval(messs);sys.exit();
  
def enlaces3(params):
    ref=params['url'];cache_id=plugintools.find_single_match(ref,'cache_id=(.*)');
    usrxxx=plugintools.get_setting('otro_user');passxxx=plugintools.get_setting('otro_pwd');
    opts={'cache_id':cache_id,'email2':usrxxx,'password2':passxxx,}
    data=urllib.urlencode(opts);headers={'Referer': ref,};jar=cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(jar))
    opener.addheader=headers;response=opener.open('http://golstadium.es/comprobar_login.php',data)
    response=opener.open(params['page']);akamai=response.read();
    try: r='href="([^"]+)">'+params['title'];akamai=plugintools.find_single_match(akamai,r);
    except: eval(noevent);sys.exit();
    response=opener.open(baseurl+akamai);akamai=response.read();#print akamai;sys.exit();
    try: r='<h1>([^<]+)';tit=plugintools.find_single_match(akamai,r);
    except: tit='';pass
    try: r='<td class="equipos">([^<]+)';tit+=' ('+plugintools.find_single_match(akamai,r)+')';
    except: pass
    r='sources:\s?\[\s+\{\s+file:\s?\'?"?([^\'"]+)';
    try: resumen=plugintools.find_single_match(akamai,r);
    except: eval(messs);sys.exit();
    return tit,resumen

def play(url):
 if url.startswith('plugin'): xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
 else: plugintools.play_resolved_url(url);