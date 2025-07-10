from fastapi import APIRouter,Request,HTTPException,status
from settings import log
from schemas.webflow import WebflowPayload

hook = APIRouter(
    prefix="",
    tags=["Webhook Webflow"])

async def webflow_validate(req: Request):
    pass

#Заметка: накатить валидацию
@hook.post("/whwf")
async def webhook_webflow(req: Request):
    try: data = WebflowPayload(**await req.json())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e))

    print(data)
    
    

