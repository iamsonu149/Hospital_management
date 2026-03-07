from werkzeug.security import generate_password_hash
from application.database import db
from application.model import User

def create_default_admin():
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        db.session.add(User( name="optimus",email="admin@hospital.com",
                password=generate_password_hash("1234"),
                role="admin"
            )
        )
        db.session.commit()
