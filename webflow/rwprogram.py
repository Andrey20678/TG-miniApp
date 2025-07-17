import aiofiles, json
from settings import log
from webflow.client import webflow as wf

filename = "program.json"

async def read_prg(filename: str = filename):
    try:
        async with aiofiles.open(filename,"r") as f:
            data = await f.read()
            await f.close()
            return json.loads(data)
    except Exception as e:
        log.error(f"Failed to read file {e}")

async def write_prg(filename: str = filename):
    try:
        spk = await wf.get_speakers()
        if not spk:
            log.error("There is nothing to write to the file")
            return False
        async with aiofiles.open(filename,"w") as f:
            await f.write(json.dumps(spk))
            await f.close()
            return True
    except Exception as e:
        log.error(f"Failed to write file {e}")
