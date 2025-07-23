from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from initResources.db import db
from models.models import User
from initResources.jwt import jwt
from resources.routes import resources_bp, register_jwt_error_handlers
from authentication import auth_bp
from scripting.genString import generate_random_string
from scripting.initialiseValues import jwt_time_period as jwt_period


def create_app():
    pass

    app = Flask(__name__)
    app.secret_key = generate_random_string(32)
    app.config['JWT_SECRET_KEY'] = generate_random_string(32)

    jwt_time_period = jwt_period

    if "seconds" in jwt_time_period:
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=int(jwt_time_period.split()[0]))
    elif "minutes" in jwt_time_period:
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=int(jwt_time_period.split()[0]))
    elif "hours" in jwt_time_period:
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=int(jwt_time_period.split()[0]))
    elif "days" in jwt_time_period:
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=int(jwt_time_period.split()[0]))
    else:
        raise ValueError("Invalid JWT time period format. Use 'seconds', 'minutes', 'hours', or 'days'.")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

    CORS(app,
     supports_credentials=True,
     origins=["http://localhost:5173"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"])
    

    # initialize db :
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # initialize jwt manager
    jwt.init_app(app)
    # register JWT error handlers
    register_jwt_error_handlers()

    # register authentication blueprint
    app.register_blueprint(auth_bp)
    # register resources blueprint
    app.register_blueprint(resources_bp)


    return app

if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)

