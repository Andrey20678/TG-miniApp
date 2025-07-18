import aiohttp.typedefs as types
import aiohttp.web_exceptions as ex
from config.settings import log, webflow_settings as ws, main_settings as ms
import aiohttp, asyncio
from typing import Union


class WebflowBase:
    headers_base = {
        "Authorization": f"Bearer {ws.api_key.get_secret_value()}",
        "Content-Type" : "application/json",
        }
    
    
    def responce_handler(self, accepted_status: list[int] = []) -> aiohttp.ClientResponse:
        def decorator(func):
            async def wrapper(*args, **kwargs):
                try:
                    res: aiohttp.ClientResponse = await func(*args, **kwargs)
                    if 200 <= res.status < 300 or res.status in accepted_status:
                        return res
                    else:
                        raise ex.HTTPException(f"Unexpected result received: {res.status}, {await res.text()}")
                except Exception as e:
                    log.error(f"Error: {str(e)}")
                    raise e
            return wrapper
        return decorator


class WebflowWebhooks(WebflowBase):
    wh_ids: list[str] = []
    wh_url = f"https://{ms.web_hook}/wf/wh"

    def retry(self, webhook_method: str, count: int = 3):
        def decorator(func):
            async def wrapper(*args, **kwargs):
                for _ in range(count):
                    try:
                        wh_id = await func(*args, **kwargs)
                        log.info(f"webhook {wh_id} {webhook_method} success")
                    except Exception:
                        log.info(f"failed to {webhook_method} webhook: retry")
                        await asyncio.sleep(2)
                        continue
                    return True
                raise ex.HTTPException(f"Error: failed to {webhook_method} webhook")
            return wrapper
        return decorator



    async def create_webhooks(self) -> None:
        async with aiohttp.ClientSession() as ss:
            url = f"https://api.webflow.com/v2/sites/{ws.site_id.get_secret_value()}/webhooks"
            headers = self.headers_base
            data = {"url": self.wh_url}
            trigger_types = [
                "collection_item_created",
                "collection_item_changed",
                "collection_item_deleted",
            ]

            @self.responce_handler()
            async def post(data):
                return await ss.post(url=url, headers=headers, json=data)

            @self.retry(webhook_method="set")
            async def create_webhook(trigger_type: str) -> None:
                data["triggerType"] = trigger_type
                res = await (await post(data)).json()
                wh_id = res.get("id")
                self.wh_ids.append(wh_id)
                return wh_id
            
            try:
                for trigger_type in trigger_types:
                    await create_webhook(trigger_type)
                await ss.close()
            except Exception as e:
                await ss.close()
                raise e
            
            

    async def remove_webhooks(self) -> None:
        if not self.wh_ids: return
        async with aiohttp.ClientSession() as ss:
            url = "https://api.webflow.com/v2/webhooks/"
            headers = self.headers_base

            @self.responce_handler(accepted_status=[404])
            async def delete(id: str):
                return await ss.delete(url=url+id, headers=headers)


            @self.retry(webhook_method="delete")
            async def delete_webhook(id: str) -> None:
                await delete(id)
                self.wh_ids.remove(id)
                return id
            
            try:
                ids = self.wh_ids.copy()
                for id in ids:
                    await delete_webhook(id)
                await ss.close()
            except Exception as e:
                await ss.close()
                raise e



    async def get_webhooks(self) -> list[str]:
        url = f"https://api.webflow.com/v2/sites/{ws.site_id.get_secret_value()}/webhooks"
        headers = self.headers_base
        async with aiohttp.ClientSession() as ss:

            @self.responce_handler()
            async def get():
                return await ss.get(url=url, headers=headers)

            data = await get()
            await ss.close()
            data = await data.json()
            if not data: return []
            whs = data.get("webhooks")
            res = []
            self.wh_ids = []
            for wh in whs:
                if wh.get("url") == self.wh_url:
                    res.append(wh)
                    self.wh_ids.append(wh.get("id"))
            log.info(f"Found {res.__len__()} existing webhooks")
            return res
        

class WebflowClient(WebflowBase):
    async def get_collection_items(self):
        url = f"https://api.webflow.com/v2/collections/{ws.collection_id.get_secret_value()}/items"
        async with aiohttp.ClientSession() as ss:

            @self.responce_handler()
            async def get():
                return await ss.get(url=url, headers=self.headers_base)

            data = await (await get()).json()
            await ss.close()
            if not data: return
            items = data.get("items")
            res = []
            for item in items:
                if item.get("isDraft") or item.get("isArchived"): continue
                res.append(item)
            return res