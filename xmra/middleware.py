from xmra.config import config
from xmra.logger import logger

web_address = 'http://{0}'.format(config['xmra']['web_host'])
if config['xmra']['web_port'] != '80':
    web_address += ':{0}'.format(config['xmra']['web_port'])
# if config['web']['host'] is '*':
#     web_address = '*'

ALLOWED_ORIGINS = [web_address]

logger.debug(ALLOWED_ORIGINS)


class CorsMiddleware(object):

    def process_request(self, request, response):
        origin = request.get_header('Origin')
        if origin in ALLOWED_ORIGINS:
            response.set_header('Access-Control-Allow-Origin', origin)
            response.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT')
            response.set_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With')


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    with open('index.html') as f:
        return [f]
