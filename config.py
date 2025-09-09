import os
import logging
from dotenv import load_dotenv

# Настройка логирования
logger = logging.getLogger(__name__)

# Загружаем переменные окружения из .env файла
load_dotenv()


def get_env_variable(name, default=None, required=True):
    """Получает переменную окружения с проверкой"""
    value = os.getenv(name, default)
    if required and value is None:
        error_msg = f"Не найдена обязательная переменная окружения: {name}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    return value


# Получаем данные из переменных окружения
BOT_TOKEN = get_env_variable("BOT_TOKEN")
ADMIN_ID = int(get_env_variable("ADMIN_ID"))
