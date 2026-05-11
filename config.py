class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///car_shop.db'
    DEBUG = True

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'