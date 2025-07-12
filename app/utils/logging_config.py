# app/utils/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../logs/app.log")

# Create logs folder if it doesn't exist
os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s:%(lineno)d] %(message)s",
    handlers=[
        RotatingFileHandler(LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("app")
