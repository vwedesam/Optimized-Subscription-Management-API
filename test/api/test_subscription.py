import flask_unittest
from app import app as flask_app
from core.extensions import db
from config import config_by_env

headers= { "Content-Type": "application/json"}

class SubscriptionTest(flask_unittest.ClientTestCase):

    app = flask_app
    app.config.from_object(config_by_env['test'])

    def setUp(self, client):
        with self.app.app_context():
            db.create_all()

    def tearDown(self, client):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def create_plan(self, client, name="Free", price="200"):
        response = client.post("/api/plans", json={
            "name": name,
            "price": price
        }, headers=headers)

    def login_user(self, client):

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
        return json.get('token')

    def test_create_subscription_required_auth_token(self, client):

        response = client.post("/api/subscriptions", json={}, headers=headers)

        json = response.json
        # assert status code
        assert response.status_code == 401
        assert "msg" in json
        assert json.get('msg') == 'Missing Authorization Header'

    def test_create_subscription_required_field(self, client):

        token = self.login_user(client)

        response = client.post("/api/subscriptions", json={}, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json
        # assert status code
        assert response.status_code == 422
        assert "errors" in json
        # asset the errors return contains required field error 
        assert "plan_id" in json.get('errors')


    def test_create_subscription(self, client):

        token = self.login_user(client)
        self.create_plan(client)
        plan_id = 1

        response = client.post("/api/subscriptions", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json
        # assert status code
        assert response.status_code == 200
        # asset subscription model fields are present
        assert "id" in json
        assert "name" in json
        assert "price" in json
        assert "user_id" in json
        assert "plan_id" in json
        assert "start_date" in json
        assert "end_date" in json
        assert "is_active" in json
        assert "created_at" in json
        assert json.get("plan_id") == str(plan_id)


    def test_list_subscription(self, client):

        token = self.login_user(client)
        self.create_plan(client)
        plan_id = 1

        response = client.post("/api/subscriptions", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        response = client.get("/api/subscriptions", json={}, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json
        # assert status code
        assert response.status_code == 200
        assert "next_cursor_id" in json
        assert "per_page" in json
        data = json.get('data')
        assert len(data) == 1
        # asset subscription model fields are present
        assert "id" in data[0]
        assert "name" in data[0]
        assert "price" in data[0]
        assert "user_id" in data[0]
        assert "plan_id" in data[0]
        assert "start_date" in data[0]
        assert "end_date" in data[0]
        assert "is_active" in data[0]
        assert "created_at" in data[0]


    def test_active_subscription(self, client):

        token = self.login_user(client)
        self.create_plan(client)
        plan_id = 1

        response = client.post("/api/subscriptions", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        response = client.get("/api/subscriptions/active", json={}, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json
        # assert status code
        assert response.status_code == 200
        # asset subscription model fields are present
        assert "id" in json
        assert "name" in json
        assert "price" in json
        assert "user_id" in json
        assert "plan_id" in json
        assert "start_date" in json
        assert "end_date" in json
        assert "is_active" in json
        assert "created_at" in json

    def test_cancel_subscription(self, client):

        token = self.login_user(client)
        self.create_plan(client)
        plan_id = 1

        response = client.post("/api/subscriptions", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        response = client.patch("/api/subscriptions/cancel", json={}, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json
        # assert status code
        assert response.status_code in [200, 201]
        assert "success" in json
        assert json.get("success") == "ok"


    def test_upgrade_subscription_existing_plan(self, client):

        token = self.login_user(client)
        self.create_plan(client)
        plan_id = 1

        response = client.post("/api/subscriptions", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        response = client.put("/api/subscriptions/upgrade", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json
        # assert status code
        assert response.status_code == 400
        assert "error" in json
        assert json.get("error") == "You're already on this subscription plan. Please select a different plan to upgrade."
    

    def test_upgrade_subscription(self, client):

        token = self.login_user(client)
        self.create_plan(client)
        self.create_plan(client, name="Basic", price="560")
        plan_id = 1
        plan_id2 = 2

        response = client.post("/api/subscriptions", json={
            "plan_id": str(plan_id)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        response = client.put("/api/subscriptions/upgrade", json={
            "plan_id": str(plan_id2)
        }, headers={
            **headers,
            "authorization": "Bearer "+ token
        })

        json = response.json

        # assert status code
        assert response.status_code in [200, 201]
        # asset subscription model fields are present
        assert "id" in json
        assert "name" in json
        assert "price" in json
        assert "user_id" in json
        assert "plan_id" in json
        assert "start_date" in json
        assert "end_date" in json
        assert "is_active" in json
        assert "created_at" in json
        # assert plan id
        assert json.get('plan_id') is not str(plan_id)
        assert json.get('plan_id') == str(plan_id2)
