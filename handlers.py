from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from db import add_user
from stickers import PETTING_STICKER

router = Router()

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Погладить свинку")]],
        resize_keyboard=True,
        persistent=True
    )
    return keyboard

@router.message(Command("start"))
async def cmd_start(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    await add_user(user_id, chat_id)
    await message.answer(
        "Привет! Я бот благословений от свинки.\n\nКаждое утро я буду присылать тебе благословение.\nВ любой момент ты можешь погладить свинку с помощью кнопки внизу 🐖✨",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "Погладить свинку")
async def handle_pet_pig(message: Message):
    await message.answer_sticker(PETTING_STICKER)



