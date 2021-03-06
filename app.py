from flask import Flask, jsonify, request, abort

from config import config
from query.query import query_all
from tools.tool import get_current_timestamp



app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    """ handle 404 error"""
    msg = error.description
    return (jsonify({
        'code': '404',
        'msg': 'not found' if not msg else msg,
        'timestamp': get_current_timestamp(),
    }), 200)


@app.errorhandler(403)  #
def not_allowed(error):
    """handle 403 error"""
    msg = error.description
    return (jsonify({
        'code': '403',
        'msg': 'unauthorized' if not msg else msg,
        'timestamp': get_current_timestamp(),
    }), 200)


@app.errorhandler(500)  
def internal_error(error):
    """handle 500 error"""
    msg = error.description
    return (jsonify({
        'code': '500',
        'msg': 'internal error' if not msg else msg,
        'timestamp': get_current_timestamp(),
    }), 200)


@app.route('/', methods=['GET'])
def index():
    """url for test index"""
    return (jsonify({
        'code': '1',
        'msg': 'success',
        'timestamp': get_current_timestamp(),
    }), 200)


@app.route('/query',methods=['GET', 'POST'])
def query():
    try:
        if request.method == 'GET':
            phone = request.args.get('phone')
        elif request.method == 'POST':
            phone = request.POST.get('phone')
        return (jsonify(query_all(phone)), 200)
    except Exception as e:
        print(e)
        abort(403, 'error in query')



if __name__ == '__main__':
    from gevent import pywsgi,monkey ;monkey.patch_all()
    print('starting server at ',config.PORT,'  ...')
    gevent_server = pywsgi.WSGIServer((config.IP,config.PORT), app)
    gevent_server.serve_forever()

