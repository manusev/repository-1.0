# -*- coding: utf-8 -*-
#--------------------------------------------------------
#  creado por quequeQ para Black Box TV
# (http://forum.rojadirecta.es/member.php?1370946-quequeQ)
# (http://xbmcspain.com/foro/miembro/quequino/)
#  cipromario(at)gmail(dot)com
# Version 0.0.7 (26.05.2015)
#--------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#--------------------------------------------------------

from __main__ import *
thumb="http://dinozaptv.files.wordpress.com/2011/11/dtv1.jpg"
fanart="http://dinozaptv.files.wordpress.com/2011/11/dtv1.jpg"
nolink='plugintools.message("ATENCION","[COLOR=yellow]Canal sin emicion[/COLOR]","[COLOR=red](no hay enlaces)[/COLOR]")'

def dzap0(params):
 plugintools.add_item(title="[COLOR=red][B]D[COLOR=blue]ino[COLOR=red]Z[COLOR=blue]ap [/B][/COLOR]",thumbnail=thumb,fanart=thumb,folder=False );
 plugintools.add_item(action="dzap02",title="Todos los canales",thumbnail=thumb,fanart=thumb,folder=True );
 plugintools.add_item(action="dzap01",title="[COLOR=green]Programacion hoy[/COLOR]",thumbnail=thumb,fanart=thumb,folder=True );
 plugintools.add_item(action="dzap03",title="[COLOR=gray]Programacion mañana[/COLOR]",thumbnail=thumb,fanart=thumb,folder=True );
 
def dzap02(params):
 try: url='http://www.dinozap.tv/';ref=url;body='';body=curl_frame(url,ref,body)
 except: url='http://www.dinozap.info/';ref=url;body='';body=curl_frame(url,ref,body)
 thumb="http://dinozaptv.files.wordpress.com/2011/11/dtv1.jpg"
 fanart="http://dinozaptv.files.wordpress.com/2011/11/dtv1.jpg"
 plugintools.add_item(title="[COLOR=red][B]D[COLOR=blue]ino[COLOR=red]Z[COLOR=blue]ap by quequino[/B][/COLOR]",thumbnail=thumb,fanart=thumb,folder=False );
 data=plugintools.find_single_match(body,'(navbar-nav.*<\/ul>)');
 data=plugintools.find_multiple_matches(data,'href="\?id=1([^"]*)');
 for i in data:
  title="[COLOR=green]Dino[COLOR=yellow]Zap[COLOR=red] "+str(int(i)-10)+"[/COLOR][/COLOR][/COLOR]";
  plugintools.add_item(action="dzap2",url=i,title=title,thumbnail=thumb,fanart=thumb,isPlayable=True,folder=False )

def dzap03(params):
 akamai=''
 try: url='http://www.dinozap.tv/prog.txt';ref=url;body='';body=curl_frame(url,ref,body)
 except: url='http://www.dinozap.info/prog.txt';ref=url;body='';body=curl_frame(url,ref,body)
 try:
  t=plugintools.find_single_match(body,'[X]{5,25}(.*)');#t is tomorrow !!!
  daytitle=plugintools.find_single_match(t,'[X\r\n]+(.*?)[\r\n]');t=t.replace(daytitle+'\r\n','');
  plugintools.add_item(title="[COLOR=blue]Programacion "+daytitle+"[/COLOR]",thumbnail=thumb,fanart=thumb,folder=False );
  pat=re.compile(ur'(CHANNEL.*?)(?=[XCHANEL]{7})',re.DOTALL);channel=re.findall(pat,t);
  doepg(channel)
 except: pass

def dzap01(params):
 akamai='';body='';
 try:
  url='http://www.dinozap.info/prog.txt';ref=url;body=curl_frame(url,ref,body);t=plugintools.find_single_match(body,'(.*?[X]{5,25})');
  if not len(t)>0: url='http://www.dinozap.tv/prog.txt';ref=url;body=curl_frame(url,ref,body);
 except: pass
 try:
  t=plugintools.find_single_match(body,'(.*?[X]{5,25})');#t is today !!!
  daytitle=plugintools.find_single_match(t,'(.*?)[\r\n]');t=t.replace(daytitle+'\r\n','');
  plugintools.add_item(title="[COLOR=blue]Programacion "+daytitle+"[/COLOR]",thumbnail=thumb,fanart=thumb,folder=False );
  pat=re.compile(ur'(CHANNEL.*?)(?=[XCHANEL]{7})',re.DOTALL);channel=re.findall(pat,t)
  doepg(channel)
 except: 
  daytitle=plugintools.find_single_match(body,'(.*?)[\r\n]');t=daytitle.replace('\r\n','');
  plugintools.add_item(title="[COLOR=blue]Programacion "+daytitle+"[/COLOR]",thumbnail=thumb,fanart=thumb,folder=False );
  pat=re.compile(ur'(CHANNEL.*?)(?=[XCHANEL]{7})',re.DOTALL);channel=re.findall(pat,t)
  doepg(channel)
  pass

def doepg(channel):
 epg=[];
 for i in channel:
  #print i
  ch='(CHANNEL\s?\d{1,2})';ch=plugintools.find_single_match(i,ch);i=i.replace(ch,'');a=i.split('\r\n');a=filter(None,a);
  #print ch;print a
  for j in a:
   k=plugintools.find_single_match(j,'\d{2}:\d{2}');
   if k: j=j
   else: j='3'+j
   epg+=[(j+'€€€'+ch)];
 epg=sorted(epg);mec='';link=[];
 epg=iter(epg);
 for i in epg:
  try:
   par='(\d{1,2}:\d{2})(.*?)(\([^\)]+.).*?€€€.*?(\d{1,2})';par=plugintools.find_multiple_matches(i,par);meci=str(par[0][1]);lin=str(int(par[0][3])+10);
   try: w=re.findall(re.compile(r'(3(\d{1}:\d{2}))'),str(par[0][0]));c=re.sub(w[0][0],'0'+w[0][1],par[0][0])
   except: c=par[0][0]
   title="[COLOR=green]"+str(c)+ "[COLOR=yellow] "+meci.upper() + " [COLOR=red]"+str(par[0][2]).lower() + "[/COLOR][/COLOR][/COLOR]";
   plugintools.add_item(action="dzap2",title=title,url=str(lin),thumbnail=thumb,fanart=thumb,isPlayable=True,folder=False)
   mec=meci;
  except: pass
 return

def dzap2(params):
 url = params.get("url");
 id=100+int(str(url));#pid=str(url);
 url='http://www.dinozap.info/redirect/channel.php?id='+str(id)+'&width=680&height=390&autostart=true';
 ref='http://www.dinozap.info/';body='';body=curl_frame(url,ref,body);print str(id);reff=url;url=plugintools.find_single_match(body,'iframe\ssrc="([^"]+)');
 body=curl_frame(url,reff,'');r='function\sgetURL03(.*?)setStream\(data\);';
 try: hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
 except:eval(nolink);sys.exit();
 try:body=plugintools.find_single_match(body,r);
 except:eval(nolink);sys.exit();
 try:r='[\'|"]result\d{1}[\'|"]\s?:\s?[[](.*?)[]]';p=plugintools.find_multiple_matches(body,r);
 except:pass
 if not p:
  try:r='var\s(.*?)\s=\s?[\'|"]([^\'"]+)';p=plugintools.find_multiple_matches(body,r);jq_cback(p,url);#jquery callback method!!!
  except:sys.exit();
 else:var_1_2_b64(p,url);#var1,var2 base64 method!!!
def jq_cback(p,url):
 Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));jquery = '%s?callback=jQuery17049106340911455604_%s&v_cod1=%s&v_cod2=%s&_=%s';
 jurl=jquery%(b64_error(p[2][1]).decode('base64'),Epoc_mil,urllib.quote_plus(p[0][1]),urllib.quote_plus(p[1][1]),Epoc_mil);
 r='"result\d{1}":"([^"]+)';p='plugintools.find_multiple_matches(body,r)';body=curl_frame(jurl,url,'');#jQuery17036659089173190296
 swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';app=plugintools.find_single_match(eval(p)[1].replace('\\',''),'1735\/([^"]+)');
 q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
 w=eval(p)[1].replace('\\','')+' app='+app+' playpath='+eval(p)[0]+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+url+' live=1 timeout=15'
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();
def var_1_2_b64(p,url):
 r='var\s('+p[0]+'|'+p[1]+')\s?=\s?[\'|"](.*?)[\'|"]';p=plugintools.find_multiple_matches(body,r);
 swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';app=plugintools.find_single_match(b64_error(p[1][1]).decode('base64'),'1735\/([^"]+)');
 q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
 w=b64_error(p[1][1]).decode('base64')+' app='+app+' playpath='+b64_error(p[0][1]).decode('base64')+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+url+' live=1 timeout=15'
 if w: plugintools.play_resolved_url(w);sys.exit();
 else: eval(nolink);sys.exit();

def businessapp2(url,ref,bodi):
  bodi=curl_frame(url,ref,'');reff=url;url=plugintools.find_single_match(bodi,'<iframe src="([^"]+)');k=url;body=curl_frame(url,reff,'');
  hidd='type="hidden"\sid="([^"]+)"\svalue="([^"]*)';hidd=plugintools.find_multiple_matches(body,hidd);
  swfUrl='http://www.businessapp1.pw/jwplayer5/addplayer/jwplayer.flash.swf';Epoc_mil=str(int(time.time()*1000));EpocTime=str(int(time.time()));
  app=plugintools.find_single_match(hidd[2][1].decode('base64').replace('\\',''),'1735\/([^"]+)');
  q='%s app=%s playpath=%s flashver=WIN%5C2017,0,0,134 swfUrl=%s swfVfy=1 pageUrl=%s live=1 timeout=15';#dzap,tvdirecto
  w=hidd[2][1].decode('base64').replace('\\','')+' app='+app+' playpath='+hidd[1][1].decode('base64')+' flashver=WIN%5C2017,0,0,134 swfUrl='+swfUrl+' swfVfy=1 pageUrl='+k+' live=1 timeout=15'
  #print w;sys.exit();
  if w: plugintools.play_resolved_url(w);sys.exit();
  else: eval(nolink);sys.exit();
   
def b64_error(b64_str):
 missing_padding=4-len(b64_str)%4
 if missing_padding: b64_str+=b'='*missing_padding;return b64_str
 
def curl_frame(url,ref,body):
 request_headers=[];request_headers.append(["User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko"])
 request_headers.append(["Referer",ref]);body,resp=plugintools.read_body_and_headers(url,headers=request_headers,timeout=30);
 return body