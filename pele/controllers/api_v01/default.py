from builtins import str
import traceback, jwt, uuid
from datetime import datetime, timedelta

from flask import current_app, g, url_for
from flask_restplus import Resource, fields, inputs
from flask_mail import Message

from pele import db, cache, limiter, mail
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
        data['verification_code'] = str(uuid.uuid4())
        user = User(**data)
        db.session.add(user)
        try: db.session.commit()
        except Exception as e:
            current_app.logger.debug(traceback.format_exc())
            return { 'success': False,
                     'message': "Registration failed. Please contact support." }, 500
        msg = Message("Verify your Pele API account", recipients=[user.email])
        msg.body = "Use your verification code below to verify your Pele API " + \
                   "account at {}:\n\n{}".format(url_for('api_v0-1.doc', _external=True),
                                                 data['verification_code'])
        mail.send(msg)
        user_dict = user.to_dict()
        user_dict['success'] = True
        user_dict['message'] = "Verification email sent. Verify before using the API."
        return user_dict, 201


@api.route('/verify', endpoint='verify')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Verification failed" },
         description="Verify registered account.")
class Verify(Resource):
    """Verify."""

    parser = api.parser()
    parser.add_argument('email', required=True, type=inputs.email(),
                        help='email address', location='form')
    parser.add_argument('verification_code', required=True, type=str, 
                        help='verification code', location='form')

    model = api.model('Verify', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
    })

    decorators = [limiter.limit("3/minute")]

    @api.marshal_with(model)
    @api.doc(parser=parser)
    def post(self):
        data = self.parser.parse_args()
        user = User.verify(**data)
        if not user:
            return { 'message': 'Invalid verification code' }, 401
        return { 'success': True,
                 'message': 'Mahalo for verifying. You may now login to receive an API token.' }


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

    decorators = [limiter.limit("3/minute")]

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
        except Exception as e:
            current_app.logger.debug(traceback.format_exc())
            return { 'success': False,
                     'message': "Login failed. Please contact support." }, 500
        return { 'success': True,
                 'token': token.decode('UTF-8') }
