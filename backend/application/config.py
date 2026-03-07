class Config():
    DEBUG =False
    SQLALCHEMY_TRACK_MODIFICATIONS =False

class LocalDevelopmentConfig(Config):
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = "sqlite:///optimus.sqlite3"
    JWT_SECRET_KEY ="keep this secret"