from aiogram.types import Update
from fastapi import APIRouter,Request,HTTPException,status
from bot.bot import bot,dp
from settings import log, bot_settings as bs

hook = APIRouter(
    prefix="/whma",
    tags=["Webhook MiniApp"])

@hook.post("")
async def webhook_miniapp(req: Request):
    if req.headers.get("x-telegram-bot-api-secret-token") != bs.secret_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nope"
        )
    try: data = Update.model_validate(await req.json(), context={"bot": bot})
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    await dp.feed_update(bot, data)