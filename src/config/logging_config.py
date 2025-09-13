import logging
import datetime
import os
from logging.handlers import TimedRotatingFileHandler

log_directory = "./src/logs/"
# Create the logs directory if it doesn't exist
if not os.path.exists(log_directory):
    os.makedirs(log_directory)


for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

# Set the logging level for the root logger
logging.root.setLevel(logging.INFO)

# Create a formatter for log messages
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


file_handler = TimedRotatingFileHandler(
    os.path.join(log_directory, "app.log"),
    when="midnight",
    interval=1,
    backupCount=30,
    encoding="utf-8",
)
file_handler.setFormatter(formatter)
logging.root.addHandler(file_handler)
