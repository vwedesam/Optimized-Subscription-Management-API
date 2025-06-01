import flask_unittest
from app import app as flask_app
from core.extensions import db
from config import config_by_env

headers= { "Content-Type": "application/json"}

class PlanTest(flask_unittest.ClientTestCase):

    app = flask_app
    app.config.from_object(config_by_env['test'])

    def setUp(self, client):
        with self.app.app_context():
            db.create_all()

    def tearDown(self, client):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_plan_required_field(self, client):

        response = client.post("/api/plans", json={}, headers=headers)

        json = response.json
        # assert status code
        assert response.status_code == 422
        assert "errors" in json
        # asset the errors return contains required field error 
        assert "name" in json.get('errors')
        assert "price" in json.get('errors')

    def test_create_plan(self, client):

        response = client.post("/api/plans", json={
            "name": "Free",
            "price": "200"
        }, headers=headers)

        json = response.json
        # assert status code
        assert response.status_code == 200
        # asset user model fields are present
        assert "name" in json
        assert "price" in json
        assert "created_at" in json


    def test_list_plans(self, client):

        response = client.post("/api/plans", json={
            "name": "Free",
            "price": "200"
        }, headers=headers)

        response = client.get("/api/plans", json={}, headers=headers)

        json = response.json
    
        assert response.status_code in [200, 201]
        assert len(json) == 1
        # asset plan model fields are present
        assert "id" in json[0]
        assert "name" in json[0]
        assert "price" in json[0]
        assert "created_at" in json[0]


