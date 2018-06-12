from flask import request, current_app, g
from flask_restplus import Resource, fields, inputs

from pele import limiter
from pele.controllers import token_required
from pele.controllers.api_v01.config import api, test_ns


@test_ns.route('/echo', endpoint='echo')
@api.doc(responses={ 200: "Success",
                     400: "Invalid parameters",
                     401: "Unathorized",
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

    decorators = [limiter.limit("1/second")]

    @token_required
    @api.marshal_with(model)
    @api.doc(parser=parser, security='apikey')
    def get(self):
        echo_str = request.args.get('echo_str', None)
        if echo_str is None:
            return {'success': False,
                    'message': "Missing echo_str parameter."}, 400

        return { 'success': True,
                 'message': "{}".format(echo_str) }
