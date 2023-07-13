from fastapi import FastAPI,HTTPException,File,UploadFile
from fastapi.responses import Response

import json
import logging

#logging.basicConfig(level=logging.DEBUG, filename="output.log")
logging.basicConfig(level=logging.DEBUG)

from config import Configuration
from blob_helper.manager_async import AzureBlobManager_async

config = Configuration()

app = FastAPI()

@app.get("/")
async def get_root():
    return "Welcome to File service built on Fast API"

@app.get("/blobs/")
async def blob_list():
    try:
        logging.debug(config.account_url)
        logging.debug(config.sastoken)
        blobmanager = AzureBlobManager_async(config.account_url, config.sastoken)
        data = await blobmanager.get_blob_list()
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
    finally:
        return json.dumps(data)

