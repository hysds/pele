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
By default, development mode is on:
```
flask run -h 0.0.0.0 -p 8877
```

To explicitly set development mode:
```
FLASK_ENV=development flask run -h 0.0.0.0 -p 8877
```

## To run in production mode
Using flask's development web server (not recommended for production):
```
FLASK_ENV=production flask run -h 0.0.0.0 -p 8877
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
