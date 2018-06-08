from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_caching import Cache
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager
from flask_assets import Environment
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth


# setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()

# setup debug toolbar
debug_toolbar = DebugToolbarExtension()

# setup login manager
login_manager = LoginManager()
login_manager.login_view = "main.login"

# setup bcrypt
bcrypt = Bcrypt()

# setup cors
cors = CORS()

# setup sqlalchemy
db = SQLAlchemy()

# setup http basic auth
auth = HTTPBasicAuth()
