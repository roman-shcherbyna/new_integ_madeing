import os
import json

from _reports.logging_config import logger
from _data.utils_data import parse_xml_file
from dotenv import load_dotenv
load_dotenv()



def get_prices_and_quantity_lists(price_and_quantity_filename): #add report

    price_root = parse_xml_file(price_and_quantity_filename)

    prices = price_root.findall(".//art")


    prises_and_quantity_dict = {}

    for art in prices:
        sku = art.attrib.get("idx")
        quantity = art.find("s").text
        price =  art.find("ca/c").attrib.get("b") if art.find("ca/c") is not None else None

        if not quantity:
            logger.error(f"The product has no quantity. SKU: {sku}")

        if not price:
            logger.error(f"The product has no price. SKU: {sku}")

        prises_and_quantity_dict[sku] = {}
        prises_and_quantity_dict[sku]["price"] = price
        prises_and_quantity_dict[sku]["quantity"] = quantity
        

    with open('prises_and_quantity_dict.json', 'w', encoding='utf-8') as f:
        json.dump(prises_and_quantity_dict, f, ensure_ascii=False, indent=4)

    return prises_and_quantity_dict


