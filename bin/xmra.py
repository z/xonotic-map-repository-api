#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# Description: Xonotic Map Repository tools help create and manage a map repository.
# Author: Tyler "-z-" Mulligan
# Contact: z@xnz.me

import argparse
import time
import os
import datetime
from xmra.repositories.local.model import Library
from xmra.xonotic.objects import MapPackage
from xmra.config import config
from xmra.repositories.local.db import session
from xmra.helpers.database import get_or_create
from xmra.util import DateTimeEncoder
from xmra.repositories.local import model
from xmra.logger import logger
from sqlalchemy import func


def main():

    start_time = time.monotonic()
    errors = False
    args = parse_args()

    if args.all:

        # Process all the files
        for file in sorted(os.listdir(config['xmra']['packages_dir'])):
            if file.endswith('.pk3'):
                pk3, category, errors = add_map_package(file)

    if args.new:

        file = args.new
        pk3, category, errors = add_map_package(file)

    end_time = time.monotonic()
    logger.debug('Operation took: ' + str(datetime.timedelta(seconds=end_time - start_time)))


def add_map_package(file):

    if file.endswith('.pk3') and os.path.isfile(config['xmra']['packages_dir'] + file):

        logger.debug('Procesing map: {0}'.format(file))

        q = session.query(model.MapPackage).filter_by(pk3_file=file).count()

        if q > 0:
            logger.debug('Map package already in database: {0}'.format(file))
            return False, False, False

        mypk3 = MapPackage(pk3_file=file)
        pk3, category, errors = mypk3.process_package()

        if category != 'maps':
            logger.debug('Not map package: {0}'.format(file))
            return False, False, False

        map_package = model.MapPackage(pk3_file=pk3.pk3_file, shasum=pk3.shasum, filesize=pk3.filesize)

        session.add(map_package)
        session.commit()

        for bsp_name, bsp in pk3.bsp.items():

            new_bsp = model.Bsp(
                map_package_id=map_package.map_package_id,
                bsp_name=bsp.bsp_name,
                bsp_file=bsp.bsp_file,
                map_file=bsp.map_file,
                mapshot=bsp.mapshot,
                radar=bsp.radar,
                title=bsp.title[:255],
                description=bsp.description[:600],
                mapinfo=bsp.mapinfo,
                author=bsp.author,
                waypoints=bool(bsp.waypoints),
                license=bool(bsp.license),
                entities=bsp.entities,
            )

            session.add(new_bsp)
            session.commit()

            map_package.bsp.append(new_bsp)

            if bsp.gametypes:
                for gametype in bsp.gametypes:
                    gametype = get_or_create(session, model.Gametype, name=gametype)
                    bsp_gametype = get_or_create(session, model.BspGametype, bsp_id=new_bsp.bsp_id, gametype_id=gametype.gametype_id)

            if bsp.entities:
                for entity, value in bsp.entities.items():
                    entity = get_or_create(session, model.Entity, name=entity)
                    bsp_entity = get_or_create(session, model.BspEntity, bsp_id=new_bsp.bsp_id, entity_id=entity.entity_id, value=value)

        session.add(map_package)
        session.commit()

        return pk3, category, errors

    else:
        logger.debug('Not found or not pk3.')
        raise SystemExit


def parse_args():

    parser = argparse.ArgumentParser(description='Xonotic Map Repository tools help create and manage a map repository.')

    parser.add_argument('--new', '-n', nargs='?', type=str, help='Add a new package to the database')
    parser.add_argument('--all', '-A', action='store_true',
                        help='Add all maps to the repositories JSON. (overwrites existing maps.json)')

    return parser.parse_args()


if __name__ == "__main__":
    main()

