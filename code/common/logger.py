# coding=utf-8
from logging import Logger
import logging
from logging.handlers import RotatingFileHandler
_logger: Logger = logging.getLogger()


def init_logger(name, debug=False) -> Logger:
    global _logger
    return _logger


def get_logger() -> Logger:
    global _logger
    return _logger
