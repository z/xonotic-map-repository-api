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


class MapPackageCollection:

    def on_get(self, req, resp):
        """Handles GET requests"""
        print(req.params)

        q = session.query(MapPackage).filter(MapPackage.bsp.any())
        map_packages = get_map_json(q)

        resp.body = json.dumps({'data': map_packages}, cls=ObjectEncoder)

    def on_post(self, req, resp):
        pass


class MapPackageResource:

    def on_get(self, req, resp, map_package_id):
        """Handles GET requests"""
        print(req.params)

        q = session.query(MapPackage).filter_by(map_package_id=map_package_id).all()
        map_package = get_map_json(q)

        resp.body = json.dumps({'data': map_package}, cls=ObjectEncoder)

    def on_post(self, req, resp):
        pass


def get_map_json(query):

    map_packages = []

    for map_pack in query:
        r_map_package = {
            'id': map_pack.map_package_id,
            'pk3': map_pack.pk3_file,
            'bsp': {},
            'shasum': map_pack.shasum,
            'filesize': map_pack.filesize,
            'date': map_pack.date,
        }

        for bsp in map_pack.bsp:
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

            for ent in q_entites:
                r_entity = {
                    ent.entity.name: ent.value
                }

                r_bsp['entities'].update(r_entity)

            q_gametype = session.query(BspGametype).filter_by(bsp_id=bsp.bsp_id).join(Gametype)

            for gt in q_gametype:
                r_bsp['gametypes'].append(gt.gametype.name)

        map_packages.append(r_map_package)

    return map_packages