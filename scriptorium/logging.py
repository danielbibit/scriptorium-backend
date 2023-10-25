import logging

from scriptorium.config import config

LOG_FORMAT_DEBUG = "%(levelname)s: %(pathname)s - %(funcName)s:%(lineno)d - %(message)s"


def configure_logging():
    log_level = config.LOG_LEVEL

    if log_level == "DEBUG":
        logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=log_level)
