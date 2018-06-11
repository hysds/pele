import json, requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import FacetedSearch, Search, Q, A
from flask import current_app

from pele import cache


class QueryES():
    """Class for querying ES backend."""

    client = None

    def __init__(self, es_url, es_index):
        self.es_url = es_url
        self.es_index = es_index
        self.client = Elasticsearch(es_url)

    def query_datasets(self):
        """Return list of datasets:
    
        {
          "query": {
            "match_all": {}
          }, 
          "aggs": {
            "datasets": {
              "terms": {
                "field": "_type", 
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        s = Search(using=self.client, index=self.es_index).extra(size=0)
        a = A('terms', field='_type', size=0)
        s.aggs.bucket('datasets', a)
        resp = s.execute()
        return [i['key'] for i in resp.aggregations.to_dict()['datasets']['buckets']]
