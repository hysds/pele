import json, requests
from elasticsearch import Elasticsearch
from elasticsearch_dsl import FacetedSearch, Search, Q, A
from flask import current_app

from pele import cache


def get_page_size(r):
    """Return page size."""

    page_size = int(r.form.get('page_size',
        r.args.get('page_size', current_app.config['DEFAULT_PAGE_SIZE'])))
    if page_size > current_app.config['MAX_PAGE_SIZE']:
        raise RuntimeError("Maximum page size is {}.".format(current_app.config['MAX_PAGE_SIZE']))
    return page_size


def get_offset(r):
    """Return page size."""

    return int(r.form.get('offset', r.args.get('offset', 0)))


def get_page_size_and_offset(r):
    """Return page size and offset."""

    return get_page_size(r), get_offset(r)


class QueryES():
    """Class for querying ES backend."""

    client = None

    def __init__(self, es_url, es_index):
        self.es_url = es_url
        self.es_index = es_index
        self.client = Elasticsearch(es_url)

    def query_types(self, offset, page_size):
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
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        types = [i['key'] for i in s.execute().aggregations.to_dict()['types']['buckets']]
        return len(types), types[offset:offset+page_size]
    
    def query_datasets(self, offset, page_size):
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
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        datasets = [i['key'] for i in s.execute().aggregations.to_dict()['datasets']['buckets']]
        return len(datasets), datasets[offset:offset+page_size]

    def query_datasets_by_type(self, dataset_type, offset, page_size):
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
    
        s = Search(using=self.client, index=self.es_index).extra(size=0)
        q = Q('term', dataset_type__raw=dataset_type)
        a = A('terms', field='dataset.raw', size=0)
        s = s.query(q)
        s.aggs.bucket('datasets', a)
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        datasets = [i['key'] for i in s.execute().aggregations.to_dict()['datasets']['buckets']]
        return len(datasets), datasets[offset:offset+page_size]

    def query_types_by_dataset(self, dataset, offset, page_size):
        """Return list of types by dataset:
    
        {
          "query": {
            "term": {
              "dataset.raw": "area_of_interest"
            }
          }, 
          "aggs": {
            "types": {
              "terms": {
                "field": "dataset_type.raw", 
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        s = Search(using=self.client, index=self.es_index).extra(size=0)
        q = Q('term', dataset__raw=dataset)
        a = A('terms', field='dataset_type.raw', size=0)
        s = s.query(q)
        s.aggs.bucket('types', a)
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        types = [i['key'] for i in s.execute().aggregations.to_dict()['types']['buckets']]
        return len(types), types[offset:offset+page_size]

    def query_ids_by_dataset(self, dataset, offset, page_size):
        """Return list of ids by dataset:
    
        {
          "query": {
            "term": {
              "dataset.raw": "area_of_interest"
            }
          }, 
          "fields": [
            "_id"
          ]
        }
        """
    
        s = Search(using=self.client, index=self.es_index).query(Q('term', dataset__raw=dataset)).fields(['_id'])
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i['_id'] for i in s[offset:offset+page_size]]

    def query_ids_by_type(self, dataset_type, offset, page_size):
        """Return list of ids by type:
    
        {
          "query": {
            "term": {
              "dataset_type.raw": "area_of_interest"
            }
          }, 
          "fields": [
            "_id"
          ]
        }
        """
    
        s = Search(using=self.client, index=self.es_index).query(Q('term', dataset_type__raw=dataset_type)).fields(['_id'])
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i['_id'] for i in s[offset:offset+page_size]]

    def query_id(self, id):
        """Return metadata for dataset ID:
    
        {
          "query": {
            "term": {
              "_id": "AOI_earthquake_test_san_fran"
            }
          }, 
          "fields": [
            "_id"
          ]
        }
        """
    
        s = Search(using=self.client, index=self.es_index).query(Q('term', _id=id))
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        resp = s.execute()
        #current_app.logger.debug(json.dumps(resp.to_dict(), indent=2))
        #current_app.logger.debug(json.dumps([i.to_dict() for i in s[:s.count()]], indent=2))
        #return [i.to_dict() for i in s[:s.count()]]
        return resp[0].to_dict() if s.count() > 0 else None

    def query_fields(self, terms, fields, offset, page_size):
        """Return list of documents by term bool query:
    
        {
          "query": {
            "bool": {
              "must": [
                { 
                  "term": {
                    "dataset_type.raw": "acquisition"
                  }
                },
                { 
                  "term": {
                    "dataset.raw": "acquisition-S1-IW_SLC"
                  }
                }
              ]
            }
          },
          "partial_fields": {
            "partial": {
              "include": [
                "id",
                "metadata.trackNumber",
                "location"
              ]
            }
          }
        }
        """
    
        q = None
        for field, val in terms.items():
            f = field.lower().replace('.', '__')
            if q is None: q = Q('term', **{ f: val })
            else: q += Q('term', **{ f: val })
        s = Search(using=self.client, index=self.es_index).query(q).partial_fields(partial={'include': fields})
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i.to_dict() for i in s[offset:offset+page_size]]
