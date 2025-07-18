from fastapi import APIRouter,Request,HTTPException,status
from config.settings import log
from webflow.rwprogram import read_file, write_file

hook = APIRouter(
    prefix="/wf",
    tags=["Webflow"])


@hook.get("/speakers")
async def webflow_get_speakers(request: Request):
    res = await read_file()
    if not res:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read data")
    return res


@hook.post("/wh")
async def webflow_webhook(request: Request):
    if not (request.headers.get("x-webflow-signature") and request.headers.get("x-webflow-timestamp")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        data = await request.json()
        payload = data.get("payload")
        if not payload or payload.get("isDraft") or payload.get("isArchived"): return
        await write_file()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    

    

    

