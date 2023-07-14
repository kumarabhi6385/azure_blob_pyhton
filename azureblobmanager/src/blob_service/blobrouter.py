#################### import section ################################################
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.append(str(HERE / '..'))


from fastapi import APIRouter,HTTPException,File,UploadFile
from fastapi.responses import Response

import json
import logging

#logging.basicConfig(level=logging.DEBUG, filename="output.log")
logging.basicConfig(level=logging.DEBUG)


from dependencies import Configuration
from blob_helper.manager_async import AzureBlobManager_async

#################### import section ################################################

router = APIRouter()

appConfig = Configuration()

################################# Get API ##########################################

@router.get("/blobs/list/")
async def blob_list():
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        data = await blobmanager.get_blob_list()
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
    finally:
        return json.dumps(data)
    
@router.get("/blobs/{blob_name}/info/")
async def get_blob_info(blob_name: str):
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        blob_properties = await blobmanager.get_blob_info(blob_name)
        return {
                 "name": blob_properties.name,
                 "container": blob_properties.container,
                 "blob_type": blob_properties.blob_type,
                 "size": blob_properties.size,
                 "deleted": blob_properties.deleted,
                 "blob_tier": blob_properties.blob_tier,
                 "tags": blob_properties.tags,
                 "has_legal_hold": blob_properties.has_legal_hold,
                 "has_versions_only": blob_properties.has_versions_only,
               }
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise HTTPException(status_code=500, detail="can not get blob info")
    
@router.get("/blobs/{blob_name}/blocks/")
async def get_blob_blocks(blob_name: str):
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        blocks = await blobmanager.get_blob_block_async(blob_name)
        return blocks
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise HTTPException(status_code=500, detail="can not get blocks detail")
    
################################# Get API ##########################################

################################# Delete API ##########################################

@router.delete("/blobs/all/")
async def delete_blobs_all():
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        await blobmanager.delete_all_blobs()
        return {"message": "Blobs are deleted"}
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise HTTPException(status_code=500, detail="can not delete")
    

@router.delete("/blobs/{blob_name}")
async def delete_blob(blob_name: str):
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        await blobmanager.delete_blob_async(blob_name)
        return {"message": "Blob is deleted"}
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise HTTPException(status_code=500, detail="can not delete")


################################# Delete API ##########################################

################################# Upload API ##########################################

@router.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    try:
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        await blobmanager.uploadFileData_async(file) 
        return {"filename": file.filename, "message": "File is uploaded"}
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise HTTPException(status_code=500, detail="can not delete")


################################# Upload API ##########################################

################################# Download API ##########################################

@router.get("/download/{blob_name}")
async def download_blob_async(blob_name: str):
    try:
        logging.debug(f"download_blob_async is called")
        blobmanager = AzureBlobManager_async(appConfig.account_url, appConfig.sastoken)
        file = await blobmanager.download_blob(blob_name)
        headers = {'Content-Disposition': f'attachment; filename="{blob_name}"'}
        return Response(file, headers=headers, media_type='application/pdf')
    except Exception as err:
        logging.exception(f"Exception details  - {err}")
        raise HTTPException(status_code=500, detail="can not downloaded")   

################################# Download API ##########################################