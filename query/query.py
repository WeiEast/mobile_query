import gevent
from gevent import monkey
monkey.patch_all()

from query.interface import sougou


def query_all(phone):
	tasks = [
		gevent.spawn(sougou.query,phone),#搜狗
	]
	result = gevent.joinall(tasks)
	result = list(map(lambda x:x.value,result))
	return result
	


if __name__ == '__main__':
	print(query_all('112'))