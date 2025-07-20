from initResources.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.Integer, unique=True, nullable=False)
    username = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    authorizedPicturepath = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    email_varified = db.Column(db.String(7), nullable=False)


    def __init__(self, sub_id, username, first_name, last_name, authorizedPicturepath, email, email_varified):
        self.sub_id = sub_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.authorizedPicturepath = authorizedPicturepath
        self.email = email
        self.email_varified = email_varified