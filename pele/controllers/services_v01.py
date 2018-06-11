import os, sys, json, requests, traceback, jwt
from datetime import datetime, timedelta

from flask import Blueprint, request, Response, current_app, g
from flask_restplus import Api, apidoc, Resource, fields, inputs
from flask_login import login_user, logout_user, login_required

from pele import db, cache
from pele.extensions import auth
from pele.controllers import token_required, authorizations
from pele.models.user import User


services = Blueprint('api_v0-1', __name__, url_prefix='/api/v0.1')
api = Api(services, ui=False, version="0.1", title="Pele REST API",
          description="REST API for HySDS Datasets.",
          authorizations=authorizations)


# default namespace operations


login_parser = api.parser()
login_parser.add_argument('email', required=True, type=inputs.email(),
                          help='email address', location='form')
login_parser.add_argument('password', required=True, type=str, 
                          help='password', location='form')


@api.route('/register', endpoint='register')
@api.doc(responses={ 200: "Success",
                     401: "Unathorized",
                     500: "Register failed" }, description="Register.")
class Register(Resource):
    """Register."""

    @api.doc(parser=login_parser)
    def post(self):
        data = login_parser.parse_args()
        user = User(**data)
        db.session.add(user)
        try: db.session.commit()
        except:
            current_app.logger.debug(traceback.format_exc())
            raise
        return user.to_dict(), 201


@api.route('/login', endpoint='login')
@api.doc(responses={ 200: "Success",
                     401: "Unathorized",
                     500: "Login failed" }, description="Login.")
class Login(Resource):
    """Login."""

    @auth.login_required
    def post(self):
        user = g.user
        if not user:
            return { 'message': 'Invalid credentials', 'authenticated': False }, 401

        try: token = jwt.encode({
            'sub': user.email,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=current_app.config['TOKEN_EXPIRATION_SECS'])},
            current_app.config['SECRET_KEY'])
        except:
            current_app.logger.debug(traceback.format_exc())
            raise
        return { 'token': token.decode('UTF-8') }


# test namespace operations


test_ns = api.namespace('test', description="test operations")


@test_ns.route('/echo', endpoint='echo')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     500: "Echo execution failed" },
         description="Echo.")
class Echo(Resource):
    """Echo."""

    @api.doc(params={ 'echo_str': 'string to echo' }, security='apikey')
    @token_required
    def get(self):
        echo_str = request.args.get('echo_str', None)
        if echo_str is None:
            return {'success': False,
                    'message': "Missing echo_str parameter."}, 400

        return {'success': True,
                'message': "{}".format(echo_str) }
