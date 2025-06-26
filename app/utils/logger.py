import os
import logging

log_path = os.path.join(os.getcwd(), "logs")
os.makedirs(log_path, exist_ok=True)

logger = logging.getLogger("currency_manager")
logger.setLevel(logging.DEBUG)

info_handler = logging.FileHandler(os.path.join(log_path, "info.log"), encoding="utf-8")
info_handler.setLevel(logging.INFO)
info_formatter = logging.Formatter("[INFO] %(asctime)s - %(message)s")
info_handler.setFormatter(info_formatter)

warning_handler = logging.FileHandler(os.path.join(log_path, "warning.log"), encoding="utf-8")
warning_handler.setLevel(logging.WARNING)
warning_formatter = logging.Formatter("[WARNING] %(asctime)s - %(message)s")
warning_handler.setFormatter(warning_formatter)

error_handler = logging.FileHandler(os.path.join(log_path, "error.log"), encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_formatter = logging.Formatter("[ERROR] %(asctime)s - %(message)s")
error_handler.setFormatter(error_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("[CONSOLE] %(asctime)s - %(message)s"))

logger.addHandler(info_handler)
logger.addHandler(warning_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)

logger.propagate = False