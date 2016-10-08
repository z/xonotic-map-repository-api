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

resources_dir = os.path.expanduser(config['xmra']['resources_dir'])

# Create all of the resource directories if they do not exist
os.makedirs(config['xmra']['mapshots_dir'], exist_ok=True)
os.makedirs(config['xmra']['radars_dir'], exist_ok=True)
os.makedirs(config['xmra']['entities_dir'], exist_ok=True)
os.makedirs(config['xmra']['bsp_dir'], exist_ok=True)
os.makedirs(config['xmra']['data_dir'], exist_ok=True)
