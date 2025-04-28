import os
import json
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
load_dotenv()


def parse_xml_file(file_name):
    file_path = os.path.join(os.getenv("FILES_PATH"), file_name)
    return ET.parse(file_path).getroot()



def get_batches_for_products(new_products_list, batch_size):
    products_batches = []
    for i in range(0, len(new_products_list), batch_size):
        batch = new_products_list[i:i + batch_size]
        products_batches.append(batch)
    return products_batches



def get_batches_for_quantity(quantity_list, batch_size):
    batched_result = []
    for i in range(0, len(quantity_list), batch_size):
        batch = quantity_list[i : i + batch_size]
        source_items = [
            {
                "sku": item["sku"],
                "source_code": item["source_code"],
                "quantity": int(item["quantity"]),
                "status": int(item["status"]),
            }
            for item in batch
        ]
        batched_result.append([
            {"sourceItems": source_items}
        ])
    with open('get_batches_for_quantity.json', 'w', encoding='utf-8') as f:
        json.dump(batched_result, f, ensure_ascii=False, indent=4)
    return batched_result
