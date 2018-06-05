import os, sys, json, requests, traceback

from flask import jsonify, Blueprint, request, Response, current_app
from flask_restplus import Api, apidoc, Resource, fields
from flask_login import login_user, logout_user, login_required

from pele import cache


NAMESPACE = "pele"

services = Blueprint('api_v0-1', __name__, url_prefix='/api/v0.1')
api = Api(services, ui=False, version="0.1", title="Pele REST API",
          description="REST API for HySDS Datasets.")
ns = api.namespace(NAMESPACE, description="Pele REST operations")


@ns.route('/echo', endpoint='echo')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     500: "Echo execution failed" },
         description="Echo.")
class Echo(Resource):
    """Echo."""

    @api.doc(params={ 'echo_str': 'string to echo' })
    def get(self):
        echo_str = request.args.get('echo_str', None)
        if echo_str is None:
            return {'success': False,
                    'message': "Missing echo_str parameter."}, 400

        return {'success': True,
                'message': "{}".format(echo_str) }
