import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.append(str(HERE / '..'))

import logging
#logging.basicConfig(level=logging.DEBUG, filename="output.log")
logging.basicConfig(level=logging.DEBUG)

import asyncio
from config import Configuration
from blob_helper.manager_async import AzureBlobManager_async

appConfig = Configuration()

async def getListOfBlobsAsync():
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        data = await blobmanager.get_blob_list()
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise Exception(err)
    finally:
        return data
 

async def main():
    data = await getListOfBlobsAsync()
    logging.info(data)

if __name__ == '__main__':
    asyncio.run(main())