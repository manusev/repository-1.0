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
thumb="https://pp.vk.me/c616517/v616517472/8bcd/icKxFe4qqAQ.jpg"
fan="http://www.air.io/wp-content/uploads/Torrent-TV.jpg"
fan='https://pp.vk.me/c616517/v616517472/8bcd/icKxFe4qqAQ.jpg'
burl='http://t-tv.org/?channel=canalplus-liga&source=s1';
baseurl='http://t-tv.org/';
messs='plugintools.message("ERROR","[COLOR=yellow]Cambios en la web[/COLOR]","[COLOR=red](avisar en el foro)[/COLOR]")'
nolink='plugintools.message("ATENCION","[COLOR=yellow]Canal sin emicion[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'
pxmess='plugintools.message("ATENCION","[COLOR=yellow]Necesita proxy RDS!!![/COLOR]","[COLOR=red](se intenta abrir)[/COLOR]")'
dlg="xbmcgui.Dialog().notification('ESPERE',mssg,icon,timp)"

def ttv0(params):
  mssg='buscando canales...';timp=1000;exec(dlg);
  plugintools.add_item(title='[COLOR blue]T-TV.org (categorias)[/COLOR]',thumbnail=thumb,fanart=fan,isPlayable=False,folder=False)
  request_headers=[];body,response_headers=read_body_and_headers(burl,headers=request_headers);
  r='<div\sid="channels"(.*?)<div\sclass="loading"';w=plugintools.find_single_match(body,r);
  r='<a\shref(.*?flag.*?)<\/a>';w=plugintools.find_multiple_matches(w,r);tit={}
  for j in range(0,len(w)):
   r='flag-([^"]+)"\stitle="([^"]+)';
   try:
    q=plugintools.find_multiple_matches(w[j],r);
    if q[0][1] not in tit: tit.update({q[0][1]:q[0][0]});
   except: pass;
  tit.update({'[COLOR red]Otros[/COLOR]': thumb});
  try: from collections import OrderedDict;tit=OrderedDict(sorted(tit.items()));#print "Value : %s" %  titnew
  #except: from ordereddict import OrderedDict;tit=OrderedDict(sorted(tit.items()));#intent for python 2.6 (aun asi no va en spmc)
  except: tit=dict(sorted(tit.items()));#possible solution for spmc?!?
  for k,v in tit.iteritems():
   plugintools.add_item(action='ttv1',title=k,url=k,thumbnail=v,fanart=v,isPlayable=False,folder=True);

def ttv1(params):
 urt=params.get('thumbnail');tit=re.sub('(\[.*?\])','',params.get('title'));
 plugintools.add_item(title='[COLOR blue]'+tit+'[/COLOR]',thumbnail=thumb,fanart=fan,isPlayable=False,folder=False);
 try:
  request_headers=[];body,response_headers=read_body_and_headers(burl,headers=request_headers);
  r='<div\sid="channels"(.*?)<div\sclass="loading"';w=plugintools.find_single_match(body,r);
 except: pass
 try:
  r='(<a\shref.*?<\/a>)';w=plugintools.find_multiple_matches(w,r);
 except: pass
 din=[];
 if tit=='Otros': din=[x for x in w if x.find('flag-"')>=0];
 else: din=[x for x in w if x.find('flag-'+urt)>=0];
 for x in din:
  try: r='href="([^"]+).*?id="([^"]+)';w=plugintools.find_multiple_matches(x,r);
  except: pass
  try: r='img\ssrc="([^"]+)';thum=baseurl+plugintools.find_single_match(x,r);
  except: thum=thumb;pass
  tit=w[0][1].replace('c-','').replace('-',' ').title()
  plugintools.add_item(action='ttv2',title=tit,url=baseurl+w[0][0],thumbnail=thum,fanart=fan,isPlayable=False,folder=False);
 
def ttv2(params):
 tit=params.get('title');url=params.get('url');mssg='creando servicio P2P...';timp=3000;
 request_headers=[];body,response_headers=read_body_and_headers(url,headers=request_headers);
 if str(response_headers).find('location')>=0:
  r='location\',\s\'([^\']+)';url=plugintools.find_single_match(str(response_headers),r);
  request_headers=[];body,response_headers=read_body_and_headers(url,headers=request_headers);
 try:
  r='var\sid\s=\s\'([^\']+)';url=plugintools.find_single_match(body,r);
  exec(dlg);url='plugin://plugin.video.p2p-streams/?url='+url+'&mode=1&name='+urllib.quote_plus(tit);
  print url;xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
 except: exec(messs);