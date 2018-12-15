import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from tools.redis_db import cache
from tools.tool import get_current_timestamp
from config import config



def get_cookies():
	"""存指定量的cookie到redis"""
	chrome_options = Options()
	chrome_options.add_argument("--headless")

	base_url = config.CHROME_BASE_URL
	try:
		driver = webdriver.Chrome(executable_path=(r'/usr/local/bin/chromedriver'),chrome_options=chrome_options)
	except:
		driver = webdriver.Chrome(executable_path=(config.CHROME_DRIVER_PATH), chrome_options=chrome_options)

	print('start .....')
	try:
		while 1:
			num = cache.cookie_count()
			print(get_current_timestamp(),':redis have',num,'cookie ...')
			if num < config.COOKIES_POOL_SIZE:
				driver.get(base_url + "/")
				try:
					time.sleep(1)
					driver.find_element_by_id("query").send_keys("112")
					driver.find_element_by_id('stb').click()
				except:
					# ajx 未加载完成，重新打开页面
					continue
				cookie = driver.get_cookies()
				cookies = dict()
				for i in cookie:
					cookies[i['name']] = i['value']
				cache.put(cookies)
				print('save one cookie')
				driver.delete_all_cookies()
			time.sleep(0.6)
	except Exception as e:
		print(e)
		# 关闭浏览器
		driver.quit()

	


if __name__ == '__main__':
	get_cookies()
