from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from bot.bot import bot_start, bot_stop
from bot.webhook import hook as hook_ma

from config.settings import log, main_settings as ms
from webflow.endpoints import hook as hook_wf
from webflow.rwprogram import write_file
from webflow.client import WebflowWebhooks

@asynccontextmanager
async def lifespan(app: FastAPI):
     wf = WebflowWebhooks()
     try:
          await bot_start()
     except Exception as e:
          await bot_stop()
          raise e
     try:
          await wf.get_webhooks()
          await wf.remove_webhooks()
          await wf.create_webhooks()
     except Exception as e:
          await wf.remove_webhooks()
          await bot_stop()
          raise e
     await write_file()
     yield
     try: await wf.remove_webhooks()
     except Exception: pass
     try: await bot_stop()
     except Exception: pass

app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

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