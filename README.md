# xonotic-map-repository-api
This repository includes the REST API, and data model used by xonotic-map-repository-web

## Setup

```bash
python3 setup.py install
```

Configuration is available in `~/.xmra.ini` with the default options:

```ini
[default]
# requires imagemagick
extract_mapshots = True

# requires matplotlib and imagemagick
extract_radars = True

# Requires nothing
parse_entities = True

# Base dir for generated resources
resources_dir = ~/.xonotic/repo_resources/

# db settings
db_name = map_repo
db_user = xonotic
db_password = password
db_host = localhost
db_port = 5432

# api settings 
api_host = localhost
api_port = 8010
```

Once you configure your database, run `xmra-init` to create the database schema.

## Add Maps

You can add maps to the database with: `xmra-add -n mymap.pk3` where `mymap.pk3` exists in the `packages` sub-directory of the `resources_dir` in your `~/~.xmra.ini`, e.g. `~/.xonotic/repo_resources/packages/`

## Start the API

`xmra-serve` uses gunicorn to serve the repository as a wsgi application.

##  Tips

There is a docker folder with a `docker-compose.yml` file. If you prefer to use docker instead of
installing postgres on your host, you can `cd docker` && `docker-compose up`

## License

Licensed under MIT