from aiogram.types import Update
from fastapi import APIRouter,Request,HTTPException,status
from bot.bot import bot,dp
from settings import log

hook = APIRouter(
    prefix="",
    tags=["Webhook MiniApp"])

#Заметка: накатить валидацию
@hook.post("/whma")
async def webhook_miniapp(req: Request):
    try: data = Update.model_validate(await req.json(), context={"bot": bot})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))
    await dp.feed_update(bot, data)