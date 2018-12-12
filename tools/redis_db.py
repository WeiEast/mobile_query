import redis
import pickle

from config import config


class Cache(object):
    r = redis.StrictRedis(connection_pool=redis.ConnectionPool.from_url(config.REDIS_URL))
    p = r.pipeline(transaction=False)

    def get(self, name):
        ext = self.r.get(name)
        return pickle.loads(ext) if ext else None

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return self.r.set(name, pickle.dumps(value), ex, px, nx, xx)

    def delete(self, names):
        return self.r.delete(names)

    def put(self,value):
        if not isinstance(value,dict):
            return
        return self.r.sadd(config.REDIS_SET_NAME,pickle.dumps(value))

    def pop(self):
        ext = self.r.spop(config.REDIS_SET_NAME)
        return pickle.loads(ext) if ext else None

    def cookie_count(self):
        return self.r.scard(config.REDIS_SET_NAME)


cache = Cache() 

