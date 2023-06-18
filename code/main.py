# coding=utf-8
from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from common.logger import init_logger


def create_app(name):
    app = Flask(__name__)

    app.logger = init_logger(name)
    return app
