import traceback, jwt
from datetime import datetime, timedelta

from flask import current_app, g
from flask_restplus import Resource, fields, inputs

from pele import db, cache, limiter
from pele.extensions import auth
from pele.models.user import User
from pele.controllers.api_v01.config import api



@api.route('/register', endpoint='register')
@api.doc(responses={ 201: "Success",
                     400: "Invalid parameters",
                     500: "Registration failed" },
         description="User registration.")
class Register(Resource):
    """Register."""

    parser = api.parser()
    parser.add_argument('email', required=True, type=inputs.email(),
                        help='email address', location='form')
    parser.add_argument('password', required=True, type=str, 
                        help='password', location='form')

    decorators = [limiter.limit("1/minute")]

    model = api.model('Register', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'email': fields.String(description="email"),
        'id': fields.Integer(description="id"),
    })

    @api.marshal_with(model)
    @api.doc(parser=parser)
    def post(self):
        data = self.parser.parse_args()
        user = User(**data)
        db.session.add(user)
        try: db.session.commit()
        except Exception, e:
            current_app.logger.debug(traceback.format_exc())
            return { 'success': False,
                     'message': "Registration failed. Please contact support." }, 500
        user_dict = user.to_dict()
        user_dict['success'] = True
        return user_dict, 201


@api.route('/login', endpoint='login')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Login failed" },
         description="Login and receive API token.")
class Login(Resource):
    """Login."""

    model = api.model('Login', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'token': fields.String(description="API token"),
    })

    decorators = [limiter.limit("1/minute")]

    @auth.login_required
    @api.marshal_with(model)
    def post(self):
        user = g.user
        if not user:
            return { 'message': 'Invalid credentials' }, 401

        try: token = jwt.encode({
            'sub': user.email,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=current_app.config['TOKEN_EXPIRATION_SECS'])},
            current_app.config['SECRET_KEY'])
        except Exception, e:
            current_app.logger.debug(traceback.format_exc())
            return { 'success': False,
                     'message': "Login failed. Please contact support." }, 500
        return { 'success': True,
                 'token': token.decode('UTF-8') }
