from builtins import str

import traceback
from flask import current_app, request
from flask_restx import Resource, fields

from pele import limiter
from pele.controllers import token_required
from pele.lib.query import get_page_size_and_offset, parse_polygon
from pele.controllers.api_v01.config import api, pele_ns
from pele.controllers.api_v01.model import METADATA_MODEL


@pele_ns.route('/types', endpoint='types')
@pele_ns.param('offset', 'offset', type=int)
@pele_ns.param('page_size', 'page size', type=int)
@api.doc(responses={200: "Success",
                    400: "Invalid parameters",
                    401: "Unathorized",
                    500: "Execution failed"},
         description="Get all type names.")
class Types(Resource):
    """GRQ dataset types."""

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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, types = current_app.es_util.query_types(index, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(types),
                'page_size': page_size,
                'offset': offset,
                'types': types
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self):
        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, datasets = current_app.es_util.query_datasets(index, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(datasets),
                'page_size': page_size,
                'offset': offset,
                'datasets': datasets
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name):
        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, datasets = current_app.es_util.query_datasets_by_type(index, type_name, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(datasets),
                'page_size': page_size,
                'offset': offset,
                'datasets': datasets
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_name):
        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, types = current_app.es_util.query_types_by_dataset(index, dataset_name, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(types),
                'page_size': page_size,
                'offset': offset,
                'types': types
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    arg_parser = pele_ns.parser()
    arg_parser.add_argument('start_time', type=str, help="GTE to start_time field", required=False)
    arg_parser.add_argument('end_time', type=str, help="Less than to end_time field", required=False)
    arg_parser.add_argument('polygon', type=str, help="Bounding geo-polygon", required=False)

    json_parser = pele_ns.parser()
    json_parser.add_argument('start_time', location='json', help="GTE to start_time field", required=False)
    json_parser.add_argument('end_time', location='json', help="Less than to end_time field", required=False)
    json_parser.add_argument('polygon', location='json', type=list, help="Bounding geo-polygon", required=False)

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

    @token_required
    @pele_ns.expect(arg_parser)
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_name):
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        polygon = request.args.get('polygon', None)

        if polygon is not None:
            try:
                polygon = parse_polygon(polygon)
            except Exception as e:
                return {
                    'success': False,
                    'message': str(e)
                }, 400

        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, ids = current_app.es_util.query_ids_by_dataset(index, dataset_name, offset, page_size,
                                                                  start_time=start_time, end_time=end_time,
                                                                  polygon=polygon)
            return {
                'success': True,
                'total': total,
                'count': len(ids),
                'page_size': page_size,
                'offset': offset,
                'dataset_ids': ids
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {
                'success': False,
                'message': str(e),
            }, 500

    @token_required
    @pele_ns.expect(json_parser)
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def post(self, dataset_name):
        request_json = request.get_json()
        start_time = request_json.get('start_time', None)
        end_time = request_json.get('end_time', None)
        polygon = request_json.get('polygon', None)

        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, ids = current_app.es_util.query_ids_by_dataset(index, dataset_name, offset, page_size,
                                                                  start_time=start_time, end_time=end_time,
                                                                  polygon=polygon)
            return {
                'success': True,
                'total': total,
                'count': len(ids),
                'page_size': page_size,
                'offset': offset,
                'dataset_ids': ids
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    arg_parser = pele_ns.parser()
    arg_parser.add_argument('start_time', type=str, help="GTE to start_time field", required=False)
    arg_parser.add_argument('end_time', type=str, help="Less than to end_time field", required=False)
    arg_parser.add_argument('polygon', type=str, help="Bounding geo-polygon", required=False)

    json_parser = pele_ns.parser()
    json_parser.add_argument('start_time', location='json', help="GTE to start_time field", required=False)
    json_parser.add_argument('end_time', location='json', help="Less than to end_time field", required=False)
    json_parser.add_argument('polygon', location='json', type=list, help="Bounding geo-polygon", required=False)

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

    @token_required
    @pele_ns.expect(arg_parser)
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name):
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        polygon = request.args.get('polygon', None)

        if polygon is not None:
            try:
                polygon = parse_polygon(polygon)
            except Exception as e:
                return {
                    'success': False,
                    'message': str(e)
                }, 400

        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, ids = current_app.es_util.query_ids_by_type(index, type_name, offset, page_size,
                                                               start_time=start_time, end_time=end_time,
                                                               polygon=polygon)
            return {
                'success': True,
                'total': total,
                'count': len(ids),
                'page_size': page_size,
                'offset': offset,
                'dataset_ids': ids
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {
                'success': False,
                'message': str(e),
            }, 500

    @token_required
    @pele_ns.expect(json_parser)
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def post(self, type_name):
        request_json = request.get_json()
        start_time = request_json.get('start_time', None)
        end_time = request_json.get('end_time', None)
        polygon = request_json.get('polygon', None)

        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, ids = current_app.es_util.query_ids_by_type(index, type_name, offset, page_size,
                                                               start_time=start_time, end_time=end_time,
                                                               polygon=polygon)
            return {
                'success': True,
                'total': total,
                'count': len(ids),
                'page_size': page_size,
                'offset': offset,
                'dataset_ids': ids
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_id):
        index = current_app.config["ES_INDEX"]
        result = current_app.es_util.query_id(index, dataset_id)
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

    arg_parser = pele_ns.parser()
    arg_parser.add_argument('start_time', type=str, help="GTE to start_time field", required=False)
    arg_parser.add_argument('end_time', type=str, help="Less than to end_time field", required=False)
    arg_parser.add_argument('polygon', type=str, help="Bounding geo-polygon", required=False)

    json_parser = pele_ns.parser()
    json_parser.add_argument('start_time', location='json', help="GTE to start_time field", required=False)
    json_parser.add_argument('end_time', location='json', help="Less than to end_time field", required=False)
    json_parser.add_argument('polygon', location='json', type=list, help="Bounding geo-polygon", required=False)

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

    @token_required
    @pele_ns.expect(arg_parser)
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, type_name, dataset_name, ret_fields):
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        polygon = request.args.get('polygon', None)

        if polygon is not None:
            try:
                polygon = parse_polygon(polygon)
            except Exception as e:
                return {
                    'success': False,
                    'message': str(e)
                }, 400

        terms = {
            'dataset_type.keyword': type_name,
            'dataset.keyword': dataset_name,
        }
        try:
            index = current_app.config["ES_INDEX"]
            index = "{}_*_{}".format(index, dataset_name.lower())
            page_size, offset = get_page_size_and_offset(request)
            total, docs = current_app.es_util.query_fields(index, terms, ret_fields, offset, page_size,
                                                           start_time=start_time, end_time=end_time,
                                                           polygon=polygon)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {
                'success': False,
                'message': str(e),
            }, 500

    @token_required
    @pele_ns.expect(json_parser)
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def post(self, type_name, dataset_name, ret_fields):
        start_time = request.args.get('start_time', None)
        end_time = request.args.get('end_time', None)
        polygon = request.args.get('polygon', None)

        terms = {
            'dataset_type.keyword': type_name,
            'dataset.keyword': dataset_name,
        }
        try:
            index = current_app.config["ES_INDEX"]
            index = "{}_*_{}".format(index, dataset_name.lower())
            page_size, offset = get_page_size_and_offset(request)
            total, docs = current_app.es_util.query_fields(index, terms, ret_fields, offset, page_size,
                                                           start_time=start_time, end_time=end_time,
                                                           polygon=polygon)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_id, ret_fields):
        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, docs = current_app.es_util.overlaps(index, dataset_id, {}, ret_fields, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
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

    @token_required
    @api.marshal_with(model)
    @api.doc(security='apikey')
    def get(self, dataset_id, type_name, dataset_name, ret_fields):
        terms = {
            'dataset_type.keyword': type_name,
            'dataset.keyword': dataset_name,
        }
        try:
            index = current_app.config["ES_INDEX"]
            page_size, offset = get_page_size_and_offset(request)
            total, docs = current_app.es_util.overlaps(index, dataset_id, terms, ret_fields, offset, page_size)
            return {
                'success': True,
                'total': total,
                'count': len(docs),
                'page_size': page_size,
                'offset': offset,
                'results': docs
            }
        except Exception as e:
            current_app.logger.error(traceback.format_exc())
            return {
                'success': False,
                'message': str(e),
            }, 500
