# coding=utf-8
from logging import Logger
import logging
from logging.handlers import RotatingFileHandler
import sys
_logger: Logger = logging.getLogger()


def init_logger(name, debug=False) -> Logger:
    global _logger
    if debug:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        root.addHandler(handler)
    return _logger


def get_logger() -> Logger:
    global _logger
    return _logger
