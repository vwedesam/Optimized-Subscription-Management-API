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
    1. Register user -  POST `/api/auth/register-user` | PAYLOAD - `{ 'last_name', 'first_name', 'email', 'password' }`
    2. login - POST `/api/auth/login` | PAYLOAD - `{ 'email', 'password' }`
2. Plan
    1. List plans - GET `/api/plans`
    2. Create subscription plan - POST `/api/plans` | PAYLOAD - `{ 'name', 'price' }`
3. Subscription (`Require Authentication - Bearer {token}`)
    1. Retrieve subscription history - GET `/api/subscriptions` | Query(optional) - `{ 'per_page', 'last_seen_id' }`
    2. Create new subscription - POST `/api/subscriptions` | PAYLOAD - `{ 'plan_id' }`
    3. Get auth user active subscription - GET `/api/subscriptions/active`
    4. Upgrade subscription - PUT `/api/subscriptions/upgrade` | PAYLOAD - `{ 'plan_id' }`
    5. Cancel active subscription - PATCH `/api/subscriptions/cancel`

> **Note**:
>
> * Subscription plans assume a **monthly billing model**, not annual.
> * `start_date` and `end_date` are **automatically set** for a 30-day period.
> * A `user` can only have **one active subscription** at a time.
---
### Authentication
1. **Login** with `email` and `password` via:
```
POST /api/auth/login
```
2. You’ll get a **JWT token** in the response.
3. Use the token in the `Authorization` header for all subscription endpoints:
```
Authorization: Bearer <token>
```
---

### Model Definition
- **User**(`id`=int, `email`=str, `first_name`=str, `last_name`=str, `password_hash`=str, `created_at`=datetime)
- **Plan**(`id`=int, `name`=str, `price`=str, `created_at`=datetime)
- **Subscription**(`id`=int, `name`=str, `price`=str, `start_date`=datetime, `end_date`=datetime, `is_active`=bool, `plan_id`=str, `user_id`=str, `created_at`=datetime)

### Optimization Documentation

1. **Table Denormalization**

   * The `subscriptions` table is made self-sufficient by including the `name` and `price` columns.
   * With these columns present, querying for an active subscription doesn't require any expensive join—just one record with all the necessary details is returned.

2. **Table Indexes**

   * `idx_user_id_created_at (user_id, created_at DESC)`
     → Used when retrieving subscription history.

3. **Query Optimization**

   1. **Retrieving subscription history:** 
    * After careful analysis, I decided **not** to use `OFFSET` for pagination since it prevents MySQL from using the (`user_id, created_at DESC`) index efficiently.
    * Instead, I used the **cursor-based pattern**, which allows the index to be fully utilized.

   **Optimized Query Used**
   ```sql
   SELECT *
   FROM subscriptions
   WHERE user_id = :user_id
     AND id < :last_seen_id
   ORDER BY created_at DESC
   LIMIT :limit
   ```



