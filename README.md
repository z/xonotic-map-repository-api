# xonotic-map-repository-api
This repository includes the REST API, and data model used by xonotic-map-repository-web

## Setup

```
python3 setup.py install
```

Configuration is available in `~/.xmra.ini` with the default options:

```
[default]
# requires imagemagick
extract_mapshots = True

# requires matplotlib and imagemagick
extract_radars = True

# Requires nothing
parse_entities = True

# Base dir for generated resources
resources_dir = /home/z/dev/xonotic-map-repositry-api/web/resources/

# db settings
db_name = map_repo
db_user = xonotic
db_password = password
db_host = localhost
db_port = 5432
```

Once you configure your database, run `xmra-init` to create the database schema.

You can add maps to the database with: `xmra-add -n mymap.pk3` where 'mymap' exists in the `resources_dir`
in your `~/~.xmra.ini`.

##  Tips

There is a docker folder with a `docker-compose.yml` file. If you prefer to use docker instead of
installing postgres on your host, you can `cd docker` && `docker-compose up`