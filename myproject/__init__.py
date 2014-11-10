from pyramid.config import Configurator
#from views import big_rear
import logging
from views import *

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'myproject')

    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static')
    
    config.add_route('search', '/')
    config.add_view(search, route_name='search')
    
    config.add_route('find', '/find/{server}/{faction}/{recipe}')
    config.add_view(results, route_name='find')
    
    config.add_route('recipes', '/recipes')
    config.add_view(recipes, route_name='recipes', renderer='json')
    
    config.add_route('faq', '/faq')
    config.add_view(faq, route_name='faq')
    

    #mylog = logging.getLogger('waitress')
    #mylog.setLevel(logging.DEBUG)


    return config.make_wsgi_app()
