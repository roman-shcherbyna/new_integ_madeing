import os
import json

from _reports.logging_config import logger
from _data.utils_data import parse_xml_file
from dotenv import load_dotenv
load_dotenv()



def get_and_check_products_data(products_filename, sku_set, price_and_quantity_filename={}):

    product_root = parse_xml_file(products_filename)

    products = product_root.findall(".//art")


    products_list = []
    for art in products:
        sku = art.find("kat").text
        name = art.find("nazwa").text

        if not sku:
            logger.error("The product has no SKU")

        if not name:
            logger.error(f"The product has no name. SKU: {sku}")


        price = price_and_quantity_filename.get(sku, {}).get('price')

        res = {
                'product': {
                    'sku': sku,
                }
            }
        
        if sku not in sku_set:
            res['product']['name'] = name
            res['product']['attribute_set_id'] = 4
            res['product']['visibility'] = 1
            res['product']['status'] = 2

            if price is not None:
                res['product']['price'] = int(price)

            logger.info(f'New product! {sku},  price: {price}')
            # report.add_data(sku, entry_type='new')
            products_list.append(res)

        else:
            if price is not None:
                res['product']['price'] = int(price)
                logger.debug(f'Update product {sku}: name: {name}, price: {price}')
                # report.add_data(sku, entry_type='new')
                products_list.append(res)
        
        

    with open('products_list.json', 'w', encoding='utf-8') as f:
        json.dump(products_list, f, ensure_ascii=False, indent=4)

    return products_list


