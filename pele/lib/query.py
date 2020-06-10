from builtins import object
import json, requests
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


class QueryES(object):
    """Class for querying ES backend."""

    client = None

    def __init__(self, es_client):
        """
        :param es_client: the object returned from Elasticsearch(...)
        """
        self.client = es_client

    def query_types(self, index, offset, page_size):
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

        s = Search(using=self.client, index=index).extra(size=0)
        a = A('terms', field='dataset_type.keyword', size=0)
        s.aggs.bucket('types', a)
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        types = [i['key'] for i in s.execute().aggregations.to_dict()['types']['buckets']]
        return len(types), types[offset:offset+page_size]
    
    def query_datasets(self, index, offset, page_size):
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
    
        s = Search(using=self.client, index=index).extra(size=0)
        a = A('terms', field='dataset.keyword', size=0)
        s.aggs.bucket('datasets', a)
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        datasets = [i['key'] for i in s.execute().aggregations.to_dict()['datasets']['buckets']]
        return len(datasets), datasets[offset:offset+page_size]

    def query_datasets_by_type(self, index, dataset_type, offset, page_size):
        """Return list of datasets by type:
        {
          "query": {
            "term": {
              "dataset_type.keyword": "area_of_interest"
            }
          }, 
          "aggs": {
            "datasets": {
              "terms": {
                "field": "dataset.keyword",
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        s = Search(using=self.client, index=index).extra(size=0)
        q = Q('term', dataset_type__raw=dataset_type)
        a = A('terms', field='dataset.keyword', size=0)
        s = s.query(q)
        s.aggs.bucket('datasets', a)
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        datasets = [i['key'] for i in s.execute().aggregations.to_dict()['datasets']['buckets']]
        return len(datasets), datasets[offset:offset+page_size]

    def query_types_by_dataset(self, index, dataset, offset, page_size):
        """Return list of types by dataset:
        {
          "query": {
            "term": {
              "dataset.keyword": "area_of_interest"
            }
          }, 
          "aggs": {
            "types": {
              "terms": {
                "field": "dataset_type.keyword",
                "size": 0
              }
            }
          }, 
          "size": 0
        }
        """
    
        s = Search(using=self.client, index=index).extra(size=0)
        q = Q('term', dataset__raw=dataset)
        a = A('terms', field='dataset_type.keyword', size=0)
        s = s.query(q)
        s.aggs.bucket('types', a)
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        types = [i['key'] for i in s.execute().aggregations.to_dict()['types']['buckets']]
        return len(types), types[offset:offset+page_size]

    def query_ids_by_dataset(self, index, dataset, offset, page_size):
        """Return list of ids by dataset:
        {
          "query": {
            "term": {
              "dataset.keyword": "area_of_interest"
            }
          }, 
          "fields": [
            "_id"
          ]
        }
        """
    
        s = Search(using=self.client, index=index).query(Q('term', dataset__raw=dataset)).fields(['_id'])
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i['_id'] for i in s[offset:offset+page_size]]

    def query_ids_by_type(self, index, dataset_type, offset, page_size):
        """Return list of ids by type:
        {
          "query": {
            "term": {
              "dataset_type.keyword": "area_of_interest"
            }
          }, 
          "fields": [
            "_id"
          ]
        }
        """
    
        s = Search(using=self.client, index=index).query(Q('term', dataset_type__raw=dataset_type)).fields(['_id'])
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i['_id'] for i in s[offset:offset+page_size]]

    def query_id(self, index, _id):
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
    
        s = Search(using=self.client, index=index).query(Q('term', _id=_id))
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        resp = s.execute()
        return resp[0].to_dict() if s.count() > 0 else None

    def query_fields(self, index, terms, fields, offset, page_size):
        """Return list of documents by term bool query:
        {
          "query": {
            "bool": {
              "must": [
                { 
                  "term": {
                    "dataset_type.keyword": "acquisition"
                  }
                },
                { 
                  "term": {
                    "dataset.keyword": "acquisition-S1-IW_SLC"
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
        for field, val in list(terms.items()):
            f = field.lower().replace('.', '__')
            if q is None:
                q = Q('term', **{ f: val })
            else:
                q += Q('term', **{ f: val })
        s = Search(using=self.client, index=index).query(q).partial_fields(partial={'include': fields})
        # sort by starttime in descending order; TODO: expose sort parameters out through API
        s = s.sort({"starttime" : {"order" : "desc"}})
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i.to_dict() for i in s[offset:offset+page_size]]

    def overlaps(self, index, _id, terms, fields, offset, page_size):
        """Return list of documents that overlap temporally and spatially:
        {
          "query": {
            "filtered": {
              "filter": {
                "geo_shape": {
                  "location": {
                    "shape": {
                      "type": "polygon", 
                      "coordinates": [
                        [
                          [
                            123.234154, 
                            -33.344517
                          ], 
                          [
                            120.578377, 
                            -32.708748
                          ], 
                          [
                            121.122925, 
                            -31.111742
                          ], 
                          [
                            123.731133, 
                            -31.73547
                          ], 
                          [
                            123.234154, 
                            -33.344517
                          ]
                        ]
                      ]
                    }
                  }
                }
              }, 
              "query": {
                "bool": {
                  "must": [
                    {
                      "range": {
                        "endtime": {
                          "gt": "2017-04-18T21:09:23.789"
                        }
                      }
                    }, 
                    {
                      "range": {
                        "starttime": {
                          "lt": "2017-04-18T21:09:50.741"
                        }
                      }
                    }
                  ]
                }
              }
            }
          }, 
          "partial_fields": {
            "partial": {
              "include": [
                "id"
              ]
            }
          }
        }
        """
    
        # get document by id
        doc = self.query_id(_id)
        current_app.logger.debug(json.dumps(doc, indent=2))
        if doc is None:
            raise RuntimeError("Failed to find dataset ID: {}".format(_id))

        # get spatial and temporal fields
        starttime = doc.get('starttime', None)
        endtime = doc.get('endtime', None)
        location = doc.get('location', None)

        # build terms query
        t = None
        for field, val in list(terms.items()):
            f = field.lower().replace('.', '__')
            if t is None:
                t = Q('term', **{f: val})
            else:
                t += Q('term', **{f: val})

        # set temporal query
        q = None
        if starttime is not None and endtime is not None:
            q = Q('range', **{'endtime': {'gt': starttime}}) + Q('range', **{'starttime': {'lt': endtime}})
        elif starttime is not None and endtime is None:
            q = Q('range', **{'endtime': {'gt': starttime}})
        elif starttime is None and endtime is not None:
            q = Q('range', **{'starttime': {'lt': endtime}})

        # set spatial filter
        f = None
        if location is not None:
            f = Q('geo_shape', **{'location': {'shape': location}})

        # search
        s = Search(using=self.client, index=index)
        if t is not None:
            s = s.query(t)
        if q is not None:
            s = s.query(q)
        if f is not None:
            s = s.filter(f)
        s = s.partial_fields(partial={'include': fields})
        current_app.logger.debug(json.dumps(s.to_dict(), indent=2))
        return s.count(), [i.to_dict() for i in s[offset:offset+page_size]]
