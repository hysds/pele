# pele
REST API for HySDS Datasets

## Create virtualenv
```bash
virtualenv --system-site-packages env
source env/bin/activate
```

## Install Dependencies via pip
```bash
git clone https://github.com/hysds/pele.git
cd pele
pip install -e .
```

## Create DB
```bash
flask create-db
flask db init
flask db migrate
```

## Run tests
```bash
flask test
```

## Run tests under code coverage
```bash
flask cov
```

## To run in development mode
```bash
FLASK_ENV=development flask run -h 0.0.0.0 -p 8877
```

## To run in production mode
Using flask's development web server (not recommended for production):
```bash
FLASK_ENV=production flask run -h 0.0.0.0 -p 8877
```
or 
```bash
flask run -h 0.0.0.0 -p 8877
```

Instead use gunicorn. As a daemon:
```bash
gunicorn -w4 -b 0.0.0.0:8877 -k gevent --log-level=debug --timeout=3600 \
  --graceful-timeout=3600 --limit-request-line=0 --daemon --pid pele.pid \
  'pele:create_app("pele.settings.ProductionConfig")'
```

In the foreground:
```bash
gunicorn -w4 -b 0.0.0.0:8877 -k gevent --log-level=debug --timeout=3600 \
  --graceful-timeout=3600 --limit-request-line=0 \
  'pele:create_app("pele.settings.ProductionConfig")'
```

## Examples

### user registration
```python
import requests
from requests.auth import HTTPBasicAuth

base_url = 'http://localhost:8877/api/v0.1'

r = requests.post(base_url + '/login', auth=HTTPBasicAuth('koa@test.com', 'test'), verify=False)

r.status_code
# 401

r.content
# 'Unauthorized Access'

r = requests.post(base_url + '/register', data={'email': 'koa@test.com', 'password': 'test'}, verify=False)

r.status_code
# 201

r.json()
# {u'email': u'koa@test.com',
#  u'id': 2,
#  u'message': u'Verification email sent. Verify before using the API.',
#  u'success': True}
```

### verify user
```python
r = requests.post(base_url + '/verify', data={'email': 'koa@test.com', 'verification_code': '3d990a2e-f036-44c4-86ad-f33cfe894ef3'}, verify=False)

r.status_code
# 200

r.json()
# {u'message': u'Mahalo for verifying. You may now login to receive an API token.',
#  u'success': True}
```

### login to get API token
```python
r = requests.post(base_url + '/login', auth=HTTPBasicAuth('koa@test.com', 'test'), verify=False)

r.status_code
# 200

r.json()
# {u'token': u'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE1Mjg0MjczNzIsInN1YiI6ImdlcmFsZEB0ZXN0LmNvbSIsImV4cCI6MTUyODQyOTE3Mn0.dlR4ZJzXDzi8dsiaq6ZdXTqT6TJPtI_7IHnCyCDoio0'}

token = r.json()['token']
```

### call restricted API using token
```python
r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'})

r.status_code
# 401

r.json() 
# {u'authenticated': False,
#  u'message': u'Invalid token. Registeration and/or authentication required'}

r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

r.status_code
# 200

r.json()
# {u'message': u'hello world', u'success': True}
```

### refresh API token after expiration
```python
r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

r.status_code
# 401

r.json()
# {u'authenticated': False,
#  u'message': u'Expired token. Reauthentication required.'}

r = requests.post(base_url + '/login', auth=HTTPBasicAuth('koa@test.com', 'test'))

token = r.json()['token']

r = requests.get(base_url + '/test/echo', params={'echo_str': 'hello world'}, headers={'X-API-KEY': token})

r.json()
# {u'message': u'hello world', u'success': True}
```

### use the Pele requests client to handle token expiration/refreshing for you
Ensure your login creds are set in your .netrc file, e.g.
```bash
cat ~/.netrc
# machine localhost login koa@test.com password test
# macdef init


```
The Pele requests client will then use your creds to attain an API token to use for subsequent API calls. When the token expires, the client will refresh the token automatically:
```python
from pele.lib.client import PeleRequests
    
base_url = "http://localhost:8877/api/v0.1"

# instantiate PeleRequests object
pr = PeleRequests(base_url)

# now use like requests module (`request()`, `get()`, `head()`, `post()`, `put()`, `delete()`, `patch()`)
r = pr.get(base_url + '/test/echo', params={'echo_str': 'hello world'})
```
