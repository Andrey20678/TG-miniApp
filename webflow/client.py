import aiohttp.web_exceptions
from settings import log, webflow_settings as ws, main_settings as ms
import aiohttp, asyncio

wh_url = f"https://{ms.web_hook}/wf/wh"


class WebFlow:
    wh_ids: list[str] = []

    headers_base = {
        "Authorization": f"Bearer {ws.api_key.get_secret_value()}",
        "Content-Type" : "application/json",
        }

    async def create_webhook(self):
        async with aiohttp.ClientSession() as ss:
            url = f"https://api.webflow.com/v2/sites/{ws.site_id.get_secret_value()}/webhooks"
            headers = self.headers_base
            data = {
                "url": wh_url,
                "triggerType": "collection_item_created"
                }
            async def post(data):
                async with ss.post(url=url, headers=headers, json=data) as res:
                    if 200 <= res.status < 300:
                        return await res.json()
                    else:
                        log.error(f"Error: {res.status}, {await res.text()}")
                        raise aiohttp.web_exceptions.HTTPException(f"Error: {res.status}, {await res.text()}")
            
            async def retry(data):
                for _ in range(3):
                    try:
                        wh = (await post(data)).get("id")
                        log.info(f"Webhook id {wh} was set")
                        self.wh_ids.append(wh)
                    except Exception:
                        log.info("failed to set webhook: retry")
                        await asyncio.sleep(2)
                        continue
                    return True
                raise aiohttp.web_exceptions.HTTPException("Error: failed to set webhook")
            
            await retry(data)

            data["triggerType"] = "collection_item_changed"
            await retry(data)

            data["triggerType"] = "collection_item_deleted"
            await retry(data)
            


    async def remove_webhook(self):
        async with aiohttp.ClientSession() as ss:
            url = "https://api.webflow.com/v2/webhooks/"
            async def delete(id):
                async with ss.delete(url=url+id, headers=self.headers_base) as res:
                    if 200 <= res.status < 300 or res.status == 404:
                        return
                    else:
                        log.error(f"Error: {res.status}, {await res.text()}")
                        raise aiohttp.web_exceptions.HTTPException(f"Error: {res.status}, {await res.text()}")
            
            async def retry(id):
                for _ in range(3):
                    try:
                        await delete(url+id)
                        log.info(f"Webhook id {id} was delete")
                    except Exception:
                        log.info(f"failed to delete webhook {id}: retry")
                        await asyncio.sleep(2)
                        continue
                    return True
                raise aiohttp.web_exceptions.HTTPException(f"Error: failed to delete webhook {id}")

            for id in self.wh_ids: await retry(id)
            self.wh_ids = []
    

    async def session_get(self, url, headers, session: aiohttp.ClientSession):
        try:
            async with session.get(url, headers=headers) as res:
                if 200 <= res.status < 300:
                    return await res.json()
                else:
                    log.error(f"Error: {res.status}, {await res.text()}")
        except Exception as e:
            log.error(f"Error: {str(e)}")

    
    async def get_speakers(self):
        headers = self.headers_base
        url = f"https://api.webflow.com/v2/collections/{ws.collection_id.get_secret_value()}/items"

        async with aiohttp.ClientSession() as ss:
            data = await self.session_get(url, headers, ss)
            await ss.close()
        if not data: return
        items = data.get("items")
        res = []
        for item in items:
            if item.get("isDraft") or item.get("isArchived"): continue
            res.append(item)
        return res

webflow = WebFlow()