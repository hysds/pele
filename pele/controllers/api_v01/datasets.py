from flask import current_app
from flask_restplus import Resource, fields, inputs

from pele import limiter
from pele.controllers import token_required
from pele.lib.query import QueryES
from pele.controllers.api_v01.config import api, pele_ns


@pele_ns.route('/types', endpoint='types')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset types.")
class Types(Resource):
    """Types."""

    model = api.model('Type', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'types': fields.List(fields.String, description="types"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        
        types = QueryES(current_app.config['ES_URL'], current_app.config['ES_INDEX']).query_types()
        return { 'success': True,
                 'types': types }


@pele_ns.route('/datasets', endpoint='datasets')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all datasets/collections.")
class Datasets(Resource):
    """Datasets."""

    model = api.model('Dataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        
        datasets = QueryES(current_app.config['ES_URL'], current_app.config['ES_INDEX']).query_datasets()
        return { 'success': True,
                 'datasets': datasets }


@pele_ns.route('/type/<string:dataset_type>/dataset', endpoint='datasets_by_type')
@pele_ns.param('dataset_type', 'dataset type')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all datasets/collections by dataset type.")
class DatasetsByType(Resource):
    """Datasets/collections by type."""

    model = api.model('DatasetsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_type):
        
        datasets = QueryES(current_app.config['ES_URL'], 
                           current_app.config['ES_INDEX']).query_datasets_by_type(dataset_type)
        return { 'success': True,
                 'datasets': datasets }


@pele_ns.route('/dataset/<string:dataset>/type', endpoint='types_by_dataset')
@pele_ns.param('dataset', 'dataset')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all types by dataset/collection.")
class TypesByDataset(Resource):
    """Types by dataset/collection."""

    model = api.model('TypesByDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'types': fields.List(fields.String, description="types"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset):
        
        types = QueryES(current_app.config['ES_URL'], 
                        current_app.config['ES_INDEX']).query_types_by_dataset(dataset)
        return { 'success': True,
                 'types': types }


@pele_ns.route('/dataset/<string:dataset>/ids', endpoint='ids_by_dataset')
@pele_ns.param('dataset', 'dataset')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset IDs by dataset/collection.")
class IdsByDataset(Resource):
    """IDs by dataset."""

    model = api.model('IdsByDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'ids': fields.List(fields.String, description="ids"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset):
        
        ids = QueryES(current_app.config['ES_URL'], 
                      current_app.config['ES_INDEX']).query_ids_by_dataset(dataset)
        return { 'success': True,
                 'ids': ids }


@pele_ns.route('/type/<string:dataset_type>/ids', endpoint='ids_by_type')
@pele_ns.param('dataset_type', 'dataset type')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all dataset IDs by type.")
class IdsByType(Resource):
    """IDs by type."""

    model = api.model('IdsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'ids': fields.List(fields.String, description="ids"),
    })

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_type):
        
        ids = QueryES(current_app.config['ES_URL'], 
                      current_app.config['ES_INDEX']).query_ids_by_type(dataset_type)
        return { 'success': True,
                 'ids': ids }
