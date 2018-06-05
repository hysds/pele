#!/usr/bin/env python
import unittest
from pele import create_app, db
from pele.models.user import User


class TestModels(unittest.TestCase):
    def setUp(self):
        app = create_app('pele.settings.DevelopmentConfig')
        self.app = app.test_client()
        db.app = app
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        admin = User('admin', 'admin@test.com', 'supersafepassword')

        assert admin.username == 'admin'
        assert admin.password == 'supersafepassword'

        db.session.add(admin)
        db.session.commit()
