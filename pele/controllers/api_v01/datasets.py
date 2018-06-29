from flask import current_app
from flask_restplus import Resource, fields, inputs

from pele import limiter
from pele.controllers import token_required
from pele.lib.query import QueryES
from pele.controllers.api_v01.config import api, pele_ns
from pele.controllers.api_v01.model import *


@pele_ns.route('/types', endpoint='types')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all type names.")
class Types(Resource):
    """Types."""

    model = api.model('Type', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'types': fields.List(fields.String, description="types"),
        'total': fields.Integer(description="total"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        
        types = QueryES(current_app.config['ES_URL'], current_app.config['ES_INDEX']).query_types()
        return { 'success': True,
                 'total': len(types),
                 'types': types }


@pele_ns.route('/datasets', endpoint='datasets')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset names.")
class Datasets(Resource):
    """Dataset names."""

    model = api.model('Dataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
        'total': fields.Integer(description="total"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        
        datasets = QueryES(current_app.config['ES_URL'], current_app.config['ES_INDEX']).query_datasets()
        return { 'success': True,
                 'total': len(datasets),
                 'datasets': datasets }


@pele_ns.route('/type/<string:type_name>/datasets', endpoint='datasets_by_type')
@pele_ns.param('type_name', 'type name')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset names by type.")
class DatasetsByType(Resource):
    """Dataset names by type."""

    model = api.model('DatasetsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
        'total': fields.Integer(description="total"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name):
        
        datasets = QueryES(current_app.config['ES_URL'], 
                           current_app.config['ES_INDEX']).query_datasets_by_type(type_name)
        return { 'success': True,
                 'total': len(datasets),
                 'datasets': datasets }


@pele_ns.route('/dataset/<string:dataset_name>/types', endpoint='types_by_dataset')
@pele_ns.param('dataset_name', 'dataset name')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all types by dataset name.")
class TypesByDataset(Resource):
    """Types by dataset name."""

    model = api.model('TypesByDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'types': fields.List(fields.String, description="types"),
        'total': fields.Integer(description="total"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_name):
        
        types = QueryES(current_app.config['ES_URL'], 
                        current_app.config['ES_INDEX']).query_types_by_dataset(dataset_name)
        return { 'success': True,
                 'total': len(types),
                 'types': types }


@pele_ns.route('/dataset/<string:dataset_name>/ids', endpoint='ids_by_dataset')
@pele_ns.param('dataset_name', 'dataset name')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset IDs by dataset name.")
class IdsByDataset(Resource):
    """IDs by dataset name."""

    model = api.model('IdsByDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'ids': fields.List(fields.String, description="ids"),
        'total': fields.Integer(description="total"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_name):
        
        ids = QueryES(current_app.config['ES_URL'], 
                      current_app.config['ES_INDEX']).query_ids_by_dataset(dataset_name)
        return { 'success': True,
                 'total': len(ids),
                 'ids': ids }


@pele_ns.route('/type/<string:type_name>/ids', endpoint='ids_by_type')
@pele_ns.param('type_name', 'type name')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset IDs by type name.")
class IdsByType(Resource):
    """IDs by type name."""

    model = api.model('IdsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'ids': fields.List(fields.String, description="ids"),
        'total': fields.Integer(description="total"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name):
        
        ids = QueryES(current_app.config['ES_URL'], 
                      current_app.config['ES_INDEX']).query_ids_by_type(type_name)
        return { 'success': True,
                 'total': len(ids),
                 'ids': ids }


@pele_ns.route('/dataset/<string:id>', endpoint='dataset_by_id')
@pele_ns.param('id', 'dataset ID')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get metadata by dataset ID.")
class MetadataById(Resource):
    """Get metadata by dataset ID."""

    model = api.model('MetadataById', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'result': fields.Nested(METADATA_MODEL, allow_null=True, skip_none=True),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, id):
        
        result = QueryES(current_app.config['ES_URL'], 
                         current_app.config['ES_INDEX']).query_id(id)
        return { 'success': True,
                 'result': result }
