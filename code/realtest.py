#!/usr/bin/python2.7
# -*- coding:utf-8 -*-
###################################################
###################################################
############ now a real-practical test ############
############ sina weibo login/get text ############
###################################################
###################################################

import os
import sys
import json
import time
import requests
import cchardet as chardet
from lxml import etree, html
reload(sys)
sys.setdefaultencoding('utf-8')

url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=14736622755473'
# method = post #
postdata = {
	'username':'fuyu82648@163.com',
	'password':'fuyu826481086',
	}
# 整个请求命令 #
# rsa2加密方式, su--用户名, sp--密码 #
#curl 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=1473662810543' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3' -H 'Content-Type: application/x-www-form-urlencoded' -H 'Cookie: U_TRS1=00000008.bdb714e4.579853e4.d2600b7e; UOR=cn.bing.com,www.sina.com.cn,; SGUID=1470998391127_54979975; SINAGLOBAL=218.30.116.4_1470998393.341977; ULV=1473662777767:6:2:2:218.30.116.10_1473662773.161744:1473662773327; lxlrttp=1473659488; SCF=AtgHDXbf4Fvaa426jbdL3cVA9qkhOdE7X3QwNeyAI8oWiLNy8fdlc1zUXNRebcg-YBA1qVb08yew0QLeBAXw2y8.; SUB=_2AkMg6JFfdcNhrAZRm_0dxG3rbItH-jzEiebBAn7tJhMyAhh87mgRqSVwhA3EVKu1JzuoBLsEmOv407QtNg..; SUBP=0033WrSXqPxfM72wWs9jqgMF55529P9D9WFrREg4oG5G8zfjq3yxrQBo5JpV8K2f1K27SKzfSozcdKW5McLVqC4odntt; U_TRS2=00000009.ffd22aec.57d64f2c.a639f0c5; Apache=218.30.116.10_1473662773.161744; lxlrtst=1473659488_c' -H 'Host: login.sina.com.cn' -H 'Referer: http://www.sina.com.cn/' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0' -H 'origin: http://www.sina.com.cn' --data 'entry=homepage&gateway=1&from=&savestate=0&useticket=0&pagerefer=&vsnf=1&su=ZnV5dTgyNjQ4JTQwMTYzLmNvbQ%3D%3D&service=sso&servertime=1473662809&nonce=Q0J13W&pwencode=rsa2&rsakv=1330428213&sp=af69d0009bbeb88f147c1886805c92291017503cf74942077683e9bfcf03990710056abb4f8089349afe0fd3276a394926681546e9c6566ab1ac99020ef0e67c728c7fe4a0601258bb8306d4078ceecf570da9ef2106efa61bbc339857361fd0537d14347db4d5314d29c2b6c5005e7f897e428c37c8eb7525c9f708128fa49e&sr=1920*1200&encoding=UTF-8&cdult=3&domain=sina.com.cn&prelt=59&returntype=TEXT'




