import flask_unittest
from app import app as flask_app
from core.extensions import db
from config import config_by_env

headers= { "Content-Type": "application/json"}

class AuthTest(flask_unittest.ClientTestCase):

    app = flask_app
    app.config.from_object(config_by_env['test'])

    def setUp(self, client):
        with self.app.app_context():
            db.create_all()

    def tearDown(self, client):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user_required_field(self, client):

        response = client.post("/api/auth/register-user", json={}, headers=headers)


        json = response.json
        # assert status code
        assert response.status_code == 422
        assert "errors" in json
        # asset the errors return contains required field error 
        assert "email" in json.get('errors')
        assert "first_name" in json.get('errors')
        assert "last_name" in json.get('errors')
        assert "password" in json.get('errors')

    
    def test_register_user(self, client):

        response = client.post("/api/auth/register-user", json={
            "email": "samuel-@example.com",
            "first_name": "Samuel",
            "last_name": "Esh....",
            "password": "password"
        }, headers=headers)

        json = response.json

        # assert status code
        assert response.status_code == 200
        # asset user model fields are present
        assert "email" in json
        assert "first_name" in json
        assert "last_name" in json
        assert "password" not in json # make sure password is not return
        assert "created_at" in json


    def test_login_user_wrong_cred(self, client):

        response = client.post("/api/auth/login", json={
            "email": "samuel-@example.com",
            "password": "wrong-pass"
        }, headers=headers)

        json = response.json

        # assert status code
        assert response.status_code == 400
        # asset error field and message are present
        assert "error" in json
        assert json.get("error") == 'Password or Email not correct.'

    def test_login_user(self, client):

        # Register user
        response = client.post("/api/auth/register-user", json={
            "email": "samuel-@example.com",
            "first_name": "Samuel",
            "last_name": "Esh....",
            "password": "password"
        }, headers=headers)

        # Authenticate the user
        response = client.post("/api/auth/login", json={
            "email": "samuel-@example.com",
            "password": "password"
        }, headers=headers)

        json = response.json

        # assert status code
        assert response.status_code in [200, 201]
        # asset token is present
        assert "token" in json

