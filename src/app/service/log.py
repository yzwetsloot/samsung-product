import logging
import os
from logging.handlers import RotatingFileHandler

from app import config


# get current directory name
current_directory = os.path.basename(os.getcwd())

# create formatter
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

# create file handler
file_handler = RotatingFileHandler(
    filename=config.log_path,
    maxBytes=config.log_max_size,
    backupCount=config.log_backup_count,
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# create logger
logger = logging.getLogger(current_directory)
logger.setLevel(config.log_level)
logger.addHandler(file_handler)

# console handler
if config.environment == "dev":
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(console_handler)
