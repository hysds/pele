from setuptools import setup, find_packages

setup(
    name='pele',
    version='1.1.2',
    long_description='REST API for HySDS Datasets',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # TODO: remove this pin on click once this celery issue is resolved:
        # https://github.com/celery/celery/issues/6768
        # 'click>=7.0,<8.0',  # don't think we need click here because its nto used by mozart
        # TODO: remove these pins on flask/extensions once the celery issue above is resolved
        'Flask>2.0.0,<3.0.0',
        'flask-restx>=0.5.1',
        'Flask-Assets>=2.0,<3.0.0',
        'Flask-Bcrypt>=0.7.1,<1.0.0',
        'Flask-Caching>=1.10.1,<2.0.0',
        'Flask-Cors>=3.0.10,<4.0.0',
        'Flask-DebugToolbar>=0.11.0,<1.0.0',
        'Flask-HTTPAuth>=4.4.0,<5.0.0',
        'Flask-Limiter>=1.4,<2.0.0',
        'Flask-Login>=0.5.0,<1.0.0',
        'Flask-Mail>=0.9.1,<1.0.0',
        'Flask-Migrate>=2.7.0,<3.0.0',  # may need to look into sdscli to update this to >=3.0.0
        'Flask-Script>=2.0.6,<3.0.0',
        'Flask-SQLAlchemy>=2.5.1,<3.0.0',
        'Flask-Testing>=0.8.1,<1.0.0',
        'Flask-WTF>=0.15.1,<1.0.0',
        'elasticsearch>=7.0.0,<7.14.0',
        'elasticsearch-dsl>=7.0.0,<7.4.0',
        'shapely>=1.5.15,<1.7.0',
        'PyJWT==1.7.1',
        'WTForms>=2.0.0,<3.0.0',
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
