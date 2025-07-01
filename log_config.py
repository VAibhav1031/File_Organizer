import logging
import logging.config
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)


# we have imported the logging.Formatter  class from logging and  added the basic new functionality
# ther is override happening in the default format() function which was
# we used super() so that rest of the part of the format function of Formatter class will be used in it ,  so that
# our formatting of other thing  will work
class ColorFormatter(logging.Formatter):
    COLOR_MAP = {
        "DEBUG": Fore.CYAN + "[DEBUG]" + Style.RESET_ALL,
        "INFO": Fore.GREEN + Style.BRIGHT + "[INFO]" + Style.RESET_ALL,
        "WARNING": Fore.YELLOW + "[WARNING]" + Style.RESET_ALL,
        "ERROR": Fore.RED + "[ERROR]" + Style.RESET_ALL,
        "CRITICAL": Fore.RED + Style.BRIGHT + "[CRITICAL]" + Style.RESET_ALL,
    }

    def format(self, record):
        level_name = record.levelname
        if level_name in self.COLOR_MAP:
            level_color = self.COLOR_MAP[level_name]
            record.levelname = level_color
        return super().format(record)


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
            "colored": {
                "()": ColorFormatter,
                "format": "%(asctime)s %(levelname)s %(message)s",
            },
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": level,
                "formatter": "colored",
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
