from flask import Flask
from flask_cors import CORS
from application.config import LocalDevelopmentConfig
from application.database import db
from application.security import jwt
from application.initializers import create_default_admin

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    # In WSL/browser setups, frontend may be opened via localhost or 127.0.0.1.
    allowed_origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    CORS(app, resources={r"/*": {"origins": allowed_origins}})

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        create_default_admin()

    from application.auth import auth_bp
    from application.admin import admin_bp
    from application.doctor import doctor_bp
    from application.patient import patient_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)

    return app
