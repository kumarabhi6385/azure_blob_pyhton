#################### import section ################################################
from azure.storage.blob import BlobBlock
from azure.storage.blob.aio import ContainerClient
import logging
import uuid
import time

#################### import section ################################################

class AzureBlobManager_async():
    def __init__(self, url, sas):
        self.account_url = url
        self.sastoken = sas

     # Below function will be be used to list of blobs
    async def get_blob_list(self):
        blob_list = []
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            # async for blob in container.list_blob_names():
            #     blob_list.append(blob)
            #blobs = container.list_blob_names().by_page()
            blob_list = [b async for b in container.list_blob_names()]
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()
            logging.debug(f"Received blobs {blob_list}")
            return blob_list
            
        
    # Below function will be be used to get specific blob information
    async def get_blob_info(self, blobname:str):
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            blob_client = container.get_blob_client(blobname)
            properties = await blob_client.get_blob_properties()
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()
            return properties

    # Below function will be be used to get blocks info of blob    
    async def get_blob_blocks(self, blobname:str):
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            blob_client = container.get_blob_client(blobname)
            blocklist = await blob_client.get_block_list()
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()
            return blocklist
        
    # Below function will be be used to delete list of blobs
    async def delete_all_blobs(self):
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            blob_list = [b async for b in container.list_blob_names()]
            await container.delete_blobs(*blob_list)
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()

    # Below function will be be used to delete the blob
    async def delete_blob(self, blobname:str):
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            blobs = [blobname]
            await container.delete_blobs(*blobs)
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()

    # Below function will be be used to upload file using file object
    async def upload_file_in_chunks(self,local_file_path:str, blob_file_path:str, chunk_size:int = 1024*1024*4):
        '''
        Upload large file to blob
        '''

        try:
            container = ContainerClient.from_container_url(
                    container_url=self.account_url,
                    credential=self.sastoken,
                )
            blob_client = container.get_blob_client(blob_file_path)
            # upload data
            block_list=[]
            with open(local_file_path,'rb') as f:
                while True:
                    read_data = f.read(chunk_size)
                    if not read_data:
                        break # done
                    blk_id = str(uuid.uuid4())
                    await blob_client.stage_block(block_id=blk_id,data=read_data) 
                    block_list.append(BlobBlock(block_id=blk_id))
                    logging.debug(f"{blk_id} appended")
                    time.sleep(5)
            await blob_client.commit_block_list(block_list)
            logging.debug('Upload file completed')
        except BaseException as err:
            logging.exception('Upload file error')
            logging.exception(err)

    # Below function will be be used to upload file using file object
    async def uploadFile(self, file):
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            blobname = str(uuid.uuid4())
            extension = ".pdf"
            name = blobname + extension
            await container.upload_blob(name=name, data=file, overwrite=True)
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()


    # Below function will be be used to download blob
    async def download_blob(self, blobname:str):
        try:
            container = ContainerClient.from_container_url(
                container_url=self.account_url,
                credential=self.sastoken,
            )
            stream = await container.download_blob(blobname)
            data = await stream.readall()
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)
        finally:
            await container.close()
            return data
     
    
      