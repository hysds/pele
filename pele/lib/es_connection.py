from flask import current_app
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth


AWS_ES = current_app.config['AWS_ES']
AWS_REGION = current_app.config['AWS_REGION']

ES_HOST = current_app.config['ES_HOST']
ES_URL = current_app.config['ES_URL']

ES_CLIENT = None


def get_es_client():
    global ES_CLIENT

    if ES_CLIENT is None:
        if AWS_ES is True:
            ES_CLIENT = Elasticsearch(
                hosts=[ES_URL],
                http_auth=BotoAWSRequestsAuth(aws_host=ES_HOST, aws_region=AWS_REGION, aws_service='es'),
                use_ssl=True,
                connection_class=RequestsHttpConnection,
                verify_certs=False,
                ssl_show_warn=False
            )
        else:
            ES_CLIENT = Elasticsearch(hosts=[ES_URL])
    return ES_CLIENT
