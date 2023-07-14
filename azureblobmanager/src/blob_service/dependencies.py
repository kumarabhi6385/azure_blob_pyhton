import json
import logging

class Configuration():
    def __init__(self):
        self.loadConfiguration()

    def loadConfiguration(self):
        try:
            import os
            import os 
            cdir = os.getcwd() 
            pdir = os.path.dirname(cdir)
            filePath = pdir + "\config.json"
            print("filePath: ", filePath)

            with open(filePath) as file:
                config = json.load(file)
                blob_credential = config["azure_storage_account"]
                self.maxfilesize = blob_credential["maxfilesize"]
                self.account_url = blob_credential["account_url"]
                self.sastoken = blob_credential["token"]
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)    