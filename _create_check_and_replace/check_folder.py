import os
import re
from dotenv import load_dotenv
from _reports.logging_config import logger
load_dotenv()

folder_path = os.environ.get('FILES_PATH')

def check_products_file():
    pattern = re.compile(r'artykuly_\d+\.xml')

    files = os.listdir(folder_path)
    for file in files:
        if pattern.match(file):
            logger.info(f'A file "Artykuły" has been found: {file}')
            return file
    return False


def check_price_and_quantity_file():
    pattern = re.compile(r'ceny_stany_\d+\.xml')

    files = os.listdir(folder_path)
    for file in files:
        if pattern.match(file):
            logger.info(f'A file "ceny_stany" has been found: {file}')
            return file
    return False