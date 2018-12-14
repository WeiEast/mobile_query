import os 
# redis db
REDIS_URL = os.environ.get('REDIS_URL') or 'http://redis:6379/1'
REDIS_SET_NAME = 'cookiejars'
COOKIES_POOL_SIZE = 10
# 查询结果缓存时间
RESULT_EXPIRE = 24*60*60

# for selenium
CHROME_DRIVER_PATH = '/Users/apple/phantomjs-2.1.1-macosx/bin/chromedriver'
CHROME_BASE_URL = "https://www.sogou.com/"

# for server
IP = '0.0.0.0'
PORT = 6789
WORKER = 4

# download
TIMEOUT = 10
RETRY = 3
