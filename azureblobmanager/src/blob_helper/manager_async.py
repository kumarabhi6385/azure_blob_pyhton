from azure.storage.blob.aio import ContainerClient
import logging

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
