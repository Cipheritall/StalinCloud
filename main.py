import os
import Google
import logging
import db
from config import CONFIG
import files
import argparse
import api


if __name__ == "__main__":
    # Configure the logging module
    logging.basicConfig(filename="log/main.log", level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description="StalinCloud v0.1")
    # Add command-line arguments
    parser.add_argument("--sync", help="Number of new assets to sync")
    parser.add_argument("--xx", help="xx")
    # Add more arguments as needed
    parser.add_argument("--move", action="store_true", help="Move files to a new directory defined in config.yml [media_path]")

    args = parser.parse_args()

    if int(args.sync)>1:
        db.create_photos_database()
        service = Google.Create_Service()
        Google.sync_photos(service,target_num=int(args.sync))

    if args.move:
        api.move_all_photos()