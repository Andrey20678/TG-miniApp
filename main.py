from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from bot.bot import bot_start, bot_stop
from bot.webhook import hook as hook_ma

from settings import log, main_settings as ms
from webflow.client import webflow as wf
from webflow.webhook import hook as hook_wf
from webflow.rwprogram import write_prg

@asynccontextmanager
async def lifespan(app: FastAPI):
     await bot_start()
     #await wf.create_webhook()
     await write_prg()
     yield
     #await wf.remove_webhook()
     await bot_stop()

app = FastAPI(lifespan=lifespan)

app.include_router(hook_ma)
app.include_router(hook_wf)

# origins = [
#      "http://localhost:*",
#      "http://127.0.0.1:*",
# ]
# 
# app.add_middleware(
#      CORSMiddleware,
#      allow_origins=origins,
#      allow_credentials=True,
#      allow_methods=["*"],
#      allow_headers=["*"],
#      )

if __name__=="__main__":
     uvicorn.run("main:app",port=ms.port)