from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# declare flask app packages
db = SQLAlchemy()
migrate = Migrate()
flask_bcrypt = Bcrypt()
