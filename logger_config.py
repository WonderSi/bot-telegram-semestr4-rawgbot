import os
import logging
from datetime import datetime

os.makedirs('logs/users', exist_ok=True)
os.makedirs('logs/system', exist_ok=True)

system_logger = logging.getLogger('bot_system')
system_logger.setLevel(logging.INFO)
system_logger.handlers.clear()

simple_format = '%(asctime)s - %(message)s'
detailed_format = '%(asctime)s - %(levelname)s - %(message)s'

console = logging.StreamHandler()
console.setFormatter(logging.Formatter(simple_format))
system_logger.addHandler(console)

today = datetime.now().strftime("%Y-%m-%d")
system_file_log = logging.FileHandler(
    f'logs/system/bot_{today}.log', encoding='utf-8')
system_file_log.setFormatter(logging.Formatter(detailed_format))
system_logger.addHandler(system_file_log)

user_loggers = {}


def get_user_logger(user_id):
    if user_id not in user_loggers:
        user_logger = logging.getLogger(f'user_{user_id}')
        user_logger.setLevel(logging.INFO)
        user_logger.handlers.clear()

        user_file_log = logging.FileHandler(
            f'logs/users/user_{user_id}_history.log',
            encoding='utf-8'
        )
        user_file_log.setFormatter(logging.Formatter(simple_format))
        user_logger.addHandler(user_file_log)

        user_loggers[user_id] = user_logger

    return user_loggers[user_id]


def log_user(user_id, username, message):
    user_logger = get_user_logger(user_id)
    user_logger.info(f"👤 Пользователь: {message}")
    system_logger.info(f"👤 Пользователь {user_id} ({username}): {message}")


def log_bot(user_id, message):
    user_logger = get_user_logger(user_id)
    user_logger.info(f"🤖 Бот: {message}")
    system_logger.info(f"🤖 Бот → {user_id}: {message}")


def log_info(message):
    system_logger.info(f"ℹ️ {message}")


def log_error(message):
    system_logger.error(f"❌ {message}")


def log_user_action(user_id, action):
    user_logger = get_user_logger(user_id)
    user_logger.info(f"🔄 Действие: {action}")
    system_logger.info(f"🔄 Пользователь {user_id} выполнил: {action}")
