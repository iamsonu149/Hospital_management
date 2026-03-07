from flask_jwt_extended import JWTManager
from application.model import User

jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup_callback(__jwt_header,jwt_data):
    user_id = int(jwt_data['sub'])
    return User.query.get(user_id)
