from datetime import datetime, timedelta
from app import app, db
from models import User, Plan, Subscription
import random

with app.app_context():
    # Optional: Reset tables
    db.drop_all()
    db.create_all()

    # 1. Seed Plans
    free_plan = Plan(name="Free", price=0, created_at=int(datetime.now().timestamp()))
    premium_plan = Plan(name="Premium", price=200, created_at=int(datetime.now().timestamp()))
    db.session.add_all([free_plan, premium_plan])
    db.session.commit()

    # 2. Seed User
    user = User(last_name="samuel", first_name="vwede", email="samuel@vwede.com", password="password", created_at=int(datetime.now().timestamp()))
    db.session.add(user)
    db.session.commit()

    # Seed 5000 Subscriptions
    subscriptions = []
    for i in range(1, 5000):
        plan = random.choice([free_plan, premium_plan])
        days_ago = 5001 - i # generate data in ascending order

        start_date = (datetime.now() - timedelta(days=days_ago))
        end_date = start_date + timedelta(days=30)

        start_date = int(start_date.timestamp())
        end_date = int(end_date.timestamp())
        is_active = int(end_date > datetime.now().timestamp())

        sub = Subscription(
            name=plan.name,
            price=plan.price,
            user_id=user.id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date,
            created_at=start_date,
            is_active=is_active
        )
        subscriptions.append(sub)
    db.session.add_all(subscriptions)
    db.session.commit()

    print("✅ Database seeded successfully!")
