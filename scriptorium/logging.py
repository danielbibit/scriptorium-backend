import logging

from scriptorium.config import config

LOG_FORMAT_DEBUG = "%(levelname)s: %(pathname)s:%(lineno)d - %(funcName)s - %(message)s"


def configure_logging():
    log_level = config.LOG_LEVEL

    logger = logging.getLogger("scriptorium")
    logger.setLevel(log_level)

    formatter = logging.Formatter(LOG_FORMAT_DEBUG)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(log_level)
    consoleHandler.setFormatter(formatter)

    logger.addHandler(consoleHandler)

    if config.ENVIRONMENT == "development":
        fileHandler = logging.FileHandler("scriptorium.log")
        fileHandler.setLevel(log_level)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    # logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG, force=True)


def get_logger() -> logging.Logger:
    """
    Returns the logger for the application.
    """
    return logging.getLogger("scriptorium")
