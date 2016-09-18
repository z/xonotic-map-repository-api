import json
from xmra.repositories.local.db import session
#from xmra.repositories.local.model import MapPackageBsp
from xmra.repositories.local.model import MapPackage
from xmra.repositories.local.model import Bsp
from xmra.repositories.local.model import User
from xmra.repositories.local.model import Keyword
# from xmra.xonotic.objects import MapPackage
from xmra.util import ObjectEncoder
from xmra.util import DateTimeEncoder
from sqlalchemy import func


class MapPackageResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        print(req.params)

        map_packages = []
        #q = session.query(MapPackageBsp).join(MapPackage).join(Bsp).all()
        # q = session.query(MapPackageBsp, MapPackage, Bsp).all()
        # for mp in q:
        #     # print(mp.map_package_id)
        #     r_map_package = {
        #         'id': mp.MapPackage.map_package_id,
        #         'bsp_id': mp.Bsp.bsp_id,
        #         'pk3': mp.MapPackage.pk3_file,
        #         'shasum': mp.MapPackage.shasum,
        #         'filesize': mp.MapPackage.filesize,
        #         'date': str(mp.MapPackage.date),
        #     }
        #     map_packages.append(r_map_package)

        q = session.query(MapPackage).filter(MapPackage.bsp.any())
        for mp in q:
            r_map_package = {
                'id': mp.map_package_id,
                'pk3': mp.pk3_file,
                'bsp': {},
                'shasum': mp.shasum,
            }

            for bsp in mp.bsp:
                r_bsp = {
                    'bsp_file': bsp.bsp_file,
                }
                r_map_package['bsp'].update({bsp.bsp_name: r_bsp})

            map_packages.append(r_map_package)

        print(map_packages)

        resp.body = json.dumps(map_packages, cls=ObjectEncoder)

    def on_post(self, req, resp):
        pass
        # print(req.params)
        # user = User(name='john')
        # keyword1 = Keyword(keyword='cool')
        # keyword2 = Keyword(keyword='alright')
        # keyword3 = Keyword(keyword='yay')
        # user.kw.append(keyword1)
        # user.kw.append(keyword2)
        # user.kw.append(keyword3)
        # session.add(user)
        # session.commit()


class UserResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        print(req.params)

        map_packages = []
        q = session.query(User, Keyword).all()
        for mp in q:
            print(mp)
            r_map_package = {
                'id': mp.User.id,
                'keyword_id': mp.Keyword.id,
                'keyword': mp.Keyword.keyword,
                'user': mp.User.name,
            }
            map_packages.append(r_map_package)

        print(map_packages)

        resp.body = json.dumps(map_packages, cls=ObjectEncoder)

    def on_post(self, req, resp):
        """Handles GET requests"""
        print(req.params)
        user = User(name='john')
        keyword1 = Keyword(keyword='cool')
        keyword2 = Keyword(keyword='alright')
        keyword3 = Keyword(keyword='yay')
        user.kw.append(keyword1)
        user.kw.append(keyword2)
        user.kw.append(keyword3)
        session.add(user)
        session.commit()
