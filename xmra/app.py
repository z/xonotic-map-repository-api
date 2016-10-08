import falcon
from xmra.resources.MapPackage import MapPackageResource
from xmra.resources.MapPackage import MapPackageCollection
from xmra.middleware import CorsMiddleware


api = falcon.API(middleware=[CorsMiddleware()])
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/maps', MapPackageCollection())
api.add_route('/map/{map_package_id}', MapPackageResource())
