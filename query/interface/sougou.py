import re
import time
from lxml import etree

from tools.redis_db import cache
from tools.tool import get_current_timestamp, download
from config import config



NAME = 'sougou'
HEADERS = {
"Host":"www.sogou.com",
"Connection":"keep-alive",
"User-Agent":("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) App"
	"leWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"),
"Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
}
COOKIES = cache.pop()



def get_address(phone):
	"""
		获取手机号归属地
	"""
	url = 'https://www.sogou.com/websearch/phoneAddress.jsp'
	params = {
	'phoneNumber':phone,
	'cd':'handlenumber',
	'isSogoDomain':'0'
	}
	try:
		text = download(url,headers=HEADERS,params=params).text
		msg = re.search('"(.*?)"',text)[1]
		return msg
	except Exception as e:
		return '全国'


def refresh_cookie():
	"""
		从redis获取可用的cookies
	"""
	global COOKIES
	COOKIES = cache.pop()
	if not COOKIES:
		print('redis 中没有cookie')
		time.sleep(2)


def get_tag_in_web(phone,retry=3):
	"""
		在搜狗的web页面给号码打标签
	"""

	url = 'https://www.sogou.com/web'
	params = {'query':phone}
	msg = ''
	while retry:
		r = download(url,params=params,headers=HEADERS,cookies=COOKIES)

		# 下载超时
		if not r:
			continue

		# cookie 过期，刷新cookie，cookie 有用，存入数据库继续使用
		if ' <form name="authform" method="POST" id="seccodeForm" action="/">' in r.text \
		or 'sogou.com";"snapshot.sogoucdn.com"' in r.text: 
			retry -= 1
			refresh_cookie()
			if not retry:
				return '无可用cookie'
			continue

		cache.put(COOKIES)

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
			return '未搜到'

	return '程序错误'


def query(phone):
	"""
		查询入口
	"""
	# 先从缓存读取数据，缓存没有再查询
	cache_key = NAME + phone
	res = cache.get(cache_key)
	if res:
		return res

	# 查询归属地 和 号码标签
	addr= get_address(phone)
	tag = get_tag_in_web(phone)

	# 组织查询结果
	if addr and tag and (tag not in ['程序错误','无可用cookie']):
		status = 'success'
	else:
		status = 'failed'
	res = {
	'source':NAME,
	'phone':phone,
	'status':status,
	'addr':addr,
	'tag':tag,
	'timestamp':get_current_timestamp()}

	# 如果查询成功，缓存数据
	if  status == 'success':
		cache.set(cache_key,res,config.RESULT_EXPIRE)

	# 返回查询结果
	return res


if __name__ == '__main__':
	phone='112'
	j = 1
	while  j:
		print(j);j+=1
		print(query(phone))


