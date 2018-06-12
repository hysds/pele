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
                "field": "dataset", 
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        s = Search(using=self.client, index=self.es_index).extra(size=0)
        a = A('terms', field='dataset.raw', size=0)
        s.aggs.bucket('datasets', a)
        resp = s.execute()
        return [i['key'] for i in resp.aggregations.to_dict()['datasets']['buckets']]

    def query_types(self):
        """Return list of dataset types:
    
        {
          "query": {
            "match_all": {}
          }, 
          "aggs": {
            "types": {
              "terms": {
                "field": "dataset_type", 
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        s = Search(using=self.client, index=self.es_index).extra(size=0)
        a = A('terms', field='dataset_type.raw', size=0)
        s.aggs.bucket('types', a)
        resp = s.execute()
        return [i['key'] for i in resp.aggregations.to_dict()['types']['buckets']]

    def query_datasets_by_type(self, dataset_type):
        """Return list of datasets by type:
    
        {
          "query": {
            "term": {
              "dataset_type.raw": "area_of_interest"
            }
          }, 
          "aggs": {
            "datasets": {
              "terms": {
                "field": "dataset.raw", 
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        #s = Search(using=self.client, index=self.es_index).query(Q('term', dataset_type__raw=dataset_type)).fields(['_id'])
        #return [i['_id'] for i in s[:s.count()]]
        s = Search(using=self.client, index=self.es_index).extra(size=0)
        q = Q('term', dataset_type__raw=dataset_type)
        a = A('terms', field='dataset.raw', size=0)
        s = s.query(q)
        s.aggs.bucket('datasets', a)
        resp = s.execute()
        return [i['key'] for i in resp.aggregations.to_dict()['datasets']['buckets']]
