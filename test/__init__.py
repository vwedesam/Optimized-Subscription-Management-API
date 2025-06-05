import flask_unittest
import subprocess
from app import app as flask_app
from core.extensions import db
from config import config_by_env
from datetime import datetime
from sqlalchemy import text

headers= { "Content-Type": "application/json"}

class PerformanceQueryTest(flask_unittest.ClientTestCase):

    app = flask_app
    app.config.from_object(config_by_env['test'])

    def setUp(self, client):
        with self.app.app_context():
            db.create_all()
            # Run your seed script to populate the test database
            subprocess.run(["python", "seed.py"], check=True)

    def tearDown(self, client):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_active_subscription_query_performance(self, client):

        user_id = 1
        now = int(datetime.now().timestamp())
        sql = text("""
            SELECT *
            FROM subscriptions
            WHERE user_id = :user_id
            AND is_active = TRUE
            AND end_date > :now
            ORDER BY created_at DESC
            LIMIT 1
        """)

        with self.app.app_context():

            start = datetime.now().timestamp()

            result = db.session.execute(sql, {"user_id": user_id, "now": now}).first()

            duration = datetime.now().timestamp() - start

            print(f"[Performance Test - active_subscription] Query duration: {duration:.6f}(s)")
            assert result is not None
            assert duration < 0.1


    def test_subscription_history_performance(self, client):

        user_id = 1
        sql = text("""
            SELECT id, name, price, created_at
            FROM subscriptions
            WHERE user_id = :user_id
            ORDER BY created_at DESC
            LIMIT 10
        """)

        with self.app.app_context():

            start = datetime.now().timestamp()

            result = db.session.execute(sql, {"user_id": user_id}).first()

            duration = datetime.now().timestamp() - start

            print(f"[Performance Test - subscription_history] Query duration: {duration:.6f}(s)")
            assert result is not None
            assert duration < 0.1


    def test_index_usage_in_active_subscription(self, client):
        now = datetime.now().timestamp()
        sql = f"EXPLAIN SELECT * FROM subscriptions WHERE user_id = 1 AND is_active = TRUE AND end_date > {now} ORDER BY created_at DESC LIMIT 1"

        with self.app.app_context():
            result = db.session.execute(text(sql)).all()
            print(f"EXPLAIN Output: {result}")
            assert any("idx_user_id_is_active_end_date_created_at" in str(row) for row in result)
            assert any("Using index" in str(row) for row in result)

    def test_index_usage_in_subscription_history(self, client):
        sql = f"EXPLAIN SELECT * FROM subscriptions WHERE user_id = 1 ORDER BY created_at DESC LIMIT 10"

        with self.app.app_context():
            result = db.session.execute(text(sql)).all()
            print(f"EXPLAIN Output: {result}")
            assert any("idx_user_id_created_at_desc" in str(row) for row in result)
            assert any("Using index" in str(row) for row in result)


