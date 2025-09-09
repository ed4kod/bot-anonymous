from aiogram import types, Dispatcher
from aiogram.filters import Command
from config import ADMIN_ID


def register_handlers(dp: Dispatcher):
    """Регистрирует все обработчики в диспетчере"""
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(admin_reply, lambda message: message.from_user.id == ADMIN_ID and message.reply_to_message)
    dp.message.register(forward_to_admin)


# Остальные функции обработчиков остаются без изменений
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Здравствуйте! Я бот-помощник. Опишите вашу проблему или вопрос, и я передам его сотруднику.")


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
            await message.bot.send_message(ADMIN_ID, f"{user_info}\n💬 Сообщение: {message.text}")
        elif message.photo:
            await message.bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=user_info)
        elif message.document:
            await message.bot.send_document(ADMIN_ID, message.document.file_id, caption=user_info)

        # Подтверждаем пользователю, что сообщение отправлено
        await message.answer("✅ Ваше сообщение было передано сотруднику. Ожидайте ответа.")

    except Exception as e:
        print(f"Ошибка при пересылке сообщения: {e}")
        await message.answer("❌ Произошла ошибка при отправке сообщения. Попробуйте позже.")


async def admin_reply(message: types.Message):
    try:
        # Извлекаем ID пользователя из текста сообщения
        reply_text = message.reply_to_message.text
        lines = reply_text.split('\n')
        user_id_line = [line for line in lines if '🆔 ID:' in line][0]
        user_id = int(user_id_line.split(': ')[1])

        # Отправляем ответ пользователю
        await message.bot.send_message(user_id, f"📩 Ответ от сотрудника:\n\n{message.text}")
        await message.answer("✅ Ответ отправлен пользователю.")

    except (IndexError, ValueError) as e:
        await message.answer("❌ Не удалось определить пользователя для ответа.")
    except Exception as e:
        await message.answer(f"❌ Ошибка при отправке ответа: {e}")
