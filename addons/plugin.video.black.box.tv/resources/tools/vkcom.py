from __main__ import *

def catch_vkcom(name,url):
 try:
  request_headers=[];y=[];
  body,response_headers=read_body_and_headers(url,headers=request_headers);
  url=[x[1] for x in response_headers if x[0]=='location'][0];
  if not url: print '********OK';pass
  else:
   try:
    body,response_headers=read_body_and_headers(url,headers=request_headers);
   except: pass
 except:pass
 try:
  r='url720=(http:\/\/[\w\W]+?.mp4?[\w\W]+?)&';w=plugintools.find_single_match(body,r);y.append(w);
 except: pass
 try:
  r='url480=(http:\/\/[\w\W]+?.mp4?[\w\W]+?)&';w=plugintools.find_single_match(body,r);y.append(w);
 except: pass
 try:
  r='url360=(http:\/\/[\w\W]+?.mp4?[\w\W]+?)&';w=plugintools.find_single_match(body,r);y.append(w);
 except: pass
 try:
  r='url240=(http:\/\/[\w\W]+?.mp4?[\w\W]+?)&';w=plugintools.find_single_match(body,r);y.append(w);
 except: pass
 return filter(None,y)[0]#autoselect best quality;return entire list for multilink qualities selector!!!