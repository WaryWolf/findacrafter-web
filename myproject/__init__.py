from pyramid.config import Configurator
#from views import big_rear

def main(global_config, **settings):
    """ This function returns a WSGI application.
    
    It is usually called by the PasteDeploy framework during 
    ``paster serve``.
    """
    settings = dict(settings)
    settings.setdefault('jinja2.i18n.domain', 'myproject')

    #config = Configurator(root_factory=get_root, settings=settings)
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_chameleon')
    config.add_static_view('deform_static', 'deform:static')
    config.add_static_view('static', 'static')
    
    config.add_route('search', '/')
    config.add_route('find', '/find/{server}/{faction}/{recipe}')
    config.add_route('recipes', '/recipes')
    
    #config.add_route('search2', '/search')
    #config.add_route('results', '/results')

    config.scan('myproject')

    return config.make_wsgi_app()
