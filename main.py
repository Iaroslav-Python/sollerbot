import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv
from aiohttp import web

# Веб-сервер для пинга (аптайм)
async def handle_ping(request):
    return web.Response(text="✅ I'm alive!")

async def start_web_app():
    PORT = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"✅ Web ping server started on port {PORT}")
    while True:
        await asyncio.sleep(3600)  # чтобы сервер не завершался

# Загрузка токена из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set in .env")

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

PRICE_USD = 0.02
CRYPTO_LINK = "https://t.me/send?start=IVeBVwQXkTyH"
SUPPORT_CHAT = "https://t.me/soller_support"
ADMIN_CONTACT = "@fixdbk"
REVIEWS_LINK = "https://t.me/starsbyusd/4"

def get_start_keyboard() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🚀 Купить звезду", url=CRYPTO_LINK)
    kb.button(text="💬 Поддержка", url=SUPPORT_CHAT)
    kb.adjust(1, 1)
    return kb.as_markup()

@dp.message(Command(commands=["start"]))
async def cmd_start(message: types.Message):
    text = (
        f"🌌 <b>Добро пожаловать в StarDrop!</b>\n\n"
        f"⭐ <i>Здесь ты можешь купить свою звезду всего за ≈ ${PRICE_USD} — навсегда ✨</i>\n\n"
        f"🧮 <i>Чтобы посчитать сумму, просто пришли мне число — количество звёзд (от 100).</i>\n\n"
        f"🔐 <b>Оплата:</b> в криптовалюте через @CryptoBot\n"
        f"🎁 <b>Поддержка:</b> в личные сообщения @soller_support\n"
        f"🤔 <b>Не выплатили звезды в течение 3 часов?</b> Пишите администратору {ADMIN_CONTACT}\n"
        f"💬 <b>Отзывы:</b> <a href=\"{REVIEWS_LINK}\">смотреть</a>"
    )
    await message.answer(text, reply_markup=get_start_keyboard())

@dp.message()
async def calculate_total(message: types.Message):
    text = message.text.strip()
    if text.isdigit() and int(text) > 0:
        qty = int(text)
        total_usd = qty * PRICE_USD
        reply = (
            f"💫 Вы выбрали <b>{qty}</b> {'звезду' if qty == 1 else 'звёзд'}.\n"
            f"💰 Общая сумма: <b>${total_usd:.2f}</b>\n\n"
            f"🚀 Чтобы оплатить, перейдите по ссылке:\n"
            f"{CRYPTO_LINK}"
        )
        await message.answer(reply)

async def main():
    await asyncio.gather(
        start_web_app(),
        dp.start_polling(bot)
    )

if name == "__main__":
    asyncio.run(main())
