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
* Flask (Flask-SQLAlchemy, Flask-RESTPlus, Flask_Script, )
* Flask-Bcrypt for password hashing and validation
* SQLite or MySQL/MariaDB


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
DATABASE_URL=sqlite:///db.sqlite3
```

### Running the App

```bash
flask run
# or
python app.py
```

To initialize the database:

```python

```

## API Documentation
Swagger UI available at:

```bash
http://localhost:5000/apidocs
```

### API Endpoints

.....


### Query Optimization Documentation






