from flask_restx import fields

from pele.controllers.api_v01.config import api


CENTER_MODEL = api.model('Center', { 
    'type': fields.String, 
    'coordinates': fields.List(fields.Float), 
}) 
 
LOCATION_MODEL = api.model('Location', { 
    'type': fields.String, 
    'coordinates': fields.Raw,
}) 
 
IMAGE_MODEL = api.model('Image', { 
    'small_img': fields.String, 
    'tooltip': fields.String, 
    'img': fields.String, 
}) 
 
METADATA_MODEL = api.model('Metadata', { 
    'browse_urls': fields.List(fields.String(description='browse url')), 
    'urls': fields.List(fields.String(description='url')), 
    'version': fields.String, 
    'objectid': fields.String, 
    'continent': fields.String, 
    'center': fields.Nested(CENTER_MODEL, allow_null=True, skip_none=True), 
    'location': fields.Nested(LOCATION_MODEL, allow_null=True, skip_none=True), 
    'label': fields.String, 
    'dataset': fields.String, 
    'ipath': fields.String, 
    'dataset_level': fields.String, 
    'dataset_type': fields.String, 
    'starttime': fields.String(description='ISO 8601 datetime'),
    'endtime': fields.String(description='ISO 8601 datetime'),
    'temporal_span': fields.Integer,
    'images': fields.List(fields.Nested(IMAGE_MODEL, allow_null=True, skip_none=True)),
    'system_version': fields.String, 
    'id': fields.String, 
    'metadata': fields.Raw,
}, allow_null=True, skip_none=True)
