import requests

headers= {
"Host":"www.sogou.com",
"Connection":"keep-alive",
"User-Agent":("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) App"
	"leWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"),
"Accept":"*/*",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7",
}

cookies = {'pgv_pvi': '3020272640', 'ld': 'ZZllllllll2t9MlGlllllVZFclZllllltlISgkllll9lllllRklll5@@@@@@@@@@', 'taspeed': 'taspeedexist', 'SNUID': 'CBC49FE49490E96BD1E217D19578E7A1', 'SUIR': '1544806410', 'browerV': '3', 'PHPSESSID': '51amudehacku39s5ur6f55cof0', 'sst0': '289', 'sct': '1', 'pgv_si': 's4597914624', 'ABTEST': '3|1544806408|v17', 'SUV': '1544806408850026', 'IPLOC': 'CN3301', 'osV': '2', 'SUID': '5E510A703118960A000000005C13E008'}
url = 'https://www.sogou.com/web?query=110'

print(requests.get(url,cookies=cookies,headers=headers,verify=False).text)