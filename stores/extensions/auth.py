from flask import jsonify
from flask_jwt_extended import JWTManager


BLOCKLIST = set()


def init_app(app):
    """Set authentication config on API"""
    jwt = JWTManager(app)
    jwt_configuration(jwt)


def jwt_configuration(jwt):
    """Handle access token problems"""

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(header, payload):
        return jsonify(description="The access token is not fresh"), 401

    @jwt.token_in_blocklist_loader
    def token_blocklist_check(header, payload):
        """Check if access token is in blocklist"""
        return payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(header, payload):
        return jsonify(message="The access token has been revoked", error="token_revoked"), 401

    @jwt.expired_token_loader
    def expired_token_callback(header, payload):
        """Raise an error when access token is expired"""
        return jsonify(message="The access token expired", error="token_expired"), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        """Raise an error when access token is not valid by signature"""
        return jsonify(message="Token validation failed", error="invalid_token"), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        """Raise an error when access token is missing"""
        return jsonify(message="Missing access token header", error="auth_required"), 401
