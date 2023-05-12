from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask_smorest import abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from stores.extensions.auth import BLOCKLIST
from stores.extensions.database import UserModel
from stores.extensions.database import db
from stores.extensions.schemas import UserSchema


blp = Blueprint("users", __name__, description="User operations")


@blp.route("/register")
class UserRegister(MethodView):
    """User register endpoint methods"""

    @blp.arguments(UserSchema)
    @blp.response(201)
    def post(self, data):
        """Register an user in database"""
        data["password"] = pbkdf2_sha256.hash(data["password"])

        user = UserModel(**data)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Username already exists")
        except SQLAlchemyError as error:
            abort(500, message=f"Error {error} while inserting product to database")

        return jsonify(message=f"User {data['username']} created")


@blp.route("/login")
class UserLogin(MethodView):
    """User login endpoint methods"""

    @blp.arguments(UserSchema)
    @blp.response(200)
    def post(self, data):
        """Retrive an access token to given user if registered"""
        user = UserModel.query.filter(UserModel.username == data["username"]).first()

        if not user:
            abort(404, message="User not found")

        if not pbkdf2_sha256.verify(data["password"], user.password):
            abort(401, message="Invalid credentials")

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)


@blp.route("/logout")
class UserLogout(MethodView):
    """User logout endpoint"""

    @jwt_required()
    @blp.response(200)
    def post(self):
        """Logout the user with given data/ID"""
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return jsonify(message="Successful logout")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    """Refresh current access token"""

    @jwt_required(refresh=True)
    @blp.response(200)
    def post(self, access_token):
        """Create a non-fresh token when the given access token expires"""
        current = get_jwt_identity()
        new_token = create_access_token(identity=current.id, fresh=False)
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return jsonify(access_token=new_token)


@blp.route("/user/<int:id>")
class User(MethodView):
    """User information endpoint methods"""

    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, id):
        """Retrieve user content from database by ID"""
        user = UserModel.query.get_or_404(id)
        return user

    @jwt_required(fresh=True)
    @blp.response(204)
    def delete(self, id):
        """Delete an user from database by ID"""
        user = UserModel.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
