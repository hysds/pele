import boto3
from elasticsearch import Elasticsearch, RequestsHttpConnection as RequestsHttpConnectionES
from opensearchpy import OpenSearch, AWSV4SignerAuth, RequestsHttpConnection as RequestsHttpConnectionOS

ES_CLIENT = None


def get_es_client(config):
    global ES_CLIENT

    es_engine = config.get("ES_ENGINE", "elasticsearch")
    aws_es = config.get('AWS_ES', False)
    aws_region = config.get('AWS_REGION', 'us-west-2')

    es_url = config.get('ES_URL', 'http://127.0.0.1:9200')

    if ES_CLIENT is None:
        if es_engine == "opensearch":
            if aws_es is True or "es.amazon.com" in es_url:
                credentials = boto3.Session().get_credentials()
                auth = AWSV4SignerAuth(credentials, aws_region)
                ES_CLIENT = OpenSearch(
                    hosts=[es_url],
                    http_auth=auth,
                    connection_class=RequestsHttpConnectionOS,
                    use_ssl=True,
                    verify_certs=False,
                    ssl_show_warn=False,
                    timeout=30,
                    max_retries=10,
                    retry_on_timeout=True,
                )
            else:
                ES_CLIENT = OpenSearch(es_url)
        else:
            if aws_es is True or "es.amazon.com" in es_url:
                credentials = boto3.Session().get_credentials()
                auth = AWSV4SignerAuth(credentials, aws_region)
                ES_CLIENT = Elasticsearch(
                    hosts=[es_url],
                    http_auth=auth,
                    connection_class=RequestsHttpConnectionES,
                    use_ssl=True,
                    verify_certs=False,
                    ssl_show_warn=False,
                    timeout=30,
                    max_retries=10,
                    retry_on_timeout=True,
                )
            else:
                ES_CLIENT = Elasticsearch(es_url)
    return ES_CLIENT
