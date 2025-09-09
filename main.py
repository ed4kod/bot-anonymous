import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import register_handlers

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_bot() -> Bot:
    """Создает и возвращает экземпляр бота"""
    return Bot(token=BOT_TOKEN)


async def create_dispatcher() -> Dispatcher:
    """Создает и настраивает диспетчер"""
    return Dispatcher()


async def setup_bot():
    """Настраивает и запускает бота"""
    try:
        # Инициализация бота и диспетчера
        bot = await create_bot()
        dp = await create_dispatcher()

        # Регистрация обработчиков
        register_handlers(dp)

        # Запуск бота
        logger.info("Бот запускается...")
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
    finally:
        # Корректное завершение работы
        await bot.close()


if __name__ == "__main__":
    asyncio.run(setup_bot())
