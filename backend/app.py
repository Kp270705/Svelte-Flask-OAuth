from flask import Flask, redirect, request, jsonify, session, url_for
from flask_cors import CORS
import requests
import os
import json
from urllib.parse import urlencode
from getPass import password1,password2

app = Flask(__name__)
app.secret_key = 'your-secret-key'
CORS(app, supports_credentials=True)

CLIENT_ID = password1
CLIENT_SECRET = password2
REDIRECT_URI = "http://localhost:5000/callback"

GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/login")
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

@app.route("/callback")
def callback():
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

    userinfo_endpoint = google_cfg["userinfo_endpoint"]
    userinfo_response = requests.get(userinfo_endpoint, headers={
        "Authorization": f"Bearer {access_token}"
    })

    userinfo = userinfo_response.json()
    session['user'] = userinfo

    # return the info or redirect to Svelte
    return redirect(f"http://localhost:5173/?email={userinfo['email']}&name={userinfo['name']}")

@app.route("/profile")
def profile():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify(session["user"])
