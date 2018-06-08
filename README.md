# pele
REST API for HySDS Datasets

## Create virtualenv
```
virtualenv --system-site-packages env
source env/bin/activate
```

## Install Dependencies via pip
```
git clone https://github.com/hysds/pele.git
cd pele
pip install -e .
```

## Create DB
```
flask create_db
flask db init
flask db migrate
```

## Run tests
```
flask test
```

## Run tests under code coverage
```
flask cov
```

## To run in development mode
```
FLASK_ENV=development flask run -h 0.0.0.0 -p 8877
```

## To run in production mode
Using flask's development web server (not recommended for production):
```
FLASK_ENV=production flask run -h 0.0.0.0 -p 8877
```
or 
```
flask run -h 0.0.0.0 -p 8877
```

Instead use gunicorn. As a daemon:
```
gunicorn -w4 -b 0.0.0.0:8877 -k gevent --log-level=debug --timeout=3600 \
  --graceful-timeout=3600 --limit-request-line=0 --daemon --pid pele.pid \
  'pele:create_app("pele.settings.ProductionConfig")'
```

In the foreground:
```
gunicorn -w4 -b 0.0.0.0:8877 -k gevent --log-level=debug --timeout=3600 \
  --graceful-timeout=3600 --limit-request-line=0 \
  'pele:create_app("pele.settings.ProductionConfig")'
```

## Examples

### user registration
```
In [1]: import requests, json

In [2]: from requests.auth import HTTPBasicAuth

In [3]: base_url = 'http://localhost:8877/api/v0.1'

In [4]: r = requests.post(base_url + '/login', auth=HTTPBasicAuth('gerald@test.com', 'test'))

In [5]: r.status_code
Out[5]: 401

In [6]: r.content
Out[6]: 'Unauthorized Access'

In [7]: r = requests.post(base_url + '/register', data={'email': 'gerald@test.com', 'password': 'test'})

In [8]: r.status_code
Out[8]: 201

In [9]: r.json()
Out[9]: {u'email': u'gerald@test.com', u'id': 1}
```

### get API token
```
In [10]: r = requests.post(base_url + '/login', auth=HTTPBasicAuth('gerald@test.com', 'test'))

In [11]: r.status_code
Out[11]: 200

In [12]: r.json()
Out[12]: {u'token': u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Mjg0MjczNzIsInN1YiI6ImdlcmFsZEB0ZXN0LmNvbSIsImV4cCI6MTUyODQyOTE3Mn0.dlR4ZJzXDzi8dsiaq6ZdXTqT6TJPtI_7IHnCyCDoio0'}

In [13]: token = r.json()['token']
```

### call restricted API using token
```
In [15]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'})

In [16]: r.status_code
Out[16]: 401

In [17]: r.json()
Out[17]: 
{u'authenticated': False,
 u'message': u'Invalid token. Registeration and/or authentication required'}

In [19]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

In [20]: r.status_code
Out[20]: 200

In [21]: r.json()
Out[21]: {u'message': u'hello world', u'success': True}
```

### refresh API token after expiration
```
In [31]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

In [32]: r.status_code
Out[32]: 401

In [33]: r.json()
Out[33]: 
{u'authenticated': False,
 u'message': u'Expired token. Reauthentication required.'}

In [34]: r = requests.post(base_url + '/login', auth=HTTPBasicAuth('test@test.com', 'test'))

In [35]: token = r.json()['token']

In [36]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

In [37]: r.json()
Out[37]: {u'message': u'hello world', u'success': True}
```

### use the Pele requests client to handle token expiration/refreshing for you
```
from pele.lib.client import PeleRequests

    
base_url = "http://localhost:8877/api/v0.1"

# instantiate PeleRequests object
pr = PeleRequests(base_url)

# now use like requests module (`request()`, `get()`, `head()`, `post()`, `put()`, `delete()`, `patch()`)
r = pr.get(base_url + '/test/echo', params={'echo_str': 'hello world'})
```
