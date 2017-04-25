#!/usr/local/python2.7.10/bin/python
# -*- coding:utf-8 -*-

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import requests
import cchardet as chardet
from lxml import html
from lxml import etree


def getChinesePageContent(url):
	## 获取包含中文的页面内容 ## 包括自动编解码 ##
	try:
		req  = requests.get(url)
		sysEncode = sys.getfilesystemencoding() # 获取系统默认编码 #
		page_cont = req.content # this is the key-point # content is stream of data #
		webEncode = chardet.detect(page_cont).get('encoding', 'utf-8') # 获取页面编码 #
		if webEncode:
			trans_page = page_cont.decode(webEncode, 'ignore').encode(sysEncode)
		else:	trans_page = page_cont
		return trans_page
	except:
		return ""
if __name__=="__main__":
	#url  = 'http://newhouse.jn.fang.com/'
	#url  = 'http://lvdicheng0531.fang.com/'
	url  = 'http://news.sohu.com/20160908/n467914641.shtml'
	page = getChinesePageContent(url)
	print "获取页面内容,url is:"+url
	print page[0:2000]
	page_tree = html.fromstring(page)
	#page_tree = etree.HTML(page)
	print "type of page_tree is: "+str(type(page_tree))
	href_list = page_tree.xpath('//div[@class="information"]')
	print "len of href_list is:"+str(len(href_list))
	print href_list[0].text
