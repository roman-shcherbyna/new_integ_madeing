from _reports.logging_config import logger
import requests
import os
import json
from _data.utils_data import get_batches_for_products
import itertools

headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer " + os.environ.get("TOKEN"),}


def send_prices(prises_and_quantity_dict):
    formatted = [
        {
            "product": {
                "sku": sku,
                "price": int(details["price"])
            }
        }
        for sku, details in prises_and_quantity_dict.items()
    ]

    batches = get_batches_for_products(formatted, int(os.getenv("BATCH_SIZE")))

    with open("batches.json", "w", encoding="utf-8") as f:
        json.dump(batches, f, ensure_ascii=False, indent=4)
        print("Батчи сохранены в batches.json")

    for i, batch in enumerate(batches, start=1):

        payload = batch   # или то, что вы там реально собираете
        print(">>> PRODUCTS-JSON:", json.dumps(payload, ensure_ascii=False, indent=4))

        logger.info(f"Sending batch with price. Nr: {i}")
        response = requests.post(
            url=os.getenv("BASE_URL") + os.getenv("END_POINT_UPDATE"),
            json=batch,
            headers=headers,
        )
        if response.status_code not in (200, 202):
            logger.error(
                f"Error {response.status_code} on batch #{i}: {response.text}",
                exc_info=True
            )