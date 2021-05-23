from flask import Flask, render_template, redirect, url_for, request
from flask import url_for
import pytest
import fwtapp
from flask_testing import TestCase
from fwtapp import Characters, location, time, app, db

class TestBase(TestCase):
    def create_app(self):

        app.config.update(SQLALCHEMY_DATABASE_URI="sqlite:///",
                SECRET_KEY='rtadfgfgvbpofusnfg',
                DEBUG=True,
                WTF_CSRF_ENABLED=False)
        return app

    def setUp(self):
        db.create_all()

        samplec = Characters(cname="Eddard Stark")
        samplel = location(lname="Winterfell")

        db.session.add(samplec)
        db.session.add(samplel)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestViews(TestBase):

    def test_home_get(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 302)
    
    def test_add_character_get(self):
        response = self.client.get(url_for('newcharacter'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Eddard Stark', response.data)

    def test_add_location_get(self):
        response = self.client.get(url_for('newlocation'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Winterfell', response.data)

    def test_journey_get(self):
        response = self.client.get(url_for('journey'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Eddard Stark', response.data)
        self.assertIn(b'Winterfell', response.data)



class TestAdd(TestBase):
    def test_new_character_post(self):
        response = self.client.post(
            url_for('newcharacter'),
            data = dict(cname="Caitlyn Stark"),
            follow_redirects=True
        )
        self.assertIn(b"Caitlyn Stark",response.data)

    def test_new_location_post(self):
        response = self.client.post(
            url_for('newlocation'),
            data = dict(lname="Riverrun"),
            follow_redirects=True
        )
        self.assertIn(b"Riverrun",response.data)
        
    def test_delete_location(self):
        response = self.client.post(url_for("deleteloc", lid=2),
        follow_redirects=True)
        self.assertNotIn(b'Riverrun',response.data)

    def test_delete_character(self):
        response = self.client.post(url_for("deletechar", cid=2),
        follow_redirects=True)
        self.assertNotIn(b'Caitlyn Stark',response.data)

    def test_update_character_get(self):
        response = self.client.get(url_for('updatechar',cid=1),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Eddard Stark', response.data)

    def test_update_location_get(self):
        response = self.client.get(url_for('updateloc', lid=1),
        follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Winterfell', response.data)