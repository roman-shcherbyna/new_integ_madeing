from _reports.logging_config import logger
import requests
import os
import json
from _data.utils_data import get_batches_for_products

headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer " + os.environ.get("TOKEN"),}

def send_products(products_list):
    batches = get_batches_for_products(products_list, int(os.getenv("BATCH_SIZE")))

    for i, batch in enumerate(batches, start=1):
        logger.info(f"Sending a batch with new products. Nr: {i}")
        response = requests.post(
            url=os.getenv("BASE_URL") + os.getenv("END_POINT_UPDATE"),
            data=json.dumps(batch, ensure_ascii=False),
            headers=headers,
        )

        if response.status_code not in (200, 202):
            logger.error(f"Error {response.status_code}: {response.text}", exc_info=True)


