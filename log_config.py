import logging.config


def setup_logging(verbose=False, quiet=False, log_to_file=False):
    if quiet:
        level = "ERROR"
    elif verbose:
        level = "DEBUG"
    else:
        level = "INFO"

    handlers = ["console"]
    if log_to_file:
        handlers.append("file")

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s [%(levelname)s] %(message)s"}
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.FileHandler",
                "level": level,
                "formatter": "standard",
                "filename": "organize.log",
                "mode": "a",
            },
        },
        "root": {"level": level, "handlers": handlers},
    }

    logging.config.dictConfig(LOGGING_CONFIG)
