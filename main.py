from _create_check_and_replace.check_folder import check_products_file, check_price_and_quantity_file
from _create_check_and_replace.check_and_replace import check_and_replace_file
from _create_check_and_replace.create_confirmation_file import create_confirmation_file
from _data.get_data_from_products import get_and_check_products_data
from _data.get_all_products import get_all_products
from _data.get_price_and_quantity import get_prices_and_quantity_lists
from _data.send_products import send_products
from _data.send_quantities import send_quantities
from _reports.reports_config import ReportR
from _reports.logging_config import logger
import os
import sys

from dotenv import load_dotenv
load_dotenv()

def main():
    # report = ReportR()

    LOCK_FILE = os.environ.get('LOCK_FILE')
    if os.path.exists(LOCK_FILE):
        logger.error("Script is already running.")
        sys.exit()


    try:
        open(LOCK_FILE, 'w').close()
             
        price_and_quantity_filename = check_price_and_quantity_file() # add report
        products_filename = check_products_file()
        prises_and_quantity_dict = {}


        if price_and_quantity_filename:
            prises_and_quantity_dict = get_prices_and_quantity_lists(price_and_quantity_filename)
                
        
        if products_filename:      
            sku_set = get_all_products() # add report        
            products_list = get_and_check_products_data(products_filename, sku_set, prises_and_quantity_dict) # add report
            send_products(products_list)
            check_and_replace_file(products_filename)
            create_confirmation_file(products_filename)
        
        
        if price_and_quantity_filename:          
            send_quantities(prises_and_quantity_dict) #add report
            check_and_replace_file(price_and_quantity_filename)
            create_confirmation_file(price_and_quantity_filename)

    except Exception as e:
        logger.error(f"Uncaught error: {e}", exc_info=True)

    finally:
        # report.final()
        os.remove(LOCK_FILE)








if __name__ == "__main__":
        # Every 15 min? 
        main()