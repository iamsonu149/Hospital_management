from flask import request,jsonify
from flask_jwt_extended import create_access_token
from application.model import User
from application.database import db
from . import auth_bp
from werkzeug.security import generate_password_hash,check_password_hash



@auth_bp.route('/registration',methods=['POST'])
def registration():
    data= request.get_json()
    email = data.get('email')
    name = data.get('name')
    password = data.get('password')
    if not email or not name or not password:
        return jsonify({'message':'Missing required fields'}),400
    existing_user =User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message':"User already exists"}),409
    hashed_password =generate_password_hash(password)
    new_user=User(email=email,name=name,password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'User registered successfully'}),201


@auth_bp.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'message':'one of the field is empty'}),400
    user= User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password,password):
        return jsonify({'message':"Invalid credintial"}),401
    if user.status=='blocked':
        return jsonify({"message":"Your account has been blocked"}),403
    token=create_access_token(identity=str(user.id))
    return jsonify({'token':token,'role':user.role,'name':user.name}),200
   


