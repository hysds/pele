from builtins import str
from flask import current_app, request
from flask_restx import Resource, fields, inputs

from pele import limiter
from pele.controllers import token_required
from pele.lib.query import get_page_size_and_offset
from pele.controllers.api_v01.config import api, pele_ns
from pele.controllers.api_v01.model import *


# ES_INDEX = app.config["ES_INDEX"]
# es_client = get_es_client()
# es_util = QueryES(es_client, logger=app.logger)


@pele_ns.route('/types', endpoint='types')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all type names.")
class Types(Resource):
    """Types."""
    model = api.model('Type', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'types': fields.List(fields.String, description="types"),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, types = current_app.es_util.query_types(self.index, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(types),
                'page_size': page_size,
                'offset': offset,
                'types': types
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/datasets', endpoint='datasets')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all dataset names.")
class Datasets(Resource):
    """Dataset names."""
    model = api.model('Dataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, datasets = current_app.es_util.query_datasets(self.index, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(datasets),
                'page_size': page_size,
                'offset': offset,
                'datasets': datasets
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/type/<string:type_name>/datasets', endpoint='datasets_by_type')
@pele_ns.param('type_name', 'type name')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all dataset names by type.")
class DatasetsByType(Resource):
    """Dataset names by type."""
    model = api.model('DatasetsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'datasets': fields.List(fields.String, description="datasets"),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, datasets = current_app.es_util.query_datasets_by_type(self.index, type_name, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(datasets),
                'page_size': page_size,
                'offset': offset,
                'datasets': datasets
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/dataset/<string:dataset_name>/types', endpoint='types_by_dataset')
@pele_ns.param('dataset_name', 'dataset name')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
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
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_name):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, types = current_app.es_util.query_types_by_dataset(self.index, dataset_name, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(types),
                'page_size': page_size,
                'offset': offset,
                'types': types
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/dataset/<string:dataset_name>/dataset_ids', endpoint='ids_by_dataset')
@pele_ns.param('dataset_name', 'dataset name')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all dataset IDs by dataset name.")
class IdsByDataset(Resource):
    """IDs by dataset name."""
    model = api.model('IdsByDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'dataset_ids': fields.List(fields.String, description="dataset ids"),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_name):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, ids = current_app.es_util.query_ids_by_dataset(self.index, dataset_name, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(ids),
                'page_size': page_size,
                'offset': offset,
                'dataset_ids': ids
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/type/<string:type_name>/dataset_ids', endpoint='ids_by_type')
@pele_ns.param('type_name', 'type name')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all dataset IDs by type name.")
class IdsByType(Resource):
    """IDs by type name."""
    model = api.model('IdsByType', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'dataset_ids': fields.List(fields.String, description="dataset ids"),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, ids = current_app.es_util.query_ids_by_type(self.index, type_name, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(ids),
                'page_size': page_size,
                'offset': offset,
                'dataset_ids': ids
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/dataset/<string:dataset_id>', endpoint='dataset_by_id')
@pele_ns.param('dataset_id', 'dataset ID')
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get metadata by dataset ID.")
class MetadataById(Resource):
    """Get metadata by dataset ID."""
    model = api.model('MetadataById', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'result': fields.Nested(METADATA_MODEL, allow_null=True, skip_none=True),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_id):
        result = current_app.es_util.query_id(self.index, dataset_id)
        return {
            'success': True,
            'result': result
        }


@pele_ns.route('/type/<string:type_name>/dataset/<string:dataset_name>/<list:ret_fields>',
               endpoint='fields_by_type_and_dataset')
@pele_ns.param('type_name', 'type name')
@pele_ns.param('dataset_name', 'dataset name')
@pele_ns.param('ret_fields', 'comma-separated fields to return')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all dataset results by type name and dataset name.")
class FieldsByTypeDataset(Resource):
    """Results by type name and dataset name."""
    model = api.model('FieldsByTypeDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'results': fields.List(fields.Raw),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name, dataset_name, ret_fields):
        terms = {
            'dataset_type.keyword': type_name,
            'dataset.keyword': dataset_name,
        }
        try:
            index = "{}_*_{}".format(self.index, dataset_name.lower())
            page_size, offset = get_page_size_and_offset(request)
            total, docs = current_app.es_util.query_fields(index, terms, ret_fields, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/overlaps/<string:dataset_id>/<list:ret_fields>', endpoint='overlaps_by_id')
@pele_ns.param('dataset_id', 'dataset ID')
@pele_ns.param('ret_fields', 'comma-separated fields to return')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all dataset results that overlap temporally and spatially with dataset ID.")
class OverlapsById(Resource):
    """Get all dataset results that overlap temporally and spatially with dataset ID."""
    model = api.model('OverlapsById', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'results': fields.List(fields.Raw),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]
    index = current_app.config["ES_INDEX"]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_id, ret_fields):
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, docs = current_app.es_util.overlaps(self.index, dataset_id, {}, ret_fields, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500


@pele_ns.route('/overlaps/<string:dataset_id>/type/<string:type_name>/dataset/<string:dataset_name>/<list:ret_fields>',
               endpoint='overlaps_by_id_type_dataset')
@pele_ns.param('dataset_id', 'dataset ID')
@pele_ns.param('type_name', 'type name')
@pele_ns.param('dataset_name', 'dataset name')
@pele_ns.param('ret_fields', 'comma-separated fields to return')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all results that overlap temporally and spatially with dataset ID of a certain type and "
                     "dataset.")
class OverlapsByIdTypeDataset(Resource):
    """Get all dataset results that overlap temporally and spatially with dataset ID of a certain type and dataset."""
    model = api.model('OverlapsByIdTypeDataset', {
        'success': fields.Boolean(description="success flag"),
        'message': fields.String(description="message"),
        'results': fields.List(fields.Raw),
        'total': fields.Integer(description="total"),
        'count': fields.Integer(description="count"),
        'page_size': fields.Integer(description="page size"),
        'offset': fields.Integer(description="starting offset (0 index)"),
    })

    decorators = [limiter.limit("10/second")]

    # @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_id, type_name, dataset_name, ret_fields):
        terms = {
            'dataset_type.keyword': type_name,
            'dataset.keyword': dataset_name,
        }
        try:
            page_size, offset = get_page_size_and_offset(request)
            total, docs = es_util.overlaps(ES_INDEX, dataset_id, terms, ret_fields, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            return {
                'success': False,
                'message': str(e),
            }, 500
