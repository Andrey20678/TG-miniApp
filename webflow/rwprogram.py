import aiofiles, json
from config.settings import log
from webflow.client import WebflowClient

wf_client = WebflowClient()
filename = "file.json"

async def read_file(filename: str = filename):
    try:
        async with aiofiles.open(filename,"r") as f:
            data = await f.read()
            await f.close()
            return json.loads(data)
    except Exception as e:
        log.error(f"Failed to read file {e}")


async def write_file(filename: str = filename) -> bool:
    try:
        spk = await wf_client.get_collection_items()
        if not spk:
            log.error("There is nothing to write to the file")
            return False
        async with aiofiles.open(filename,"w") as f:
            await f.write(json.dumps(spk))
            await f.close()
            return True
    except Exception as e:
        log.error(f"Failed to write to the file {e}")
    return False
