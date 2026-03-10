class Config():
    DEBUG =False
    SQLALCHEMY_TRACK_MODIFICATIONS =False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 60

class LocalDevelopmentConfig(Config):
    DEBUG =True
    SQLALCHEMY_DATABASE_URI = "sqlite:///optimus.sqlite3"
    JWT_SECRET_KEY ="keep this secret"
