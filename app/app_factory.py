import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from aiogram.types import Update

from app.bot.bot import bot, dp

from dotenv import load_dotenv
from app.scheduler.scheduler_runner import main
from starlette.middleware.sessions import SessionMiddleware
from app.admin import admin

load_dotenv()


def create_app() -> FastAPI:
    app = FastAPI(title="Crypto Asset Manager")
    app.add_middleware(SessionMiddleware, secret_key="supersecretkey")
    app.include_router(admin.router)

    WEBHOOK_PATH = f"/webhook/{os.getenv('TG_BOT_TOKEN')}"
    BASE_URL = os.getenv("BASE_URL")
    WEBHOOK_URL = BASE_URL + WEBHOOK_PATH

    @app.get("/ping", summary="Healthcheck")
    def ping():
        return JSONResponse(content={"status": "ok"})

    @app.post(WEBHOOK_PATH)
    async def telegram_webhook(request: Request):
        data = await request.json()
        update = Update(**data)
        await dp.feed_webhook_update(bot, update)
        return {"ok": True}

    @app.on_event("startup")
    async def on_startup():
        await bot.set_webhook(
            WEBHOOK_URL,
            allowed_updates=["message", "callback_query"]
        )
        await main()

    @app.on_event("shutdown")
    async def on_shutdown():
        await bot.session.close()

    return app
