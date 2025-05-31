from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# declare flask app packages
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
flask_bcrypt = Bcrypt()
jwt = JWTManager()
