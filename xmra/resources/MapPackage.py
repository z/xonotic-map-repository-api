import json
from xmra.repositories.local.db import session
from xmra.repositories.local.model import MapPackage
from xmra.repositories.local.model import Bsp
from xmra.repositories.local.model import Entity
from xmra.repositories.local.model import Gametype
from xmra.repositories.local.model import BspEntity
from xmra.repositories.local.model import BspGametype
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
                    'gametypes': [],
                    'mapshot': bsp.mapshot,
                    'author': bsp.author
                }
                r_map_package['bsp'].update({bsp.bsp_name: r_bsp})

                q_entites = session.query(BspEntity).filter_by(bsp_id=bsp.bsp_id).join(Entity)

                for e in q_entites:
                    print(e.entity_id)
                    print(e.bsp_id)
                    print(e.entity.name)

                    r_entity = {
                        e.entity.name: e.value
                    }

                    r_bsp['entities'].update(r_entity)

                q_gametype = session.query(BspGametype).filter_by(bsp_id=bsp.bsp_id).join(Gametype)

                for g in q_gametype:
                    print(g.gametype_id)
                    print(g.bsp_id)
                    print(g.gametype.name)

                    r_bsp['gametypes'].append(g.gametype.name)

            map_packages.append(r_map_package)

        print(map_packages)

        resp.body = json.dumps({'data': map_packages}, cls=ObjectEncoder)

    def on_post(self, req, resp):
        pass
