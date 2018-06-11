from flask import Blueprint
from flask_restplus import Api

from pele.controllers import authorizations


services = Blueprint('api_v0-1', __name__, url_prefix='/api/v0.1')
api = Api(services, ui=False, version="0.1", title="Pele REST API",
          description="REST API for HySDS Datasets.",
          authorizations=authorizations)


# namespaces
test_ns = api.namespace('test', description="test operations")
pele_ns = api.namespace('pele', description="pele operations")
