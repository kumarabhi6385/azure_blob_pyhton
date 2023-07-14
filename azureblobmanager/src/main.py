############################################################################################

# just run below command
# python main.py -m api
#          or
# python main.py -m console

############################################################################################

import argparse
import subprocess
import logging
import os
import json

#logging.basicConfig(level=logging.DEBUG, filename="output.log")
logging.basicConfig(level=logging.DEBUG)

def getPort():
    with open("config.json") as file:
        data = json.load(file)
        return data["port"]

def run_uvicorn():
    port = getPort()
    os.chdir(f"blob_service")
    uvicorn_command = f"uvicorn root:app --host localhost --port {port}"
    subprocess.run(uvicorn_command, shell=True)

def run_console():
    command = "python blob_console/run.py"
    subprocess.run(command, shell=True)

# Create an argument parser object
parser = argparse.ArgumentParser(description='My Python script')

# Define custom arguments
parser.add_argument('-m', '--mode', type=str, help='Specify a name. Either type api or console')

# Parse the command-line arguments
args = parser.parse_args()

if args.mode.lower() == "api":
    print("Api mode")
    run_uvicorn()
elif args.mode.lower() == "console":
    print("console mode")
    run_console()
else:
    print("Wrong argument. Plz try again")
    exit()
