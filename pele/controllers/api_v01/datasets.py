from flask import current_app
from flask_restplus import Resource, fields, inputs

from pele.controllers import token_required
from pele.lib.query import QueryES
from pele.controllers.api_v01.config import api, pele_ns


@pele_ns.route('/types', endpoint='types')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all types.")
class Types(Resource):
    """Types."""

    model = api.model('Type', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'types': fields.List(fields.String, description="types"),
    })

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
         description="Get all datasets.")
class Datasets(Resource):
    """Datasets."""

    model = api.model('Dataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
    })

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
         description="Get all datasets by type.")
class DatasetsByType(Resource):
    """Datasets by type."""

    model = api.model('DatasetsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
    })

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_type):
        
        datasets = QueryES(current_app.config['ES_URL'], 
                           current_app.config['ES_INDEX']).query_datasets_by_type(dataset_type)
        return { 'success': True,
                 'datasets': datasets }


@pele_ns.route('/dataset/<string:dataset>/granules', endpoint='granules_by_dataset')
@pele_ns.param('dataset', 'dataset')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
                     500: "Execution failed" },
         description="Get all granules by dataset.")
class GranulesByDataset(Resource):
    """Granules by dataset."""

    model = api.model('GranulesByDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'granules': fields.List(fields.String, description="granules"),
    })

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset):
        
        granules = QueryES(current_app.config['ES_URL'], 
                           current_app.config['ES_INDEX']).query_granules_by_dataset(dataset)
        return { 'success': True,
                 'granules': granules }
