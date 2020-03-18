from setuptools import setup, find_packages

setup(
    name='pele',
    version='0.0.1',
    long_description='REST API for HySDS Datasets',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[ 'Flask',
                       'gunicorn',
                       'gevent',
                       'eventlet',
                       'supervisor',
                       'requests',
                       'Flask-Assets',
                       'Flask-Bcrypt',
                       'Flask-Caching',
                       'Flask-Cors',
                       'Flask-DebugToolbar',
                       'Flask-HTTPAuth',
                       'Flask-Limiter',
                       'Flask-Login',
                       'Flask-Mail',
                       'Flask-Migrate',
                       'Flask-RestPlus',
                       'Flask-Script',
                       'Flask-SQLAlchemy',
                       'Flask-Testing',
                       'Flask-WTF',
                       'simpleldap',
                       'elasticsearch>=1.0.0,<2.0.0',
                       'elasticsearch-dsl<2.0.0',
                       'pyshp',
                       'shapely==1.5.15',
                       'Cython',
                       #'Cartopy==0.13.1',
                       'redis',
                       'bcrypt',
                       'PyJWT',
                       'coverage',
                       'webassets',
                       'lxml',
                       'nodeenv',
                     ]
)
