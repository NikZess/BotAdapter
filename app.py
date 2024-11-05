import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommandScopeAllPrivateChats

from common.bot_cmds_list import private

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'))

ALLOWED_UPDATES = ['message, edited_message']

dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет!🖐 Для того, чтобы (что будет пользователю), сначала подпишись выполни условия: ")
    await message.answer("Подпишись на (ссылка на канал)")                                     
    
@dp.message(Command("check"))
async def check_cmd(message: types.Message):
    user_id = message.from_user.id

    try:
        user_status = await bot.get_chat_member(chat_id=-1002167897714, user_id=user_id)

        if user_status.status in ['member', 'administrator', 'creator']:
            await message.reply("Условия выполнены!")
            # Что будет пользователю за выполнение условий
        else:
            await message.reply("Вы не подписаны на канал.")
            await message.answer("Подпишитесь на канал (ссылка на канал)")
    except Exception as e:
        await message.reply(f"Произошла ошибка: {str(e)}")
        # Ошибка сервера
    
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())