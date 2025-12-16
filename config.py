import os

class Config:
    SECRET_KEY = 'dev-secret-key-12345'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'

