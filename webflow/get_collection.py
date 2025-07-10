from settings import log,webflow_settings as ws
import aiohttp

async def get_webflow_collection_items():
    headers = {
        "Authorization": f"Bearer {ws.api_key.get_secret_value()}",
        "accept-version": "1.0.0"
    }
    url = f"https://api.webflow.com/v2/collections/{ws.collection_id.get_secret_value()}/items"

    async with aiohttp.ClientSession() as ss:
        try:
            async with ss.get(url, headers=headers) as res:
                if res.status == 200:
                    data = await res.json()
                    items = data.get("items", [])
                    log.info(f"Got collection items {items}")
                    return str(items).replace("<"," ").replace(">"," ")
                else:
                    log.error(f"Error: {res.status}, {await res.text()}")
                    
        except Exception as e:
            log.error(f"Error: {str(e)}")