import os
import shutil
import logging

# Configure the logging module
logger = logging.getLogger(__name__)

def delete_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        logger.info(f"Folder deleted: {folder_path}")
    except FileNotFoundError:
        logger.warning(f"Folder not found: {folder_path}")
    except PermissionError:
        logger.error(f"Permission denied to delete folder: {folder_path}")

def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
        logger.info(f"Folder created: {folder_path}")
    except FileExistsError:
        logger.warning(f"Folder already exists: {folder_path}")

def folder_exists(folder_path):
    return os.path.exists(folder_path) and os.path.isdir(folder_path)

def create_folder_if_not_exist(folder_path):
    if not folder_exists(folder_path):
        create_folder(folder_path)

def move_file(source_path, destination_path):
    try:
        shutil.move(source_path, destination_path)
        logger.info(f"File moved from {source_path} to {destination_path}")
    except FileNotFoundError:
        logger.warning(f"File not found: {source_path}")
    except PermissionError:
        logger.error(f"Permission denied to move file: {source_path}")

def file_exists(file_path):
    return os.path.exists(file_path)