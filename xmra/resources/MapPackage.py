import json
from xmra.repositories.local.db import session
# from xmra.repositories.local.model import MapPackageBsp
from xmra.repositories.local.model import MapPackage
from xmra.repositories.local.model import Bsp
from xmra.repositories.local.model import BspEntity
from xmra.repositories.local.model import Entity
# from xmra.xonotic.objects import MapPackage
from xmra.util import ObjectEncoder
from xmra.util import DateTimeEncoder
from sqlalchemy import func


class MapPackageResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        print(req.params)

        map_packages = []

        q = session.query(MapPackage).filter(MapPackage.bsp.any())
        for mp in q:
            r_map_package = {
                'id': mp.map_package_id,
                'pk3': mp.pk3_file,
                'bsp': {},
                'shasum': mp.shasum,
                'filesize': mp.filesize,
                'date': mp.date,
            }

            for bsp in mp.bsp:
                r_bsp = {
                    'bsp_file': bsp.bsp_file,
                    'title': bsp.title,
                    'license': bsp.license,
                    'map': bsp.map_file,
                    'radar': bsp.radar,
                    'waypoints': bsp.waypoints,
                    'description': bsp.description,
                    'mapinfo': bsp.mapinfo,
                    'entities': {},
                    'mapshot': bsp.mapshot,
                    'author': bsp.author
                }
                r_map_package['bsp'].update({bsp.bsp_name: r_bsp})

                # q_entities = session.query(BspEntity).join(Entity).filter(BspEntity.bsp.has(bsp_id=bsp.bsp_id))
                #
                # for entity in bsp.entities:
                #     r_bsp['entities'].update({entity.name: 0})
                #
                # print(q_entities)

            map_packages.append(r_map_package)

        print(map_packages)

        resp.body = json.dumps(map_packages, cls=ObjectEncoder)

    def on_post(self, req, resp):
        pass


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
