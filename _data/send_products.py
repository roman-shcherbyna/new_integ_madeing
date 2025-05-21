from _reports.logging_config import logger
import requests
import os
import json
from _data.utils_data import get_batches_for_products

headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer " + os.environ.get("TOKEN"),}

def send_products(products_list):
    batches = get_batches_for_products(products_list, int(os.getenv("BATCH_SIZE")))

    with open("batches_with_products.json", "w", encoding="utf-8") as f:
        json.dump(batches, f, ensure_ascii=False, indent=4)
        print("Batches saved in batches_with_products.json")

    for i, batch in enumerate(batches, start=1):
        logger.info(f"Sending a batch with new products. Nr: {i}")
        response = requests.post(
            url=os.getenv("BASE_URL") + os.getenv("END_POINT_UPDATE"),
            json=batch,
            headers=headers,
        )

        if response.status_code not in (200, 202):
            logger.error(f"Error {response.status_code}: {response.text}", exc_info=True)


