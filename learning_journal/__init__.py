"""Learning journal init."""
import os

from pyramid.config import Configurator


def main(global_config, **settings):
    """Function that returns a Pyramid WSGI application."""
    settings['sqlalchemy.url'] = os.environ['DATABASE_URL']
    # settings['sqlalchemy.url'] = 'postgres://localhost:5432/LearningJournal'
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('.security')
    config.scan()
    return config.make_wsgi_app()
