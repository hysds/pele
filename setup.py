from setuptools import setup, find_packages

setup(
    name='pele',
    version='1.1.3',
    long_description='REST API for HySDS Datasets',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask>=2.0.0',
        'flask-restx>=0.5.1',
        'Flask-Assets>=2.0',
        'Flask-Bcrypt>=0.7.1',
        'Flask-Caching>=1.10.1',
        'Flask-Cors>=3.0.10',
        'Flask-DebugToolbar>=0.11.0',
        'Flask-HTTPAuth>=4.4.0',
        'Flask-Limiter>=1.4',
        'Flask-Login>=0.5.0',
        'Flask-Mail>=0.9.1',
        'Flask-Migrate>=2.7.0',  # may need to look into sdscli to update this to >=3.0.0
        'Flask-Script>=2.0.6',
        'Flask-SQLAlchemy>=2.5.1',
        'Flask-Testing>=0.8.1',
        'Flask-WTF>=0.15.1',
        "elasticsearch>=7.0.0,7.14.0",
        'elasticsearch-dsl>=7.0.0,<7.4.0',
        'shapely>=1.5.15,<1.7.0',
        'PyJWT==1.7.1',
        'WTForms>=2.0.0',
        "aws-requests-auth==0.4.2",
        'gunicorn',
        'gevent',
        'eventlet',
        'supervisor',
        'requests',
        'simpleldap',
        'pyshp',
        'Cython',
        # 'Cartopy==0.13.1',
        'redis',
        'bcrypt',
        'coverage',
        'webassets',
        'lxml',
        'nodeenv',
        'botocore',
    ]
)
