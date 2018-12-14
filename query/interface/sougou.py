import re
import time
import json
import requests
requests.packages.urllib3.disable_warnings()
from lxml import etree
# from multiprocessing import Process

from tools.redis_db import cache
from tools.phantomjs import feed_cookies
from tools.tool import get_current_timestamp


headers = {
"Host":"www.sogou.com",
"Connection":"keep-alive",
"User-Agent":("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) App"
	"leWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"),
"Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
}


def get_address(phone):
	"""
		获取手机号归属地的api
	"""
	url = 'https://www.sogou.com/websearch/phoneAddress.jsp'
	params = {
	'phoneNumber':phone,
	'cd':'handlenumber',
	'isSogoDomain':'0'
	}
	try:
		text = requests.get(url,headers=headers,params=params,verify=False).text
		msg = re.search('"(.*?)"',text)[1]
		return msg
	except Exception as e:
		return '全国'

# # for api search ......
# def get_tag(phone):
	
# 	url = 'https://www.sogou.com/reventondc/inner/vrapi'
# 	params = {
# 		'number':phone,
# 		'type':'json',
# 		'isSogoDomain':'0',
# 		'callback':'show'
# 	}
# 	try:
# 		text = requests.get(url,headers=headers,params=params,verify=False,
# 					cookies=cookies).text
# 		msg = re.search(r'\((\{.+?\})\)',text)[1]
# 		msg = json.loads(msg)
# 		return msg
# 	except Exception as e:
# 		print(e)

# def query(phone):
# 	addr= get_address(phone)
# 	tag = get_tag(phone)
# 	t = time.time()
# 	if addr or tag:
# 		return {
# 		'phone':phone,
# 		'status':'success',
# 		'addr':addr,
# 		'tag':tag,
# 		't':t}
# 	else:
# 		return {
# 		'phone' :phone,
# 		'status':'failed',
# 		't':t,}




# for web search mobile --------------------
cookies = cache.pop()
def refresh_cookie():
	"""
		启动一个进程用无头浏览器获取指定数量的cookies
	"""
	global cookies
	cookies = cache.pop()
	if not cookies:
		print('redis 中没有cookie')
		time.sleep(2)
		# print('redis 中没有cookie，程序取cookie，请等待8s')
		# p = Process(target=feed_cookies, args=(10,))
		# p.start()
		# time.sleep(10)
		# cookies = cache.pop()


def get_tag_in_web(phone,retry=3):
	"""
		在搜狗的web页面给号码打标签
	"""
	url = 'https://www.sogou.com/web'
	params = {'query':phone}
	msg = ''
	while retry:
		r = requests.get(url,params,headers=headers,cookies=cookies)

		# cookie 过期，刷新cookie，cookie 有用，存入数据库继续使用
		if ' <form name="authform" method="POST" id="seccodeForm" action="/">' in r.text \
		or 'sogou.com";"snapshot.sogoucdn.com"' in r.text: 
			retry -= 1
			refresh_cookie()
			continue
		cache.put(cookies)

		# 是号码的第1种情况
		try:
			msg = re.search(r'号码通用户数据：(.*?)\)',r.text).group(1).replace(
					"','0','5','",'').replace("：0'",'')
			return msg
		except Exception as e:
			pass

		# 是号码的第2种情况
		try:
			a_list = etree.HTML(r.text).xpath("//div[@class='rb']/h3/a")
			for a in a_list:
				if 'sogou_vr_70030302_title' in a.xpath('./@id')[0]:
					return a.xpath('./text()')[0]
		except Exception as e:
			print(e)

		#未搜到的情况	
		if not msg:
			return '号码不正确，未搜到'

	return '程序错误'


def query(phone):
	"""
		查询入口
	"""
	addr= get_address(phone)
	tag = get_tag_in_web(phone)
	if addr and tag and (tag not in ['号码不正确，未搜到','程序错误']):
		status = 'success'
	else:
		status = 'failed'
	return {
	'source':'搜狗',
	'phone':phone,
	'status':status,
	'addr':addr,
	'tag':tag,
	'timestamp':get_current_timestamp()}


if __name__ == '__main__':
	phone='112'
	j = 1
	while  j:
		print(j);j+=1
		print(query(phone))


