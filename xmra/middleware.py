ALLOWED_ORIGINS = ['http://localhost:8080']


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
