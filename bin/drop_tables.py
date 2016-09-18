#!/usr/bin/env python3
from xmra.repositories.local.db import engine
from xmra.repositories.local.db import Base
# from xmra.repositories.local.db import metadata


def main():

    # con = engine.connect()
    # trans = con.begin()
    #
    # con.execute(table.delete())
    # trans.commit()

    for table in Base.metadata.sorted_tables:
        if table in engine.table_names():
            table.drop()

    # metadata.drop_all()
    #
    # for tbl in reversed(metadata.sorted_tables):
    #     print(tbl)
    #     tbl.drop(engine)
    #
    # session.commit()