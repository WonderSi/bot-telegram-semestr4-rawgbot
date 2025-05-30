import os
import logging
from typing import Dict

class UserDialogLogger():
    def __init__(self, logs_dir: str = "logs"):
        self.logs_dir = logs_dir
        self.loggers: Dict[int, logging.Logger] = {}

        if os.path.exists(logs_dir):
            os.makedirs(logs_dir)
    
    def get_user_logger(self, user_id: int):
        if user_id not in self.loggers:
            os.makedirs(self.logs_dir, exist_ok=True)
            
            logger = logging.getLogger(f"user_{user_id}")
            logger.setLevel(logging.INFO)

            file_handler = logging.FileHandler(
                f"{self.logs_dir}/{user_id}.log", 
                encoding='utf-8'
            )

            formatter = logging.Formatter(
                '%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.propagate = False

            self.loggers[user_id] = logger

        return self.loggers[user_id]
    
    def log_user_message(self, user_id: int, username: str, message: str):
        logger = self.get_user_logger(user_id)
        logger.info(f"USER @{username}: {message}")

    def log_bot_messag(self, user_id: int, response: str):
        logger = self.get_user_logger(user_id)
        logger.info(f"BOT: {response}")

dialog_logger = UserDialogLogger()
