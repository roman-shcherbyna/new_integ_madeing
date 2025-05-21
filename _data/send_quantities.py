from _reports.logging_config import logger
from _data.utils_data import get_batches_for_quantity
import requests
import os
import json

from dotenv import load_dotenv
load_dotenv()

def send_batches_for_quantities(quantity_list):
    headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer " + os.environ.get("TOKEN")}
    
    batches = get_batches_for_quantity(quantity_list, int(os.getenv("BATCH_SIZE")))


    for i, batch in enumerate(batches, start=1):
        logger.debug(f"Sending a batch with quantity Nr: {i}")
        
        with open("one_batch_with_quantity.json", "w", encoding="utf-8") as f:
            json.dump(batch, f, ensure_ascii=False, indent=4)

        response = requests.post(
            url=os.getenv("BASE_URL") + os.getenv("END_POINT_ADD_STOCK"),
            json=batch,
            headers=headers,
        )

        print(f'url ={os.getenv("BASE_URL") + os.getenv("END_POINT_ADD_STOCK")}, headers = {headers}')

        if response.status_code not in (200, 202):
            logger.error(f"Error {response.status_code}: {response.text}", exc_info=True)


def send_quantities(prises_and_quantity_dict):
    quantity_list = []

    for sku, value in prises_and_quantity_dict.items():

        quantity = value.get('quantity')
        temp_dict = {
                "sku": sku,
                "source_code": "default",
                "quantity": quantity,
                "status": 1,
            }
        
        quantity_list.append(temp_dict)
        logger.debug(f"Update quantity: SKU: {sku}, quantity: {quantity}")



    with open('quantity_list_to_send.json', 'w', encoding='utf-8') as f:
        json.dump(quantity_list, f, ensure_ascii=False, indent=4)

    send_batches_for_quantities(quantity_list)

    logger.info(f"Stany zostały zaktualizowane")
