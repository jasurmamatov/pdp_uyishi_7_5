import asyncio
import logging
import sys
from aiogram import F
from os import getenv
import os
from aiogram import Bot, Dispatcher, Router, BaseMiddleware
from aiogram.filters import Filter
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message,InlineQuery, InlineQueryResultArticle,InlineQueryResultsButton, InlineQueryResultDocument, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from aiogram.fsm.state import State , StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import encode_payload
from aiogram.types import InlineQueryResultPhoto
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.utils.keyboard import  InlineKeyboardBuilder
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import FSMI18nMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
import logging
load_dotenv('.env')
TOKEN = os.getenv("TOKEN")
storage = RedisStorage(Redis())
dp = Dispatcher(storage=storage)



@dp.message()
async def message_handler(message: Message):
    ikm = InlineKeyboardBuilder()
    ikm.row(
        InlineKeyboardButton(text="uzb" , callback_data='lang_uz'),
        InlineKeyboardButton(text="Eng" , callback_data='lang_en'),
        InlineKeyboardButton(text="Rus" , callback_data='lang_ru')
        
        
    )
    await message.answer(_("Tilni tanlang"), reply_markup=ikm.as_markup() )

@dp.callback_query(F.data.startswith('lang_'))
async def lang_change_handler(callback_data:CallbackQuery, state:FSMContext):
    lang = callback_data.data.removeprefix('lang_')
    await state.update_data(locale = lang)
    await callback_data.answer(_("{} tanlandi".format(lang)))   
    await callback_data.answer()
    await callback_data.message.answer(_("Salom Python"))
    
    
    
@dp.message()
async def any_msg_handler(message:Message):
    await message.answer(_("Xush kelibsiz"))
    
 # -----------------------------------------------------------------------------

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))  
    i18n = I18n(path = "locales", default_locale = "en", domain = "messages")
    dp.update.outer_middleware.register(
    FSMI18nMiddleware(i18n)
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

"""
mkdir locales
pybabel extract --input-dirs=. -o locales/messages.pot 
pybabel init -i locales/messages.pot -d locales -l en
pybabel init -i locales/messages.pot -d locales -l uz

pybabel compile -d locales
pybabel update -d locales -i locales/messages.pot
"""
# class IsJoinedChannel(Filter):
#     def __init__(self, channel_id):
#         self.channel_id = channel_id
#         super().__init__()
        
#     async def __call__(self, message:Message, bot : Bot):
#         chat_member = await bot.get_chat_member(self.channel_id, message.from_user.id)
#         return chat_member.status not in (ChatMemberStatus.CREATOR, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER)



