#!/usr/bin/env python3

import argparse

from slapdash.app import app
from main_path import main_path





#######################################################
#This section is what is needed for the logging setup.
#######################################################
import logging
import logging.handlers
import os
from pathlib import Path
import datetime


#This gets the datestamp in the format: 'YYYY_MM_DD'
today = '{0:%Y_%m_%d}'.format(datetime.datetime.now())

#This checks if the logs folder already exists in the diretory.
#The number of '../' needs to bring it outside of the GitHub repository.
#If the folder already exists, continues on.
#If the folder does not already exist, it will create that folder then move on.
my_folder = Path(f"{main_path}/logs/")
if my_folder.is_dir():
    print('Folder already exists')
else:
    os.system(f'mkdir {main_path}/logs/')
    print('Folder Created')

#This sets up the basic logging operation.
app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s, MSS_App, %(levelname)s, %(message)s',
                              "%Y-%m-%d %H:%M:%S")

#This sets up the logging that will be sent to the file for the current date.
file_handler = logging.handlers.TimedRotatingFileHandler(f'{main_path}/logs/mss_app.log', when="midnight")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

#This sets up the logging that will be displayed on the terminal screen.
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

#This activates each of the handliers in the program.
app.logger.addHandler(file_handler)
app.logger.addHandler(stream_handler)

#######################################################
#######################################################





def argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", metavar="PORT", default=5008, type=int)
    parser.add_argument("--host", metavar="HOST", default="0.0.0.0")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--processes", metavar="PROCESSES", type=int, default=1)
    parser.add_argument("--threaded", action="store_true")
    return parser


def main():
    args = argparser().parse_args()
    app.run_server(
        port=args.port,
        debug=args.debug,
        host=args.host,
        processes=args.processes,
        threaded=args.threaded,
    )


if __name__ == "__main__":
    main()
