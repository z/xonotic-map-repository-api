# xonotic-map-repository-api
This repository includes the REST API, and data model used by xonotic-map-repository-web

## Setup

```bash
python3 setup.py install
```

Configuration is available in `~/.xmra.ini` with the default options:

```ini
[xmra]
# requires imagemagick
extract_mapshots = True

# requires matplotlib and imagemagick
extract_radars = True

# requires nothing
parse_entities = True

# directories for generated resources
resources_dir = ~/.xonotic/repo_resources
packages_dir = %(resources_dir)s/packages/
mapshots_dir = %(resources_dir)s/mapshots/
radars_dir = %(resources_dir)s/radars/
entities_dir = %(resources_dir)s/entities/
bsp_dir = %(resources_dir)s/bsp/
data_dir = %(resources_dir)s/data/

# db settings
db_name = map_repo
db_user = xonotic
db_password = password
db_host = localhost
db_port = 5432

# api settings
api_host = localhost
api_port = 8010

# for CORS
web_host = localhost
web_port = 80

# Logging configuration
[loggers]
keys = root, sqlalchemy, gunicorn.error, gunicorn.access

[logger_root]
level    = DEBUG
handlers = console, error_file

[logger_sqlalchemy]
# INFO logs SQL queries, DEBUG logs queries and results, and WARN logs neither
level = INFO
handlers = console, error_file
qualname = sqlalchemy.engine

[logger_gunicorn.error]
level = INFO
handlers = error_file
propagate = 1
qualname = gunicorn.error

[logger_gunicorn.access]
level = INFO
handlers = access_file
propagate = 0
qualname = gunicorn.access

[handlers]
keys = console, error_file, access_file

[handler_console]
class = StreamHandler
args = (sys.stdout,)
level = NOTSET
formatter = generic

[handler_error_file]
class = logging.handlers.RotatingFileHandler
formatter = generic
args = ('xmr.log', 'a', 50000000, 5)

[handler_access_file]
class = logging.FileHandler
formatter = access
args = ('/tmp/gunicorn.access.log',)

[formatters]
keys = generic, access

[formatter_generic]
format = %(asctime)s %(levelname)-5.5s [%(name)s] [%(threadName)s] %(message)s
datefmt = %Y-%m-%d %H:%M:%S
class = logging.Formatter

[formatter_access]
format = %(message)s
class = logging.Formatter
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