from pydantic_settings import BaseSettings, SettingsConfigDict, JsonConfigSettingsSource
from pydantic.types import SecretStr
from pydantic import BaseModel
import json
from typing import Optional

import logging as log
log.basicConfig(level=log.INFO, format="%(asctime)s - %(levelname)s:\t%(message)s")

class Button(BaseModel):
    text: str
    url : Optional[str]

class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config/bot.env", env_file_encoding="utf-8")
    
    bot_token   : SecretStr
    admin_id    : Optional[SecretStr]
    secret_key  : SecretStr = SecretStr("SetSecretKeyImmediatelyInConfig")
    meeting_text: str = "meeting_text"
    help_text   : str = "help_text"
    buttons     : list[list[Button]]

    def load(self = None):
        return BotSettings.model_validate(json.load(open("config/bot.json","r",encoding="utf-8")))
    def reload(self):
        self.__dict__ = self.load().__dict__

bot_settings = BotSettings.load()


class WebflowSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/webflow.env",
        env_file_encoding="utf-8")
    
    api_key       : SecretStr
    collection_id : SecretStr
    site_id       : SecretStr

webflow_settings = WebflowSettings()


class MainSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="config/main.env",
        env_file_encoding="utf-8")
    
    port: int
    web_hook: str

main_settings = MainSettings()