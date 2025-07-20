from flask import Flask
from flask_cors import CORS
from datetime import timedelta

from initResources.db import db
from models.models import User
from initResources.jwt import jwt
from resources.protected import resources_bp, register_jwt_error_handlers
from authentication import auth_bp
from scripting.genString import generate_random_string


def create_app():
    pass

    app = Flask(__name__)
    app.secret_key = generate_random_string(32)
    app.config['JWT_SECRET_KEY'] = generate_random_string(32)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=45)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    CORS(app, supports_credentials=True)

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

