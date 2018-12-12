from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tools.redis_db import cache
from config import config


def feed_cookies(num=config.COOKIES_POOL_SIZE):
	"""存制定量的cookie到redis"""
	chrome_options = Options()
	chrome_options.add_argument("--headless")

	base_url = config.CHROME_BASE_URL
	try:
		driver = webdriver.Chrome(chrome_options=chrome_options)
	except:
		driver = webdriver.Chrome(executable_path=(config.CHROME_DRIVER_PATH), chrome_options=chrome_options)

	for i in range(num):
		driver.get(base_url + "/")
		cookie = driver.get_cookies()
		cookies = dict()
		for i in cookie:
			cookies[i['name']] = i['value']
		cache.put(cookies)
		driver.delete_all_cookies()

	driver.close()
	print('成功存储了{} 个cookie到redis'.format(num))


if __name__ == '__main__':
	get_cookies()
	print(type(cache.get('cookies')))