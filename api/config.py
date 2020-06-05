#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ, path
from dotenv import load_dotenv


base_directory = path.abspath(path.dirname(__file__))
load_dotenv(path.join(base_directory, ".env"))


class BaseConfig(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    CORS_HEADERS = "Content-Type"
    CELERY_BROKER_URL = "redis://localhost:6379"
    CELERY_RESULT_BACKEND = "redis://localhost:6379"


class ProdConfig(BaseConfig):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(BaseConfig):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True
