from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.exceptions import TelegramRetryAfter

from config.settings import log, bot_settings as bs, main_settings as ms

wh_url = f"https://{ms.web_hook}/whma"

bot = Bot(
    token=bs.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def send_message_to_admin(text: str, echo: bool = True) -> bool:
    if bs.admin_id:
        if echo: log.info(f"Message \"{text}\" sent to admin")
        try:
            await bot.send_message(
                chat_id=bs.admin_id.get_secret_value(),
                text=text)
        except Exception as e:
            log.error(f"Failed to send message to admin, {str(e)}")
            return False
    return True


async def bot_start() -> None:
    log.info("Starting bot...")
    try:
        if (await bot.get_webhook_info()).url:
            try:
                await bot.delete_webhook()
                log.info("Webhook removed")
            except Exception as e:
                log.error(f"Failed to remove existing webhook, {str(e)}")
                await send_message_to_admin(f"Failed to remove existing webhook, {str(e)}", echo=False)

        await bot.set_webhook(
            url                  = wh_url,
            allowed_updates      = dp.resolve_used_update_types(),
            drop_pending_updates = True,
            secret_token         = bs.secret_key.get_secret_value(),
            )
        log.info(f"Webhook set to {wh_url}")
        log.info("Bot started successfully")
        await send_message_to_admin("Bot started")
    except Exception as e:
        log.error(f"Failed to set webhook, {str(e)}")
        await send_message_to_admin(f"Failed to set webhook, {str(e)}", echo=False)
        raise e
    

async def bot_stop() -> None:
    log.info("Shutting down bot...")

    try:
        await bot.delete_webhook()
        log.info("Webhook removed")
    except Exception as e:
        log.error(f"Failed to remove webhook, {str(e)}")
        await send_message_to_admin(f"Failed to remove webhook, {str(e)}", echo=False)

    try:
        await send_message_to_admin("Bot stopped")
        await bot.close()
        log.info("Bot stopped successfully")
    except TelegramRetryAfter as e:
        log.error(e)
        await send_message_to_admin(str(e), echo=False)
        raise e




def reply_build() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=
        [[InlineKeyboardButton(text=bs.button_text, web_app=WebAppInfo(url=bs.button_url))]]
        )
reply = reply_build()

@dp.message(CommandStart(ignore_case=True))
async def cmd_start(message: Message):
    await message.answer(text=bs.meeting_text, reply_markup=reply)
    

@dp.message(Command("help",ignore_case=True))
async def cmd_help(message: Message):
    await message.answer(text=bs.help_text)


@dp.message(Command("reloadcfg"))
async def admin_cmd_reload(message: Message):
    if message.from_user.id == int(bs.admin_id.get_secret_value()):
        bs.reload()
        global reply
        reply = reply_build()
        log.info("Config reloaded")
        await message.answer(text="reloaded")
    await cmd_start(message)


@dp.message()
async def other(message: Message):
    await cmd_start(message)