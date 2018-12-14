import time
import gevent
import requests
requests.packages.urllib3.disable_warnings()

from config import config


def get_current_timestamp():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
 

def download(url,method='get',data={},params={},headers={},cookies={},proxies={},verify=False,retry=config.RETRY,timeout=config.TIMEOUT):
    """
    Download func ,return a responde obj
    """
    while retry:
        try:
            with gevent.Timeout(timeout):
                if method == 'post':
                    r = requests.post(url,data=data,headers=headers,cookies=cookies,proxies=proxies,verify=verify)
                else:
                    r = requests.get(url,params=params,headers=headers,cookies=cookies,proxies=proxies,verify=verify)
                if r.status_code != 200:
                    pass
            return r
        except Exception as e:
            print(e)
            retry -= 1
