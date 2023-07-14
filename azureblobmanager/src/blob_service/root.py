#################### import section ################################################
from fastapi import FastAPI

import logging

#logging.basicConfig(level=logging.DEBUG, filename="output.log")
logging.basicConfig(level=logging.DEBUG)

from blobrouter import router as blob_router 

#################### import section ################################################


app = FastAPI()

@app.get("/")
async def get_root():
    return "Welcome to File service built on Fast API"

app.include_router(blob_router)
