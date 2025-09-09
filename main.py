import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем данные из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Проверяем, что переменные загружены
if not BOT_TOKEN:
    raise ValueError("Не найден BOT_TOKEN в переменных окружения")
if not ADMIN_ID:
    raise ValueError("Не найден ADMIN_ID в переменных окружения")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Здравствуйте! Я бот-помощник. Опишите вашу проблему или вопрос, и я передам его сотруднику.")


# Обработчик всех сообщений от пользователей
@dp.message()
async def forward_to_admin(message: types.Message):
    user = message.from_user

    # Формируем информацию о пользователе
    user_info = f"""
📨 Новое сообщение от пользователя:

🆔 ID: {user.id}
👤 Имя: {user.first_name}
📛 Фамилия: {user.last_name or 'не указана'}
🔖 Username: @{user.username or 'не указан'}
    """

    try:
        # Пересылаем сообщение админу с информацией о пользователе
        if message.text:
            await bot.send_message(ADMIN_ID, f"{user_info}\n💬 Сообщение: {message.text}")
        elif message.photo:
            await bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=user_info)
        elif message.document:
            await bot.send_document(ADMIN_ID, message.document.file_id, caption=user_info)

        # Подтверждаем пользователю, что сообщение отправлено
        await message.answer("✅ Ваше сообщение было передано сотруднику. Ожидайте ответа.")

    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")
        await message.answer("❌ Произошла ошибка при отправке сообщения. Попробуйте позже.")


# Обработчик сообщений от администратора (ответы пользователям)
@dp.message(lambda message: message.from_user.id == ADMIN_ID and message.reply_to_message)
async def admin_reply(message: types.Message):
    try:
        # Извлекаем ID пользователя из текста сообщения
        reply_text = message.reply_to_message.text
        lines = reply_text.split('\n')
        user_id_line = [line for line in lines if '🆔 ID:' in line][0]
        user_id = int(user_id_line.split(': ')[1])

        # Отправляем ответ пользователю
        await bot.send_message(user_id, f"📩 Ответ от сотрудника:\n\n{message.text}")
        await message.answer("✅ Ответ отправлен пользователю.")

    except (IndexError, ValueError) as e:
        await message.answer("❌ Не удалось определить пользователя для ответа.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке ответа: {e}")


# Основная функция
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())