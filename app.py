from dotenv import load_dotenv
load_dotenv()  # take environment variables

import os
from flask import Flask
from config import config_by_env
from apis import api
from core.extensions import db, flask_bcrypt, migrate

env = os.getenv('ENV') or 'dev'
flask_debug = os.getenv('FLASK_DEBUG') or False

app = Flask(__name__)
app.config.from_object(config_by_env[env])

# init packages for automatic context push
api.init_app(app)
flask_bcrypt.init_app(app)
db.init_app(app)
migrate.init_app(app)

if __name__ == '__main__':
    app.run(debug=flask_debug)

