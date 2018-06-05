#!/usr/bin/env python
import unittest
from pele import create_app


class TestConfig(unittest.TestCase):
    def test_dev_config(self):
        app = create_app('pele.settings.DevelopmentConfig')

        assert app.config['DEBUG'] is True
        #assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../database.db'
        assert app.config['SQLALCHEMY_ECHO'] is True
        assert app.config['CACHE_TYPE'] == 'null'

    def test_prod_config(self):
        app = create_app('pele.settings.ProductionConfig')

        #assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///../database.db'
        #assert app.config['CACHE_TYPE'] == 'simple'
