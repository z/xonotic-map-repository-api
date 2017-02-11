#!/bin/bash

set -e

host="$1"
shift
cmd="$@"

until psql -h "$host" -U "xonotic" map_repo -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

find . -name '__pycache__' -exec rm -rf {} +
find . -name '*.py[co]' -exec rm -f {} +

python setup.py clean && python setup.py install

xmra-init

>&2 echo "Postgres is up - executing command ${cmd}"
exec ${cmd}