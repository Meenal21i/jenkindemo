import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

log_file = "..//app.log"

console_handler = logging.StreamHandler()
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
formatter_file = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter_file)
logger.addHandler(console_handler)
logger.addHandler(file_handler)