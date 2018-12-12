import os

from config.config import WORKER, IP, PORT

command = ['nohup gunicorn -w {} -k gevent -b {}:{} app:app --access-logfile log/web_access.log >>log/gunicorn.log 2>>log/gunicorn.err.log &'.format(WORKER,IP,PORT),
		   'nohup python sougou_cookie.py >>log/gunicorn_cookie.log 2>>log/gunicorn.err.log &'
			]

if __name__ == '__main__':
	for cmd in command:
		print(cmd)
		os.system(cmd)