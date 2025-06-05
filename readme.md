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

### Project Structure

```sh
|_ apis
|_ core
|_ migrations
|_ test
|_ app.py
|_ ....
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

### To initialize the database:

```sh
$ flask db init # This will add a migrations folder to your application

$ flask db migrate -m "Initial migration."  # generate an initial migration

$ flask db upgrade # apply the changes to DB
```

### Seed Db
```sh
python seed.py
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
3. Use the token in the `Authorization` header for all `subscription` endpoints:
```
Content-Type: application/json
Authorization: Bearer <token>
```
---

### Model Definition
- **User**(`id`=int, `email`=str, `first_name`=str, `last_name`=str, `password_hash`=str, `created_at`=int)
- **Plan**(`id`=int, `name`=str, `price`=str, `created_at`=int)
- **Subscription**(`id`=int, `name`=str, `price`=str, `start_date`=int, `end_date`=int, `is_active`=bool, `plan_id`=str, `user_id`=str, `created_at`=int)

### Optimization Documentation

1. **Table Denormalization**

   * The `subscriptions` table is made self-sufficient by including the `name` and `price` columns.
   * With these columns present, querying for an active subscription doesn't require any expensive join—just one record with all the necessary details is returned.

2. **Table Indexes**

    * **idx_user_id_is_active_end_date_created_at**(`user_id`, `is_active`, `end_date`, `created_at DESC`)
    -> Used for retrieving active subscription

    * **idx_user_id_created_at_desc**(`user_id`, `created_at DESC`)
    -> Used when retrieving subscription history.

3. **Optimizing Date Indexing with Timestamps**

    * Because of how MySQL handles time and date values, index with columns `created_at, end_date` didn’t work well — so I used an `Integer/unix` timestamp instead for those columns for better performance.

4. **Query Optimization**

   1. **Retrieving subscription history:** 
    * I decided **not** to use `OFFSET` for pagination since it prevents MySQL from using index efficiently.
    * Instead, I used the **cursor-based pattern**, which allows the index to be fully utilized.

   **Optimized retrieving subscription history query**
   ```sql
   SELECT *
   FROM subscriptions
   WHERE user_id = :user_id
     AND id < :last_seen_id
   ORDER BY created_at DESC
   LIMIT :limit
   ```
   >Note: whenever `id` is present in a query `mysql` prioritize `PRIMARY` index
   2. **Retrieve Active subscription:** 
    * The query fetches the most recent active subscription for a user, ensuring it is currently valid (`is_active` = `TRUE` and `end_date` > now(millisecond/unix timestamp)).

    * It uses the (`user_id`, `is_active`, `end_date`, `created_at DESC`) composite index to efficiently filter and order results, avoiding full table scans.

   **Optimized retrieve active subscription query**
   ```sql
    SELECT *
    FROM subscriptions
    WHERE user_id = :user_id
    AND is_active = TRUE
    AND end_date > :now
    ORDER BY created_at DESC
    LIMIT 1
   ```

### **Optimized Index and Query Strategy**

To support both active subscription retrieval and subscription history pagination, i use composite indexes that align with the query filters and sort order.

The index `idx_user_id_is_active_end_date_created_at` is designed for filtering active subscriptions efficiently, while `idx_user_id_created_at_desc` supports history lookups with cursor-based pagination.

Thanks to **MySQL's leftmost prefix rule**, each index remains flexible—queries can still benefit from any leftmost combination of the indexed columns.

MySQL’s query planner automatically picks the most efficient index based on the query structure and data, making these indexes interchangeable depending on the path being queried.

For performance-critical paths, raw SQL is used to fully leverage index order and avoid `OFFSET`

### Other Queries
All other queries are optimized:
- Getting a plan by `ID` uses the `primary index`.
- Looking up a user by `email` also uses the `primary` or `unique index`.
- Subscription lookups by `ID` use the `primary index` as well.
