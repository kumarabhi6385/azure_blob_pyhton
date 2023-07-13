import json
import logging

class Configuration():
    def __init__(self):
        self.loadConfiguration()

    def loadConfiguration(self):
        try:
            with open("config.json") as file:
                config = json.load(file)
                blob_credential = config["azure_storage_account"]
                self.maxfilesize = blob_credential["maxfilesize"]
                self.account_url = blob_credential["account_url"]
                self.sastoken = blob_credential["token"]
                self.port = config["port"]
        except Exception as err:
            logging.exception(f"Exception details  - {err}")
            raise Exception(err)    