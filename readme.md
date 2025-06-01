# Optimized Subscription Management API

A simple Flask-based optimized API for user registration, authentication, and managing subscription plans (Free, Basic, Pro). Supports subscribing, upgrading, and cancelling plans with active status tracking.

### Features

* User Registration & Authentication
* Create & List Subscription Plans
* User Subscription (Subscribe, Upgrade, Cancel)
* Active Subscription Lookup
* RESTful Endpoints with JSON responses
* Secure Password Hashing
* Optimized queries with SQLAlchemy

### Tech Stack

* Python 3.x
* Flask (Flask-SQLAlchemy)
* Flask-RESTX - Restful API
* Flask-Bcrypt - password hashing and validation
* Flask-Migrate - QLAlchemy database migrations
* SQLite or MySQL/MariaDB
* Flask-JWT-EXTENDED - API Authentication(JWT) and token management
* marshmallow(FLASK-MARSHMALLOW, MARSHMALLOW-SQLAlchemy) - validate, serialization and deserialization
* FLASK_UNITTEST - for testing

### Project Structure

```bash

```

### Installation

```bash
$ git clone git@github.com:vwedesam/Optimized-Subscription-Management-API.git
$ cd Optimized-Subscription-Management-API
$ python3 -m venv venv
$ source venv/bin/activate  # on Windows: venv\Scripts\activate
$ pip install -r requirements.txt
```

### Environment Variables (Optional)

Create a `.env` file to store sensitive config like database URL, ....

```env
FLASK_APP=app.py
FLASK_DEBUG=true
ENV=dev
DATABASE_URL=sqlite:///db.sqlite3
```

### Running the App

```bash
flask run
# or
python app.py
```

### Run Test

```bash
python -m unittest
```

To initialize the database:

```sh
$ flask db init # This will add a migrations folder to your application

$ flask db migrate -m "Initial migration."  # generate an initial migration

$ flask db upgrade # apply the changes to DB
```

### API Endpoints
1. Auth
    1. Register user -  POST `/api/auth/register-user`
    2. login - POST `/api/auth/login`
2. Plan
    1. List plans - GET `/api/plans`
    2. Create subscription plan - POST `/api/plans`
3. Subscription (`Require Authentication`)
    1. List subscriptions - GET `/api/subscriptions`
    2. Create new subscription - POST `/api/subscriptions`
    3. Get auth user active subscription - GET `/api/subscriptions/active`
    4. Upgrade subscription - PUT `/api/subscriptions/upgrade`
    5. Cancel subscription - PATCH `/api/subscriptions/cancel`

>**Note**: When creating subscription plan we assume it's a monthly subscription billing model not annually.

>`start_date` and `end_date` are automatically prefilled for a period of 30 days

> A `user` can only have one active `subscription` at a time

### Model Definition
- **User**(`id`=int, `email`=str, `first_name`=str, `last_name`=str, `password_hash`=str, `created_at`=datetime)
- **Plan**(`id`=int, `name`=str, `price`=str, `created_at`=datetime)
- **Subscription**(`id`=int, `name`=str, `price`=str, `start_date`=datetime, `end_date`=datetime, `is_active`=bool, `plan_id`=str, `user_id`=str, `created_at`=datetime)

### Optimization Documentation

1. **Table Denormalization**
    - The subscription model is made to be self sufficient by adding `plan_name` and `price` column 
    - by adding these columns, whenever an active subscription is queried, expensive joins are avoided, just one records that contains everything there is for subscription is returned

2. **Table Index**
    1. `user_id, created_at DESC` - used when retrieving list of subscription
    2. `user_id, is_active, end_date, created_at DESC` - used when retrieving active subscription
    3. `user_id, is_active` - used when retrieving active subscription to be canceled

3. **Query Optimization**




