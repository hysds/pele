#!/usr/bin/env python
import unittest
from pele import create_app, db
from pele.models.user import User


class TestForm(unittest.TestCase):
    def setUp(self):
        app = create_app('pele.settings.DevelopmentConfig')
        self.app = app.test_client()
        db.app = app
        db.create_all()
        admin = User('admin', 'admin@test.com', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_login(self):
        rv = self.app.post('/login', data=dict(
            username='admin',
            password="supersafepassword"
        ), follow_redirects=True)

        assert rv.status_code == 200
        assert 'Logged in successfully.' in rv.data
