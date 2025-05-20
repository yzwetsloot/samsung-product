import os

from dotenv import load_dotenv

load_dotenv()


# database configuration
database = {
    "user": os.environ["DATABASE_USER"],
    "password": os.environ["DATABASE_PASSWORD"],
    "host": os.environ["DATABASE_HOST"],
    "port": os.environ["DATABASE_PORT"],
    "database": os.environ["DATABASE_NAME"],
}


categories = [
    "01000000",  # Smartphones, Tablets, Watches, Audio/Sound & Accessoires
    "03000000",  # Computers
    "04000000",  # TV
    "05000000",  # AV
    "07000000",  # Monitors
    "08000000",  # Home appliances
    "09000000",  # Memory & Storage
]

# logging configuration
log_level = os.environ.get("LOG_LEVEL", "INFO")
log_path = os.environ.get("LOG_PATH", "app.log")
log_max_size = int(os.environ.get("LOG_MAX_SIZE", 100_000_000))
log_backup_count = int(os.environ.get("LOG_BACKUP_COUNT", 2))

# miscellaneous
environment = os.environ.get("ENVIRONMENT", "dev")

timeout = int(os.environ.get("TIMEOUT", 10))
