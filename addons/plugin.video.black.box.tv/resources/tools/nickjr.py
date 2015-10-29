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
thumb="http://sweetiesfreebies.com/wp-content/uploads/2014/05/pawpatroldvdsweepstakes.jpg"
fan='http://images.wikia.com/paw-patrol-fanon/images/archive/5/50/20140309083220!Wiki-background'
baseurl='http://www.nickjr.com/dynamo/video/data/mrssGen.jhtml?type=normal&hub=home&loc=sidebar&mode=playlist&dartSite=nickjr.nol&mgid=mgid%3Acms%3Aplaylist%3Anickjr.com%3A118948&demo=null&block=true';
messs='plugintools.message("ERROR","[COLOR=yellow]Cambios en la web[/COLOR]","[COLOR=red](avisar en el foro)[/COLOR]")'
nolink='plugintools.message("ATENCION","[COLOR=yellow]Canal sin emicion[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'
pxmess='plugintools.message("ATENCION","[COLOR=yellow]Necesita proxy RDS!!![/COLOR]","[COLOR=red](se intenta abrir)[/COLOR]")'
dlg="xbmcgui.Dialog().notification('ESPERE',mssg,icon,timp)"

def njr0(params):
 mssg='buscando programas...';timp=1000;exec(dlg);skin_name = xbmc.getSkinDir();
 plugintools.add_item(title='[COLORcyan][B] ***    PAW[COLORyellow]   PATROL    ***[/B][/COLOR]',thumbnail=thumb,fanart=fan,isPlayable=False,folder=False)
 request_headers=[];body,response_headers=read_body_and_headers(baseurl,headers=request_headers);
 r='<item>(.*?)<\/item>';w=plugintools.find_multiple_matches(body,r);
 if skin_name.find('titan') or skin_name.find('nox'): set_view(MOVIES,view_code=504);
 else: set_view(LIST,view_code=52)
 for i in w:
  r='<title>([^<]+)';tit=plugintools.find_single_match(i,r);
  r='<description><\!\[CDATA\[([^\]]+)';desc='[COLORred]'+plugintools.find_single_match(i,r)+'[/COLOR]';print desc
  r='<media:content.*?url="([^"]+)';mc=plugintools.find_single_match(i,r);
  r='<media:thumbnail.*?url="([^"]+)';th=plugintools.find_single_match(i,r);
  plugintools.add_item(title='[COLORyellow][I]'+tit+'[/I][/COLOR]',action='njr1',url=mc,plot=str(desc),thumbnail=th,fanart=fan,isPlayable=True,folder=False)

def njr1(params):
 try:
  request_headers=[];body,response_headers=read_body_and_headers(params['url'],headers=request_headers);
 except: exec(messs);pass
 r='bitrate="([^"]+).*?<src>([^<]+)';q=[];y=[];subtitles=[];w=plugintools.find_multiple_matches(body,r);
 r='"(cea-608|ttml|vtt)"\ssrc="([^"]+)';subtitles=plugintools.find_multiple_matches(body,r);print subtitles;
 if not w: exec(nolink);sys.exit();
 for x in w: q.append(' quality: [COLOR red]('+x[0]+')[/COLOR]');y.append(x[1]);
 if len(y)==0: exec(nolink);sys.exit();
 try:
  link=q;index=0;ch=0;
  index=plugintools.selector(link,title=params['title']);
  ch=y[index];params={"title":q[index],"tit":q[index]};
  if ch:
   if index > -1: play_resolved_url(ch);
 except KeyboardInterrupt: pass;
 except IndexError: raise;