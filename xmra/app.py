import falcon
from xmra.resources.MapPackage import MapPackageResource
from xmra.middleware import CorsMiddleware


api = falcon.API(middleware=[CorsMiddleware()])
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/maps', MapPackageResource())
