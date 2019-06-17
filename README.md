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
flask create-db
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

In [4]: r = requests.post(base_url + '/login', auth=HTTPBasicAuth('koa@test.com', 'test'), verify=False)

In [5]: r.status_code
Out[5]: 401

In [6]: r.content
Out[6]: 'Unauthorized Access'

In [7]: r = requests.post(base_url + '/register', data={'email': 'koa@test.com', 'password': 'test'}, verify=False)

In [8]: r.status_code
Out[8]: 201

In [9]: r.json()
Out[9]: {u'email': u'koa@test.com',
 u'id': 2,
 u'message': u'Verification email sent. Verify before using the API.',
 u'success': True}
```

### verify user
```
In [10]: r = requests.post(base_url + '/verify', data={'email': 'koa@test.com', 'verification_code': '3d990a2e-f036-44c4-86ad-f33cfe894ef3'}, verify=False)

In [11]: r.status_code
Out[11]: 200

In [12]: r.json()
Out[12]: 
{u'message': u'Mahalo for verifying. You may now login to receive an API token.',
 u'success': True}
```

### login to get API token
```
In [13]: r = requests.post(base_url + '/login', auth=HTTPBasicAuth('koa@test.com', 'test'), verify=False)

In [14]: r.status_code
Out[14]: 200

In [15]: r.json()
Out[15]: {u'token': u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Mjg0MjczNzIsInN1YiI6ImdlcmFsZEB0ZXN0LmNvbSIsImV4cCI6MTUyODQyOTE3Mn0.dlR4ZJzXDzi8dsiaq6ZdXTqT6TJPtI_7IHnCyCDoio0'}

In [16]: token = r.json()['token']
```

### call restricted API using token
```
In [17]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'})

In [18]: r.status_code
Out[18]: 401

In [19]: r.json()
Out[19]: 
{u'authenticated': False,
 u'message': u'Invalid token. Registeration and/or authentication required'}

In [20]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

In [21]: r.status_code
Out[21]: 200

In [22]: r.json()
Out[22]: {u'message': u'hello world', u'success': True}
```

### refresh API token after expiration
```
In [23]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

In [24]: r.status_code
Out[24]: 401

In [25]: r.json()
Out[25]: 
{u'authenticated': False,
 u'message': u'Expired token. Reauthentication required.'}

In [26]: r = requests.post(base_url + '/login', auth=HTTPBasicAuth('koa@test.com', 'test'))

In [27]: token = r.json()['token']

In [28]: r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

In [29]: r.json()
Out[29]: {u'message': u'hello world', u'success': True}
```

### use the Pele requests client to handle token expiration/refreshing for you
Ensure your login creds are set in your .netrc file, e.g.
```
cat ~/.netrc
machine localhost login koa@test.com password test
macdef init


```
The Pele requests client will then use your creds to attain an API token to use for subsequent API calls. When the token expires, the client will refresh the token automatically:
```
from pele.lib.client import PeleRequests

    
base_url = "http://localhost:8877/api/v0.1"

# instantiate PeleRequests object
pr = PeleRequests(base_url)

# now use like requests module (`request()`, `get()`, `head()`, `post()`, `put()`, `delete()`, `patch()`)
r = pr.get(base_url + '/test/echo', params={'echo_str': 'hello world'})
```
