from flask import Blueprint, make_response, jsonify, session, request, redirect
from flask_jwt_extended import create_access_token
import requests
from urllib.parse import urlencode

from scripting.getPass import password1,password2
from models.models import User
from initResources.db import db


# Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# Constants for Google OAuth
CLIENT_ID = password1
CLIENT_SECRET = password2
REDIRECT_URI = "http://localhost:5000/auth/callback"
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"


# used for fetching Google OAuth configuration
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# used for logging out the user
@auth_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


# used for Google OAuth login
@auth_bp.route("/login")
def login():
    google_cfg = get_google_provider_cfg()
    auth_endpoint = google_cfg["authorization_endpoint"]

    request_uri = auth_endpoint + "?" + urlencode({
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid email profile",
        "response_type": "code",
        "prompt": "consent",
    })
    print(f"r\n\n\trequest uri is: {request_uri}")
    return redirect(request_uri)


# use to handle the callback from Google after user authentication
@auth_bp.route("/callback")
def callback():
    print(f"In callback")
    code = request.args.get("code")

    google_cfg = get_google_provider_cfg()
    token_endpoint = google_cfg["token_endpoint"]

    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_endpoint, data=token_data)
    token_json = token_response.json()
    access_token = token_json["access_token"]
    print(f"\tGoogle access token: {access_token}")

    userinfo_endpoint = google_cfg["userinfo_endpoint"]
    userinfo_response = requests.get(userinfo_endpoint, headers={
        "Authorization": f"Bearer {access_token}"
    })

    userinfo = userinfo_response.json()
    session['user'] = userinfo

    # here I get user info
    sub_id = userinfo['sub']
    name = userinfo['name']
    given_name = userinfo['given_name']
    family_name = userinfo['family_name']
    picture_path = userinfo['picture']
    email = userinfo['email']
    email_verified = userinfo['email_verified']

    if not name or not sub_id:
        return {'message': "Username or password missing"}, 400
        
    if User.query.filter_by(username=name).first():
        return {'message':"User already exists"}, 400
    
    new_user = User(sub_id, name, given_name, family_name, picture_path, email, email_verified)
    db.session.add(new_user)
    db.session.commit()

    # creating access token for the user
    jwt_access_token = create_access_token(identity=str(new_user.sub_id))
    print(f"\tJWT access token created: {jwt_access_token}")

    # Store JWT in cookie
    response = make_response(redirect(f"http://localhost:5173/?email={userinfo['email']}&name={userinfo['name']}"))
    response.set_cookie("jwt_token", jwt_access_token, httponly=False)  # httponly=False so JS can read it
    return response


# used to send the JWT token to the frontend
@auth_bp.route("/token")
def send_token_to_frontend():
    token = request.cookies.get("jwt_token")
    if not token:
        return jsonify({"msg": "No token"}), 401
    return jsonify(access_token=token)


# use to fetch profile information
@auth_bp.route("/profile")
def profile():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(session["user"])
