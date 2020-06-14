from builtins import object
import os, logging

from flask import Flask
from flask_restx import apidoc
from webassets.loaders import PythonLoader as PythonAssetsLoader
from werkzeug.routing import BaseConverter

from pele import assets
from pele.extensions import (cache, assets_env, debug_toolbar, login_manager, cors, bcrypt, db, limiter, mail)

# TODO: fix es_connection function
from pele.lib.es_connection import get_es_client
from pele.lib.query import QueryES


class ListConverter(BaseConverter):
    regex = r'.+(?:,.+)*,?'

    def to_python(self, value):
        return [i.strip() for i in value.split(',')]

    def to_url(self, values):
        return ','.join(super(ListConverter, self).to_url(value) for value in values)
    

class ReverseProxied(object):
    """Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
        location /myprefix {
            proxy_pass http://127.0.0.1:8888;
            proxy_set_header Host $host;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Scheme $scheme;
            proxy_set_header X-Script-Name /myprefix;
        }

    In apache:
        ProxyRequests Off
        ProxyPass /myprefix/ http://127.0.0.1:8888/
        ProxyPassReverse /myprefix/ http://127.0.0.1:8888/
        ProxyPass /myprefix http://127.0.0.1:8888
        ProxyPassReverse /myprefix http://127.0.0.1:8888
        <Location /myprefix>
            Header add "X-Script-Name" "/myprefix"
            RequestHeader set "X-Script-Name" "/myprefix"
            Header add "Host" "fqdn.domain.com"
            RequestHeader set "Host" "fqdn.domain.com"
            Header add "X-Scheme" "https"
            RequestHeader set "X-Scheme" "https"
        </Location>

    :param app: the WSGI application
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        x_forwarded_host = environ.get('HTTP_X_FORWARDED_HOST', '')
        if x_forwarded_host:
            environ['HTTP_HOST'] = x_forwarded_host
        return self.app(environ, start_response)


def create_app(object_name):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. pele.settings.ProductionConfig
    """

    app = Flask(__name__)
    app.config.from_object(object_name)
    app.config.from_pyfile('../settings.cfg')  # override

    # register converters
    app.url_map.converters['list'] = ListConverter

    # set debug logging level
    if app.config.get('DEBUG', False):
        app.logger.setLevel(logging.DEBUG)

    cors.init_app(app)
    app.wsgi_app = ReverseProxied(app.wsgi_app)

    app.es_client = get_es_client(app.config)  # TODO: maybe move the es connection here
    app.es_util = QueryES(app.es_client, logger=app.logger)

    # init extensions
    cache.init_app(app)
    debug_toolbar.init_app(app)
    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)
    mail.init_app(app)

    # Import and register the different asset bundles
    assets_env.init_app(app)
    assets_loader = PythonAssetsLoader(assets)
    for name, bundle in list(assets_loader.load_bundles().items()):
        assets_env.register(name, bundle)

    # register our blueprints
    from .controllers.main import main
    app.register_blueprint(main)

    from .controllers.api_v01 import services as api_v01
    app.register_blueprint(api_v01)
    app.register_blueprint(apidoc.apidoc)

    return app


if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var FLASK_ENV
    env = os.environ.get('FLASK_ENV', 'production')
    app = create_app('pele.settings.%sConfig' % env.capitalize())

    app.run()
