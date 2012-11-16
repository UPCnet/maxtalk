# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from max.resources import Root, loadMAXSettings
import pymongo


def main(global_config, **settings):
    """ This function returns a WSGI application.
    """
    # App config
    config = Configurator(settings=settings,
                          root_factory=Root)

    # Store in registry
    db_uri = settings['mongodb.url']
    conn = pymongo.Connection(db_uri)
    db = conn[settings['mongodb.db_name']]
    config.registry.max_store = db

    # Set MAX settings
    config.registry.max_settings = loadMAXSettings(settings, config)

    config.add_route('socket.io', '/socket.io/*remaining')

    config.scan('maxtalk', ignore='maxtalk.tests')

    return config.make_wsgi_app()
