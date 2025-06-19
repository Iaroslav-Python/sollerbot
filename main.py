import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from helpers import send_ton_transfer_placeholder

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

LANGUAGES = {"ru": "Русский", "en": "English"}

user_lang = {}

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for code, lang in LANGUAGES.items():
        keyboard.add(types.KeyboardButton(lang))
    await message.answer("Choose your language / Выберите язык:", reply_markup=keyboard)

@dp.message_handler(lambda msg: msg.text in LANGUAGES.values())
async def language_chosen(message: types.Message):
    lang_code = None
    for code, lang in LANGUAGES.items():
        if lang == message.text:
            lang_code = code
            break
    user_lang[message.from_user.id] = lang_code
    await message.answer(f"Language set to {LANGUAGES[lang_code]}. Welcome to NFT Market Bot!", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Use /sell to list a gift or /buy to see available gifts.")

@dp.message_handler(commands=["sell"])
async def sell_handler(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    await message.answer({
        "en": "Send me details of your NFT gift to sell (e.g. link or description).",
        "ru": "Пришлите детали вашего NFT подарка для продажи (ссылку или описание)."
    }[lang])

@dp.message_handler(commands=["buy"])
async def buy_handler(message: types.Message):
    lang = user_lang.get(message.from_user.id, "en")
    # Здесь выводим список подарков (пока заглушка)
    await message.answer({
        "en": "Available gifts: \n1. NFT Candle\n2. NFT Hat",
        "ru": "Доступные подарки: \n1. NFT Свеча\n2. NFT Шапка"
    }[lang])

@dp.message_handler(commands=["pay"])
async def pay_handler(message: types.Message):
    # Пример вызова функции отправки TON, здесь заглушка
    await send_ton_transfer_placeholder(message.from_user.id, 0.05)
    await message.answer("Payment sent! (placeholder)")

if __name__ == "__main__":
    print("Bot started...")
    executor.start_polling(dp, skip_updates=True)
