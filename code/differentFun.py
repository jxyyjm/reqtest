#!/usr/local/python2.7.10/bin/python
# -*- coding:utf-8 -*-
# reference: http://docs.python-requests.org/zh_CN/latest/user/quickstart.html
# reference: http://docs.python-requests.org/zh_CN/latest/user/advanced.html

import os
import sys
import json
import time
import requests
reload(sys)
sys.setdefaultencoding('utf-8')
import cchardet as chardet # cchardet is faster #
from lxml import html
from lxml import etree


def getChinesePageContent(url):
	## 'http://newhouse.qd.fang.com/' ##
	try:
		resp  = requests.get(url)
		sysEncode = sys.getfilesystemencoding() # 获取系统的编码方式 #
		page_cont = resp.content # this is the key-point # content is stream of data #
		webEncode = chardet.detect(page_cont).get('encoding', 'utf-8') # 获取页面的编码方式, cchardet比起chardet速度更快#
		if webEncode:
			trans_page = page_cont.decode(webEncode, 'ignore').encode(sysEncode)
		else:	trans_page = page_cont
		return trans_page
	except:
		return ""
'''
url = 'http://newhouse.qd.fang.com/'
trans_page = getChinesePageContent(url)
print trans_page[0:1000]
'''
def UserAgent(url):
	# url 'http://www.xicidaili.com/nn/' #
	# 
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
	try:
		resp = requests.get(url, headers=headers)
		return resp
	except:
		return ""
'''
url = 'http://www.xicidaili.com/nn/'
resp = UserAgent(url)
print resp.headers
'''
def PostData(url):
	### 
	post_data = {'key1':'value1', 'key2':'value2'}
	try:
		resp = requests.post(url, data=post_data)	
		#resp= requests.post(url, json=post_data)
		#resp= requests.post(url, data=json.dumps(post_data))
		print resp.text
	except: pass
'''
url = 'http://httpbin.org/post'
PostData(url)
'''
def ErrorCode(url):
	# It has inner requests.codes.ok #
	# resp.raise_for_status() #
	try:
		resp = requests.respuest('get', url, timeout=3)
		if resp.status_code == requests.codes.ok:
			print "OK"
		else:
			resp.raise_for_status()
			# above can only get HTTPError #
			# http://docs.python-requests.org/en/master/_modules/requests/models/#Response.raise_for_status#
	except requests.exceptions.ConnectionError as e:
		print "######## connect error as following #########:"
		print e
	except OSError as e: #URLError is subset of OSError ##
		print '######## url error as following ###########:'
		print e
'''
url = 'http://www.google.com'
ErrorCode(url)
'''

# cookie is the content saved into the client for distinguish the user #

def getCookie(url):
	## cookie get and print ##
	try:
		resp = requests.get(url)
		if resp.status_code == requests.codes.ok:
			print '####### cookie by brower url:'+url+' as following ##########'
			print resp.cookies
		else:
			resp.raise_for_status()
	except OSError as e:
		print e
'''
url = 'https://passport.csdn.net/account/login'
getCookie(url)
'''

# redirection #
# what is redirection?  http://baike.baidu.com/view/2173335.htm
# how to redirection ?  http://www.labazhou.net/2014/12/redirect-web-page/
# some experience :     http://www.cnblogs.com/workest/p/3891321.html
# redirection type:     301/302/307/meta/other
def ReDirection(url):
	# resp.history can offer a list of rediction url from oldest to now-right #
	try:
		resp = requests.get(url, allow_redirects=True)
		if resp.status_code == requests.codes.ok:
			print '##### url:'+url+", history of rediction as following: #####"
			print 'resp.history is:'+str(resp.history)
			print 'resp.history len is:'+str(len(resp.history))
			#print dir(resp.history)
			print 'resp.status_code is:'+str(resp.status_code)
		else:
			resp.raise_for_status()	
	except OSError as e:
		print e
'''
url = 'http://github.com'
ReDirection(url)
'''
## session ##
# keep some parameters in some time, and tcp-connection will be re-used # it is time-cost-less!! #
# notice: you can set the parameters outside of the session # # high-level, outside-set > session #
# notice: session cannot hold the parameter you set outside #
def UseSession(url):
	s = requests.Session()
	cookies = {'from-my':'my-brower'}
	try:
		resp = s.get(url, cookies=cookies)
		if resp.status_code == requests.codes.ok:
			print '### session with cookies add by you ###'
			#print dir(resp)
			print 'resp.text:'+str(resp.text)
			print 'resp.cookies:'+str(resp.cookies)
		else: resp.raise_for_status()
	except OSError as e: print 'OSError:'+str(e)
	try:
		resp = s.get(url)
		if resp.status_code == requests.codes.ok:
			print '#### same session without cookies add by outside ###'
			print 'resp.text:'+str(resp.text)
			print 'resp.cookies:'+str(resp.cookies)
		else: resp.raise_for_status()
	except OSError as e: print 'OSError:'+str(e)
	print '## NOTICE: from above, we can know that: session will not keey outside-set in different respuest attition##'
	print '## if you want operate cookies in session by hand, you can use requests.utils-method to modify the Session.cookies ##'
	print '## reference: http://docs.python-requests.org/zh_CN/latest/api.html#api-cookies ##'
	print '## http://docs.python-requests.org/zh_CN/latest/api.html#requests.Session.cookies ##'
	print "######## ok, now here is a test as following ########"
	print '######## different requests-version has different method to modify #######'
	print '######## my requests is 2.11.0, so session modify by hand is different with usual ######'
	print '######## my reference: http://docs.python-requests.org/en/master/api/#api-cookies ######'
	mycookies = requests.utils.cookiejar_from_dict(cookies)
	print 'mycookies is:'+str(mycookies)
	print 'type of mycookies is:'+str(type(mycookies))
	s = requests.Session()
	s.cookies.update(mycookies)
	print '## the first time ##'
	resp = s.get(url)
	print resp.text
	print '## the second time ##'
	resp = s.get(url)
	print resp.text
	print '## from the first and second, we have the same cookies, so the session.cookies.update is keep.'
	#print '## after s.clear_session_cookies() ## here there is no remve_cookie_by_name'
	#newmycookies = requests.utils.remove_cookie_by_name(mycookies, 'from-my')
	#s.cookies.update(newmycookies)
	#resp = s.get(url)
	#print resp.text
	
	print '## NOTICE: if you have the lower version requests  ##'
	print '## the code is right ##'
	print 's = requests.Session(cookies=mycookies)'
	print '## but 2.11.0 session without parameters ##'
'''
url = 'http://httpbin.org/cookies'
UseSession(url)
'''
## respuest and response ## 请求和响应 ##
## respuest::header:['Connection', 'Accept-Encoding', 'Accept', 'User-Agent', 'Cookie'] ##
## connection : keep-alive or not  ##
## user-agent : agent proxy        ##
## cookie     : cookies            ##
## response::header:['Date', 'Content-Type', 'Content-Length', 'Connection', 'Server', 'X-Powered-By', 'Vary', 'X-UA-Compatible', 'Content-language', 'Content-Encoding', 'P3P', 'X-Content-Type-Options', 'Last-Modified', 'Backend-Timing', 'X-Varnish', 'Via', 'Accept-Ranges', 'Age', 'X-Cache', 'X-Cache-Status', 'Strict-Transport-Security', 'X-Analytics', 'X-Client-IP', 'Cache-Control']

## 在session里面添加请求的修改内容 ## 
## 在session.send()之前，有个prepare函数,可以在之后修改,同时能够保留session的一些优势，比如cookie的携带 ##
def PrepareInSession(url):
	# modify some info in session #
	s = requests.Session()
	## make a request ##
	data = {'myname':'hello'}
	headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'}
	req = requests.Request('GET', url, headers=headers)
	## prepare ## instead req.prepare() # becauser session.prepare_requests can keey some advince in session-status(for ex: cookie)
	req_prepare = s.prepare_request(req)
	## modify nothing here ##
	print '####### here modify the request.headers["user-agent"] ="python-requests.2.11.0" #########'
	req_prepare.headers['user-agent'] = 'python-requests.2.11.0'
	print 'the first test:'
	print req_prepare.headers
	## get response ##
	try:
		resp = s.send(req_prepare, timeout=5)
		if resp.status_code == requests.codes.ok:
			#print 'headers set by myself:'+str(headers)
			#print 'resp.status_code:'+str(resp.status_code)
			print 'resp.request.headers:'+str(resp.request.headers)
		else: resp.raise_for_status()
	except OSError as e: print 'OSError is:'+str(e)
	## modify here and look the different ##
	print '####### here modify the request.headers["user-agent"] ="python-requests.2.10.0" #########'
	print 'the seacond test:'
	print req_prepare.headers
	##req = requests.Request('GET', url, headers=headers)#
	#擦，这里很奇怪的是，req_prepare应该是保存了cookie的 #但是再次用req_prepare访问的时候，就没有cookie了 #
	#notice：如果用session的这个cookie保存的prepare时，还得注意一下 #
	req_prepare.headers['user-agent'] = 'python-requests.2.10.0'
	try:
		resp = s.send(req_prepare, timeout=5)
		if resp.status_code == requests.codes.ok:
			#print 'headers set by myself:'+str(headers)
			#print 'resp.status_code:'+str(resp.status_code)
			print 'resp.request.headers:'+str(resp.request.headers)
		else: resp.raise_for_status()
	except OSError as e: print 'OSError is:'+str(e)
	# 
'''
url = 'http://en.wikipedia.org/wiki/Monty_Python'
PrepareInSession(url)
'''
## SSL certification ##(Secure Socket Layer)##
## it is to make sure the security ##
#requests.request('GET', url, vert='/path/to/certfile')
#requests.get(url, verify='/path/to/certfile')
#s=requests.Session(); s.verify='/path/to/cerfile'

## Body Content WorkFlow ##
## you can get the data not immediately until you access the Response.content ## by setting: stream=True
## notice: when stream=True, request-connect will be used until you consume all the data or call Response.close ##
##                           it means this connect will not be put back connect-pool ##
##                   to save: from contextlib import closing
#from contextlib import closing
#with closing(requests.get('http://httpbin.org/get', stream=True)) as r:
#	# do anthing with the response here # and without risk of above #
#	if int(r.headers['content-length'])>1000:
#		page_cont = r.content


# Streaming Uploads #
# stream upload will help you send stream or files without read them into memory #
# with open('/your/file', 'rb') as f:
#	requests.post(url, data = f)
# notice: open file in binary mode is best #


# Event Hooks # 监控某个/些行为，是种消息处理机制 #
# You can assign a hook function on a per-request basis by passing a 
# {hook_name: callback_function} dictionary to the hooks request parameter
#def print_url(r, *args, **kwargs):
#	print(r.url)
#requests.get('http://httpbin.org', hooks=dict(response=print_url))
# result: http://httpbin.org
# result: <Response [200]>

# Http Proxies # 代理 #
def SetProxies(url):
	proxies={
	'http':'180.173.64.152:8118',
	'http':'120.25.105.45:81',
	}
	try:
		resp = requests.get(url, proxies=proxies)
		if resp.status_code == requests.codes.ok:
			print resp.headers
		else: print resp.raise_for_status()
	except OSError as e: print e
'''
url = 'http://jm.fang.com/'
SetProxies(url)
'''
# Socks Proxies #
#pip install requests[socks]
#proxies={
#	'http':'socks5://user:pass@host:port',
#	'https':'socks5://user:pass@host:port',
#}

# Transport Adapters # 在某些情况下，需要自己定义适配器 #
'''
import ssl
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
class Ssl3HttpAdapter(HTTPAdapter):
    """"Transport adapter" that allows us to use SSLv3."""
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_version=ssl.PROTOCOL_SSLv3) # here #

s = requests.Session()
MyAdapter = Ssl3HttpAdapter()
s.mount('http://www.github.com', MyAdapter) # 将此适配器关联到某个前缀的网址上# 所有调用这个session的请求都会检查url是否是以这个为前缀，判断是否用新定义的适配器 #
'''
























