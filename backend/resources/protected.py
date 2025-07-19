from flask import Blueprint, jsonify

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    JWTManager
)
from initResources.jwt import jwt

protected_bp = Blueprint('protected', __name__, url_prefix='/user')



# ✅ Error handler registration
def register_jwt_error_handlers():
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            "message": "⚠️ Token has expired. Please re-login.",
            "error": "token_expired"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        return jsonify({
            "message": "💔 ❌ Invalid token. Please login again.",
            "error": "invalid_token"
        }), 422

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        return jsonify({
            "message": "Authorization token missing.",
            "error": "authorization_required"
        }), 401


protected_bp.route('/protected', methods=['GET'])
@jwt_required()
def protectedRoute(self):
    current_user_id = get_jwt_identity()
    print(f"\nId get...")
    return{"message": f"You accessed protected resource", "user_id": f"User-id: {current_user_id}"}, 200

print("✅ Resources.protected loaded")