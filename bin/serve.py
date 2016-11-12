from __future__ import unicode_literals

import multiprocessing
import logging
import gunicorn.app.base
from gunicorn.six import iteritems
from xmra import app
from xmra.config import config, config_file_with_path


log = logging.getLogger(__name__)


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

options = {
    'bind': '%s:%s' % (config['xmra']['api_host'], config['xmra']['api_port']),
    'reload': True,
    'logger_class': "simple",
    'logconfig': config_file_with_path,
}

log.info("Starting up the API")

StandaloneApplication(app.api, options).run()
