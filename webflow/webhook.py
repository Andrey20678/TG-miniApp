from fastapi import APIRouter,Request,HTTPException,status
from settings import log
from webflow.rwprogram import read_prg, write_prg

hook = APIRouter(
    prefix="/wf",
    tags=["Webflow"])


@hook.get("/speakers")
async def webhook_webflow(request: Request):
    return await read_prg()


@hook.post("/wh")
async def webhook_webflow(request: Request):
    if not request.headers.get("x-webflow-signature"): raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        data = await request.json()
        payload = data.get("payload")
        if not payload or payload.get("isDraft") or payload.get("isArchived"): return
        write_prg()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

    

    

