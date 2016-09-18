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
from xmra.dependency_graph import config
from xmra.repositories.local.db import session
from xmra.helpers.database import get_or_create
from xmra.util import DateTimeEncoder
from xmra.repositories.local import model


def main():

    start_time = time.monotonic()
    errors = False
    args = parse_args()

    if args.all:

        library = Library()

        # Process all the files
        for file in sorted(os.listdir(config['output_paths']['packages'])):
            if file.endswith('.pk3'):
                mypk3 = MapPackage(pk3_file=file)
                pk3, category, errors = mypk3.process_package()

                print(pk3.pk3_file)

                library.add_map_package(pk3=pk3, category=category)

                # if status['errors']:
                #     errors = True

        # Write error.log

        all_maps = library.to_json()

        fo = open(config['output_paths']['data'] + 'maps.json', 'w')
        fo.write(all_maps)
        fo.close()

    if args.new:

        file = args.new

        print(config['output_paths']['packages'])
        print(file)
        print(config['output_paths']['packages'] + file)
        print(os.path.isfile(config['output_paths']['packages'] + file))

        if file.endswith('.pk3') and os.path.isfile(config['output_paths']['packages'] + file):
            mypk3 = MapPackage(pk3_file=file)
            pk3, category, errors = mypk3.process_package()

            map_package = get_or_create(session, model.MapPackage, pk3_file=pk3.pk3_file, shasum=pk3.shasum, filesize=pk3.filesize)

            print(pk3.pk3_file)
            #print(pk3)

            for bsp_name, bsp in pk3.bsp.items():
                #print(bsp)

                new_bsp = get_or_create(session, model.Bsp, bsp_name=bsp.bsp_name, bsp_file=bsp.bsp_file)

                if bsp.gametypes:
                    for gametype in bsp.gametypes:
                        print(gametype)
                        gametype = get_or_create(session, model.Gametype, name=gametype)
                        bsp_gametype = get_or_create(session, model.BspGametype, bsp_id=new_bsp.bsp_id, gametype_id=gametype.gametype_id)

                if bsp.entities:
                    for entity in bsp.entities:
                        print(entity)
                        entity = get_or_create(session, model.Entity, name=entity)
                        bsp_entity = get_or_create(session, model.BspEntity, bsp_id=new_bsp.bsp_id, entity_id=entity.entity_id)

                new_map_package_bsp = get_or_create(session, model.MapPackageBsp, map_package_id=map_package.map_package_id, bsp_id=new_bsp.bsp_id)

            session.commit()

            # if status['errors']:
            #     errors = True

        else:
            print('Not found or not pk3.')
            raise SystemExit

    end_time = time.monotonic()
    print('Operation took: ' + str(datetime.timedelta(seconds=end_time - start_time)))


def parse_args():

    parser = argparse.ArgumentParser(description='Xonotic Map Repository tools help create and manage a map repository.')

    parser.add_argument('--new', '-n', nargs='?', type=str, help='Add a new package to the database')
    parser.add_argument('--all', '-A', action='store_true',
                        help='Add all maps to the repositories JSON. (overwrites existing maps.json)')

    return parser.parse_args()


if __name__ == "__main__":
    main()

