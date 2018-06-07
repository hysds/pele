import os, sys, json, requests, traceback, jwt
from datetime import datetime, timedelta

from flask import jsonify, Blueprint, request, Response, current_app
from flask_restplus import Api, apidoc, Resource, fields
from flask_login import login_user, logout_user, login_required

from pele import db, cache
from pele.controllers import token_required, authorizations
from pele.models.user import User


NAMESPACE = "pele"

services = Blueprint('api_v0-1', __name__, url_prefix='/api/v0.1')
api = Api(services, ui=False, version="0.1", title="Pele REST API",
          description="REST API for HySDS Datasets.",
          authorizations=authorizations)
ns = api.namespace(NAMESPACE, description="Pele REST operations")


register_parser = api.parser()
register_parser.add_argument('email', type=str, help='email address', location='form')
register_parser.add_argument('password', type=str, help='password', location='form')


@ns.route('/register', endpoint='register')
@api.doc(responses={ 200: "Success",
                     401: "Unathorized",
                     500: "Register failed" }, description="Register.")
class Register(Resource):
    """Register."""

    @api.doc(parser=register_parser)
    def post(self):
        data = register_parser.parse_args()
        print(data)
        user = User(**data)
        print(user)
        db.session.add(user)
        print("Got here")
        try: db.session.commit()
        except: print(traceback.format_exc())
        print("Got there")
        return user.to_dict(), 201


login_parser = api.parser()
login_parser.add_argument('email', type=str, help='email address', location='form')
login_parser.add_argument('password', type=str, help='password', location='form')


@ns.route('/login', endpoint='login')
@api.doc(responses={ 200: "Success",
                     401: "Unathorized",
                     500: "Login failed" }, description="Login.")
class Login(Resource):
    """Login."""

    @api.doc(parser=login_parser)
    def post(self):
        data = login_parser.parse_args()
        print(data)
        user = User.authenticate(**data)
        print(user)

        if not user:
            return jsonify({ 'message': 'Invalid credentials', 'authenticated': False }), 401

        try: token = jwt.encode({
            'sub': user.email,
            'iat':datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=30)},
            current_app.config['SECRET_KEY'])
        except: print(traceback.format_exc())
        print(token)
        return { 'token': token.decode('UTF-8') }


@ns.route('/echo', endpoint='echo')
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
