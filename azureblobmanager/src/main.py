############################################################################################

# just run below command
# python main.py -m api
#          or
# python main.py -m console

############################################################################################

import argparse
import subprocess
import logging

#logging.basicConfig(level=logging.DEBUG, filename="output.log")
logging.basicConfig(level=logging.DEBUG)

from config import Configuration

config = Configuration()

def run_uvicorn():
    uvicorn_command = f"uvicorn blob_service.root:app --host localhost --port {config.port}"
    print(uvicorn_command)
    #uvicorn_command = "uvicorn blob_service.root:app"
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
