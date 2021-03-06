from builtins import str
from functools import wraps
import traceback
import jwt

from flask import request, current_app

from pele import login_manager
from pele.models.user import User


authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY',
    }
}


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        if current_app.config.get('AUTH', False) is False:
            return f(*args, **kwargs)

        invalid_msg = {
            'message': 'Invalid token. Registeration and/or authentication required',
            'success': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'success': False
        }

        token = request.headers.get('X-API-KEY', None)
        current_app.logger.debug("token: {}".format(token))
        if token is None:
            return invalid_msg, 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_app.logger.debug("data: {}".format(data))
            user = User.query.filter_by(email=data['sub']).first()
            if not user:
                return {
                    'message': 'User not found',
                    'success': False
                }, 401
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            current_app.logger.debug("jwt.ExpiredSignatureError: {}".format(traceback.format_exc()))
            return expired_msg, 401
        except jwt.InvalidTokenError:
            current_app.logger.debug("jwt.InvalidTokenError: {}".format(traceback.format_exc()))
            return invalid_msg, 401
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {
                'message': "Unknown error: {}".format(str(e)),
                'success': False
            }, 401

    return _verify


@login_manager.user_loader
def load_user(username):
    return User.query.get(username)
