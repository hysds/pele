from flask import current_app
from elasticsearch import Elasticsearch, RequestsHttpConnection
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth


ES_CLIENT = None


def get_es_client():
    global ES_CLIENT

    aws_es = current_app.config['AWS_ES']
    aws_region = current_app.config['AWS_REGION']

    es_host = current_app.config['ES_HOST']
    es_url = current_app.config['ES_URL']

    if ES_CLIENT is None:
        if aws_es is True:
            ES_CLIENT = Elasticsearch(
                hosts=[es_url],
                http_auth=BotoAWSRequestsAuth(aws_host=es_host, aws_region=aws_region, aws_service='es'),
                use_ssl=True,
                connection_class=RequestsHttpConnection,
                verify_certs=False,
                ssl_show_warn=False
            )
        else:
            ES_CLIENT = Elasticsearch(hosts=[es_url])
    return ES_CLIENT
