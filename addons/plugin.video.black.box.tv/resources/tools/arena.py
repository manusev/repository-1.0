# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para Black Box TV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
# Version 0.1.8 (19.02.2015)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *

art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/art', ''))
playlists = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/playlists', ''))
tmp = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cipqtv/tmp', ''))
icon = art + 'icon.png';fanart = 'fanart.jpg';body='';data=''
messs='plugintools.message("CipQ-TV","[COLOR=red]Cambios en la web fuente[/COLOR]","[COLOR=blue](avisar en el foro)[/COLOR]")'
mssg='Creando servicio P2P...';timp=3000;
dlg="xbmcgui.Dialog().notification('Cargando',mssg,icon,timp)"
baseurl='http://go.arenavision.in/';
#http://arenavision.in/rss.xml

def arena0(params):
 thumb = 'http://i18.servimg.com/u/f18/19/08/63/44/av10.jpg'
 fanart='http://i18.servimg.com/u/f18/19/08/63/44/agenda11.jpg'
 baseurl='http://go.arenavision.in/';body='';ref=baseurl;
 try: baseurl='http://go.arenavision.in/';url=baseurl+'agenda';data=curl_frame(url,ref,body)
 except: pass
 try: baseurl='http://arenavision.in/';url=baseurl+'agenda';data=curl_frame(url,ref,body)
 except: pass
 try: baseurl='http://my.arenavision.in/p/';url=baseurl+'agendaschedule.html';data=curl_frame(url,ref,body)
 except: pass
 try: baseurl='http://my.arenavision.in/p/';url=baseurl+'guidetv.html';data=curl_frame(url,ref,body)
 except: pass
 try: baseurl='http://www.arenavision.in/p/';url=baseurl+'schedule.html';data=curl_frame(url,ref,body)
 except: pass
 purl=baseurl; 
 try:
  dats=plugintools.find_single_match(data,'<div\sclass=\'?"?post-body\sentry-content.*?>(.*?)<\/div>');
  if dats: data=dats
  else:
   try:
    data=plugintools.find_multiple_matches(data,'(\d{2}[^<]+)<br\s?\/?>');cabeza="[COLOR=white][B]Eventos [COLOR=blue]Deportivos [COLOR=white]ArenaVision[/B][/COLOR]";
    plugintools.add_item( action="" , title=cabeza , url="" ,thumbnail=thumb ,fanart=fanart , isPlayable=False, folder=False );#print data
   except: eval(messs);sys.exit();
 except: eval(messs);sys.exit();
 for match in data:
  #print match
  datae='(\d{2}\/\d{2}\/\d{2,4})';ora='(\d{2}:\d{2})';ave='(\/?AV\d{1,2})';liga='(\(.*\))';cet='(\s?CET\s?.*?:\s?)';
  try:
   datae=plugintools.find_single_match(match,datae);#print "\n"+datae;
   ora=plugintools.find_single_match(match,ora);#print "\n"+ora;
   liga=plugintools.find_single_match(match,liga);#print "\n"+liga;
   ave=plugintools.find_multiple_matches(match,ave);aver="".join(ave);#print "\n",ave;
   cet=plugintools.find_single_match(match,cet);#print "\n",ave;
   rest=match.replace(datae,'').replace(ora,'').replace(aver,'').replace(liga,'').replace(cet,'');#str(rest.strip())
  except IndexError: pass
  title="[COLOR=red][B] "+str(ora)+"[/COLOR][COLOR=white] "+str(datae)+"\n[COLOR=green]"+str(rest).upper() + "\t [COLOR=blue]"+str(liga).lower() + "[/COLOR][/B][/COLOR]";
  plugintools.add_item( action="arena1" , title=title , url=str(ave) ,thumbnail=thumb ,fanart=fanart , isPlayable=False, folder=False );
 
def arena1(params):
 url = params.get("url");link=url.replace("'","").replace("[","").replace("]","").replace(",","").replace("/","").split();#print link;
 try:
  for idx, item in enumerate(link):
   if any([item=='AV13',item=='AV14']): item=item+'[COLOR=green][B] (flash)[/B][/COLOR]';link[idx] = item
   if any([item=='AV1',item=='AV2',item=='AV3',item=='AV4',item=='AV5',item=='AV6',item=='AV15']): item=item+' [COLOR=green][B](Acestream)[/B][/COLOR]';link[idx]=item
   if any([item=='AV7',item=='AV8',item=='AV9',item=='AV10',item=='AV11',item=='AV12',item=='AV16']): item=item+' [COLOR=green][B](Sopcast)[/B][/COLOR]';link[idx]=item
 except: pass
 try:
  link=link;index=0;ch=0;
  index=plugintools.selector(link,title='''[COLOR=red][B]ArenaVision[/B][/COLOR]:''');
  ch=link[index];
  if ch:
   if index > -1: arena2(ch);sys.exit();
   else: sys.exit()
 except KeyboardInterrupt: pass;
 except IndexError: raise;

def arena2(ch):
 '''
 try:
  ch=re.sub('\s\[.*','',ch);#print "ch"+ch
 except: pass
 '''
 r='\d{1,2}';ch=plugintools.find_single_match(ch,r);ch=str(int(ch)-1);print 'CH='+ch
 url=baseurl+'arenavision'+str(int(ch)+1);ref=url;body='';
 try: data=curl_frame(url,ref,body);
 except:
  plugintools.message("Arenavision","\n",'\n[COLOR=blue][B]Prueba otro canal de la lista[/COLOR]\n[COLOR=red](No hay enlace en AV'+str(int(ch)+1)+')[/B][/COLOR]');
  sys.exit();pass
 match = re.compile('sop://(.+?)"').findall(data)
 if match: exec(dlg);url='plugin://plugin.video.p2p-streams/?url=sop://'+match[0]+'&mode=2&name=Arenavision '+ch+' (sop)';
 else:
  match = re.compile('this.loadPlayer\("(.+?)"').findall(data)
  if match: exec(dlg);url='plugin://plugin.video.p2p-streams/?url='+match[0]+'&mode=1&name=Arenavision '+ch+' (ace)'
  else:
   match = plugintools.find_single_match(data,'<script\ssrc="(http:\/\/www\.iguid[^"]+)');
   if match: match = plugintools.find_single_match(match,'embed\/([^\&]+)');url=iguide(match,ref);#if is iguide
   else:
    print 'streamup';match = plugintools.find_single_match(data,'src="(https:\/\/streamup[^"]+)');#if is streamup
    if match:
	 body=curl_frame(match,url,'');match = plugintools.find_single_match(body,'flashvars\.channel\s=\s\'([^\']+)');
	 url='rtmp://167.114.157.89/app playpath='+match+' swfUrl=https://streamup.com/assets/StreamupVideoChat.swf pageUrl='+url;
    else: print "UNKNOWN";eval(nocode);#aqui entran otros parsers !!!
   #body='';url='http://www.iguide.to/embedplayer_new.php?width=640&height=480&channel='+match+'&autoplay=true';
   #body=curl_frame(url,ref,body);url=iguide(url,body);
   #<iframe id="su-ivp" src="https://streamup.com/rooms/avision18s-Channel/plugins/video/show?startMuted=false" 
 run_arena(url)

def run_arena(url):
 if url.startswith("rtmp")==True: plugintools.direct_play(url)
 elif url.startswith("plugin")==True: xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
 else: mssg='Servidor desconocido!';exec(dlg);print "Invalid media type!";sys.exit();
		
def curl_frame(url,ref,body):
 request_headers=[];request_headers.append(["User-Agent","Chrome/26.0.1410.65 Safari/537.31","Referer",ref,"Cookie","beget=begetok"])
 #request_headers.append(["User-Agent","Chrome/26.0.1410.65 Safari/537.31","Referer",ref,"Cookie","beget=begetok;has_js=1;","X-Drupal-Cache","HIT","X-Generator","Drupal 7 (http://drupal.org)"])
 body,response_headers=plugintools.read_body_and_headers(url,headers=request_headers);
 return body
 
def iguide(match,ref):
 url='http://www.iguide.to/embedplayer_new.php?width=640&height=480&channel='+match+'&autoplay=true';body=curl_frame(url,ref,'');
 if body.find('domain protected'): print 'Cookie error!';sys.exit();
 p=re.compile(ur'(\$\.getJSON\(\'?"?.*?)<\/script>',re.DOTALL);pars=re.findall(p,body);print p,pars
 try:
  pars=str(pars[0]);pars=pars.replace("\n","").replace("\t","");
  tokserv=plugintools.find_single_match(str(pars),'getJSON\(\'?"?([^\'"]+)');
  strmr=plugintools.find_single_match(str(pars),'streamer\'?"?:\s?\'?"?([^\'"]+)');
  plpath=plugintools.find_single_match(str(pars),'file\'?"?:\s?\'?"?([^\.]+)');
  swf=plugintools.find_single_match(str(pars),'flash\'?"?,\s?src\'?"?:\s?\'?"?([^\'"]+)');
  body='';tok=curl_frame(tokserv,url,body);tok=plugintools.find_single_match(str(tok),'token":"([^"]+)');
  url = str(strmr)+' playpath='+str(plpath)+' swfUrl='+str(swf)+' live=1 pageUrl='+url+' token='+tok
  return url
 except: plugintools.message("Arenavision","\n",'\n[COLOR=blue][B]Prueba otro canal de la lista[/COLOR]\n[COLOR=red](No hay enlace)[/B][/COLOR]');sys.exit();