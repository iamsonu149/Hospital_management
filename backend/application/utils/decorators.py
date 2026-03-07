from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.model import User


def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user =User.query.get(user_id)

            if not user:
                return jsonify(message="User not found"), 401
            if user.status =="blocked":
                return jsonify(message="your account is blocked"),403

            if user.role!=required_role:
                return jsonify(message="You are not authorized"), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper
