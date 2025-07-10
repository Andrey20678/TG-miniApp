from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic.types import SecretStr
import dotenv,os
from typing import Optional

import logging as log
log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s:\t%(message)s")

class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/bot.env",
        env_file_encoding="utf-8",
        )

    bot_token   : SecretStr
    web_hook    : str
    button_url  : str
    admin_id    : Optional[SecretStr]
    meeting_text: str = "meeting_text"
    button_text : str = "button_text"
    help_text   : str = "help_text"

    def reload(self):
        os.environ.update(dotenv.dotenv_values(dotenv_path="config/bot.env)"))
        self.__init__()

bot_settings = BotSettings()


class WebflowSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/webflow.env",
        env_file_encoding="utf-8")
    
    api_key       : SecretStr
    collection_id : SecretStr

webflow_settings = WebflowSettings()