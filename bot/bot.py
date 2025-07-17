from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.exceptions import TelegramRetryAfter

import settings
from settings import log, bot_settings as bs, main_settings as ms

wh_url = f"https://{ms.web_hook}/whma"

bot = Bot(
    token=bs.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def send_message_to_admin(text:str):
    if bs.admin_id:
        log.info(f"Message \"{text}\" sent to admin")
        try:
            await bot.send_message(
                chat_id=bs.admin_id.get_secret_value(),
                text=text)
        except Exception as e:
            log.error(f"Failed to send message to admin, {str(e)}")


async def bot_start():
    log.info("Starting bot...")
    try:
        if (await bot.get_webhook_info()).url:
            try:
                await bot.delete_webhook()
                log.info("Webhook removed")
            except Exception as e:
                log.error(f"Failed to remove existing webhook, {str(e)}")
                await send_message_to_admin(f"Failed to remove existing webhook, {str(e)}")

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
        await send_message_to_admin(f"Failed to set webhook, {str(e)}")
    

async def bot_stop():
    log.info("Shutting down bot...")

    try:
        await bot.delete_webhook()
        log.info("Webhook removed")
    except Exception as e:
        log.error(f"Failed to remove webhook, {str(e)}")
        await send_message_to_admin(f"Failed to remove webhook, {str(e)}")

    try:
        await bot.close()
        log.info("Bot stopped successfully")
        await send_message_to_admin("Bot stopped successfully")
    except TelegramRetryAfter as e:
        log.error(e)
        await send_message_to_admin(str(e))


def reply_build(buttons_list: list[list[settings.Button]]):
    keyboard = []
    for line in buttons_list:
        buttons = []
        for button in line:
            buttons.append(InlineKeyboardButton(
                text=button.text,
                web_app=WebAppInfo(url=f"https://{button.url}")))
        keyboard.append(buttons)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@dp.message(CommandStart(ignore_case=True))
async def cmd_start(message: Message):
    await message.answer(text=bs.meeting_text, reply_markup=reply_build(bs.buttons))
    

@dp.message(Command("help",ignore_case=True))
async def cmd_help(message: Message):
    await message.answer(text=bs.help_text)


@dp.message(Command("reloadcfg"))
async def admin_cmd_reload(message: Message):
    if message.from_user.id == int(bs.admin_id.get_secret_value()):
        bs.reload()
        log.info("Config reloaded")
        await message.answer(text="reloaded")
    await cmd_start(message)


@dp.message()
async def other(message: Message):
    await cmd_start(message)