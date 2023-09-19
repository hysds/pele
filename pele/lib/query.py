from builtins import object
import json

from flask import current_app

from pele import cache

# MAX_SIZE = 2147483647
MAX_SIZE = 10000


def get_page_size(r):
    """Return page size."""
    page_size = int(r.form.get('page_size', r.args.get('page_size', current_app.config['DEFAULT_PAGE_SIZE'])))
    if page_size > current_app.config['MAX_PAGE_SIZE']:
        raise RuntimeError("Maximum page size is {}.".format(current_app.config['MAX_PAGE_SIZE']))
    return page_size


def get_offset(r):
    """Return page size."""
    return int(r.form.get('offset', r.args.get('offset', 0)))


def parse_polygon(p):
    """
    Parses string polygon to List
    ex: [[[148.16571324025443, -34.86565143737159], ... , [148.16571324025443, -34.86565143737159]]]
    :param p: str
    :return: List
    """
    try:
        p = json.loads(p)
        if type(p) != list:
            raise TypeError("polygon must be type list")
        return p
    except json.JSONDecodeError:
        raise ValueError('Invalid polygon value: %s' % p)


def get_page_size_and_offset(r):
    """Return page size and offset."""
    page_size = get_page_size(r)
    offset = get_offset(r)
    if page_size + offset > 10000:
        raise RuntimeError('Elasticsearch does not allow page_size + offset to be > 10,000')
    return page_size, offset


class QueryES(object):
    """Class for querying ES backend."""

    def __init__(self, es_client, Search, Q, A):  # noqa
        """
        :param es_client: the object returned from Elasticsearch(...)
        :param Search: function from elasticsearch DSL
        :param Q: function from elasticsearch DSL
        :param A: function from elasticsearch DSL
        """
        self.client = es_client
        self.Search = Search
        self.Q = Q
        self.A = A

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

        s = self.Search(using=self.client, index=index).extra(size=0)
        a = self.A('terms', field='dataset_type.keyword', size=MAX_SIZE)
        s.aggs.bucket('types', a)

        current_app.logger.debug(s.to_dict())

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

        s = self.Search(using=self.client, index=index).extra(size=0)
        a = self.A('terms', field='dataset.keyword', size=MAX_SIZE)
        s.aggs.bucket('datasets', a)

        current_app.logger.debug(s.to_dict())

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

        s = self.Search(using=self.client, index=index).extra(size=0)
        q = self.Q('term', dataset_type__keyword=dataset_type)
        a = self.A('terms', field='dataset.keyword', size=MAX_SIZE)
        s = s.query(q)
        s.aggs.bucket('datasets', a)

        current_app.logger.debug(s.to_dict())

        datasets = [i['key'] for i in s.execute().aggregations.to_dict()['datasets']['buckets']]
        return len(datasets), datasets[offset:offset + page_size]

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

        s = self.Search(using=self.client, index=index).extra(size=0)
        q = self.Q('term', dataset__keyword=dataset)
        a = self.A('terms', field='dataset_type.keyword', size=MAX_SIZE)
        s = s.query(q)
        s.aggs.bucket('types', a)

        current_app.logger.debug(s.to_dict())

        types = [i['key'] for i in s.execute().aggregations.to_dict()['types']['buckets']]
        return len(types), types[offset:offset+page_size]

    def query_ids_by_dataset(self, index, dataset, offset, page_size, start_time=None, end_time=None, polygon=None):
        """
        Return list of ids by dataset:
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
        :param index: Elasticsearch index/alias
        :param dataset: dataset field in ES
        :param offset: page offset from 0
        :param page_size: self-explanatory
        :param start_time: (optional) Greater than or equal of Timestamp field (start_time) in ISO format
        :param end_time: (optional) Less than of Timestamp field (end_time) in ISO format
        :param polygon: (optional) List[List[int]]
        :return: Elasticsearch document
        """

        s = self.Search(using=self.client, index=index).query(self.Q('term', dataset__keyword=dataset))
        if start_time is not None:
            s = s.query('range', **{'starttime': {'gte': start_time}})
        if end_time is not None:
            s = s.query('range', **{'endtime': {'lt': end_time}})
        if polygon is not None:
            s = s.query('geo_shape', **{
                'location': {
                    'shape': {
                        'type': 'polygon',
                        'coordinates': polygon
                    }
                }
            })

        s._source = ['id']
        current_app.logger.debug(s.to_dict())
        s = s[offset:offset + page_size]
        return s.count(), [i['id'] for i in s]

    def query_ids_by_type(self, index, dataset_type, offset, page_size, start_time=None, end_time=None, polygon=None):
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
        :param index: Elasticsearch index/alias
        :param dataset_type: dataset_type field in ES
        :param offset: page offset from 0
        :param page_size: self-explanatory
        :param start_time: (optional) Greater than or equal of Timestamp field (start_time) in ISO format
        :param end_time: (optional) Less than of Timestamp field (end_time) in ISO format
        :param polygon: (optional) List[List[int]]
        :return: Elasticsearch document
        """

        s = self.Search(using=self.client, index=index).query(self.Q('term', dataset_type__keyword=dataset_type))
        if start_time is not None:
            s = s.query('range', **{'starttime': {'gte': start_time}})
        if end_time is not None:
            s = s.query('range', **{'endtime': {'lt': end_time}})
        if polygon is not None:
            s = s.query('geo_shape', **{
                'location': {
                    'shape': {
                        'type': 'polygon',
                        'coordinates': polygon
                    }
                }
            })

        s._source = ['id']
        current_app.logger.debug(s.to_dict())
        s = s[offset:offset + page_size]
        return s.count(), [i['id'] for i in s]

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
        s = self.Search(using=self.client, index=index).query(self.Q('term', _id=_id))
        current_app.logger.debug(s.to_dict())
        resp = s.execute()
        return resp[0].to_dict() if s.count() > 0 else None

    def query_fields(self, index, terms, fields, offset, page_size, start_time=None, end_time=None, polygon=None):
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
          "_source": [
            "id",
            "metadata.trackNumber",
            "location"
          ]
        }
        :param index: Elasticsearch index/alias
        :param terms: Dict; "custom" fields to filter on
        :param fields: fields to be returned by Elasticsearch
        :param offset: page offset from 0
        :param page_size: self-explanatory
        :param start_time: (optional) Greater than or equal of Timestamp field (start_time) in ISO format
        :param end_time: (optional) Less than of Timestamp field (end_time) in ISO format
        :param polygon: (optional) List[List[int]]
        :return: Elasticsearch document
        """

        q = None
        for field, val in list(terms.items()):
            f = field.lower().replace('.', '__')
            if q is None:
                q = self.Q('term', **{f: val})
            else:
                q += self.Q('term', **{f: val})

        s = self.Search(using=self.client, index=index).query(q)
        if start_time is not None:
            s = s.query('range', **{'starttime': {'gte': start_time}})
        if end_time is not None:
            s = s.query('range', **{'endtime': {'lt': end_time}})
        if polygon is not None:
            s = s.query('geo_shape', **{
                'location': {
                    'shape': {
                        'type': 'polygon',
                        'coordinates': polygon
                    }
                }
            })

        s._source = fields
        # sort by starttime in descending order; TODO: expose sort parameters out through API
        s = s.sort({
            "starttime": {
                "order": "desc"
            }
        })
        s = s[offset:offset + page_size]

        current_app.logger.debug(s.to_dict())
        return s.count(), [i.to_dict() for i in s]

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
          "_source": [
            "id",
            "metadata.trackNumber",
            "location"
          ]
        }
        """

        # get document by id
        doc = self.query_id(index, _id)
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
                t = self.Q('term', **{f: val})
            else:
                t += self.Q('term', **{f: val})

        # set temporal query
        q = self.Q()
        if starttime is not None:
            q += self.Q('range', **{'endtime': {'gt': starttime}})
        if endtime is not None:
            q += self.Q('range', **{'starttime': {'lt': endtime}})

        # set spatial filter
        f = None
        if location is not None:
            f = self.Q('geo_shape', **{'location': {'shape': location}})

        # search
        s = self.Search(using=self.client, index=index)
        if t is not None:
            s = s.query(t)
        if q != self.Q():
            s = s.query(q)
        if f is not None:
            s = s.filter(f)
        s._source = fields

        current_app.logger.debug(s.to_dict())
        return s.count(), [i.to_dict() for i in s[offset:offset+page_size]]
