import os, sys, json, requests, traceback, jwt
from datetime import datetime, timedelta

from flask import Blueprint, request, Response, current_app, g
from flask_restplus import Api, apidoc, Resource, fields, inputs
from flask_login import login_user, logout_user, login_required

from pele import db, cache
from pele.extensions import auth
from pele.controllers import token_required, authorizations
from pele.models.user import User
from pele.lib.query import QueryES


services = Blueprint('api_v0-1', __name__, url_prefix='/api/v0.1')
api = Api(services, ui=False, version="0.1", title="Pele REST API",
          description="REST API for HySDS Datasets.",
          authorizations=authorizations)


# default namespace operations


@api.route('/register', endpoint='register')
@api.doc(responses={ 200: "Success",
                     401: "Unathorized",
                     500: "Register failed" }, description="Register.")
class Register(Resource):
    """Register."""

    parser = api.parser()
    parser.add_argument('email', required=True, type=inputs.email(),
                        help='email address', location='form')
    parser.add_argument('password', required=True, type=str, 
                        help='password', location='form')


    model = api.model('Register', {
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

    model = api.model('Login', {
        'token': fields.String(description="API token"),
    })

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

    parser = api.parser()
    parser.add_argument('echo_str', required=True, type=str,
                        help='string to echo')

    model = api.model('Echo', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="echo output"),
    })

    @api.marshal_with(model)
    @api.doc(parser=parser, security='apikey')
    @token_required
    def get(self):
        echo_str = request.args.get('echo_str', None)
        if echo_str is None:
            return {'success': False,
                    'message': "Missing echo_str parameter."}, 400

        return { 'success': True,
                 'message': "{}".format(echo_str) }


# pele namespace operations


pele_ns = api.namespace('pele', description="pele operations")


@pele_ns.route('/datasets', endpoint='datasets')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     500: "Execution failed" },
         description="Get all dataset types.")
class Datasets(Resource):
    """Datasets."""

    model = api.model('Dataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
    })

    @api.marshal_with(model)
    @api.doc(security='apikey')
    @token_required
    def get(self):
        
        datasets = QueryES(current_app.config['ES_URL'], current_app.config['ES_INDEX']).query_datasets()
        return { 'success': True,
                 'datasets': datasets }
