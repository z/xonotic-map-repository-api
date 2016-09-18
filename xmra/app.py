import falcon
from xmra.resources.MapPackage import MapPackageResource
from xmra.resources.MapPackage import UserResource
from xmra.middleware import CorsMiddleware


api = falcon.API(middleware=[CorsMiddleware()])
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/maps', MapPackageResource())
api.add_route('/user', UserResource())
