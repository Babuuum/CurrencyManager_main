import os

from aiogram import Dispatcher, Bot
from dotenv import load_dotenv

from app.bot.handlers import router
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from app.utils.logger import logger

load_dotenv()

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(os.getenv('tg_bot_webhook_url'))

def main():
    bot = Bot(token=os.getenv('tg_bot_token'))
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    app = web.Application()

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")

    setup_application(app, dp, bot=bot)
    web.run_app(app, host="127.0.0.1", port=os.getenv('tg_bot_port'))

    if __name__ == "__main__":
        try:
            logger.info('Запуск бота!')
            main()
        except KeyboardInterrupt:
            logger.info('Бот отключен!')