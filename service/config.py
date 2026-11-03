"""Configuration for the Accounts service"""
import os

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///development.db")
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
