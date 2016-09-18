import os
import configparser
from xmra.util import check_if_not_create

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

config_file = '.xmra.ini'
home = os.path.expanduser('~')
config_file_with_path = os.path.join(home, config_file)

check_if_not_create(config_file_with_path, 'config/xmra.ini')

config = configparser.ConfigParser()
config.read(config_file_with_path)

conf = config['default']

resources_dir = os.path.expanduser(conf['resources_dir'])

config = {
    'extract_mapshots': conf['extract_mapshots'],
    'extract_radars': conf['extract_radars'],
    'parse_entities': conf['parse_entities'],
    'resources_dir': resources_dir,
    'db': {
        'name': conf['db_name'],
        'user': conf['db_user'],
        'password': conf['db_password'],
        'host': conf['db_host'],
        'port': conf['db_port'],
    },
    'api': {
        'host': conf['api_host'],
        'port': conf['api_port'],
    },
    'output_paths': {
        'packages': resources_dir + 'packages/',
        'mapshots': resources_dir + 'mapshots/',
        'radars': resources_dir + 'radars/',
        'entities': resources_dir + 'entities/',
        'bsp': resources_dir + 'bsp/',
        'data': resources_dir + 'data/',
    }
}

os.makedirs(config['output_paths']['mapshots'], exist_ok=True)
os.makedirs(config['output_paths']['radars'], exist_ok=True)
os.makedirs(config['output_paths']['entities'], exist_ok=True)
os.makedirs(config['output_paths']['bsp'], exist_ok=True)
os.makedirs(config['output_paths']['data'], exist_ok=True)
