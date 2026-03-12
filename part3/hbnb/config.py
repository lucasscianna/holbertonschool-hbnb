import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'hbnb_super_secret_key_2026_secure_length_32_chars')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'hbnb_jwt_extra_long_secret_key_for_security_reasons')
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///development.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}