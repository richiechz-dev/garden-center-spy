import json
from datetime import UTC, datetime
from typing import Any, override
from uuid import uuid4

import requests

from extractors.base import Extractor
from models import Product


class Ikea(Extractor):
    def __init__(self, url: str, category: str) -> None:
        super().__init__(url)
        self.category = category

    @override
    def fetch(self) -> dict[str, Any]:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,es-MX;q=0.8,es;q=0.7",
            "content-type": "text/plain;charset=UTF-8",
            "origin": "https://www.ikea.com",
            "referer": "https://www.ikea.com/",
            "session-id": str(uuid4()),
        }

        window_size = 24
        offset = 0
        total = None
        all_items = []

        while True:
            payload = {
                "searchParameters": {"input": self.category, "type": "CATEGORY"},
                "isUserLoggedIn": False,
                "isB2B": False,
                "listingABTest": True,
                "components": [
                    {
                        "component": "PRIMARY_AREA",
                        "columns": 4,
                        "types": {"main": "PRODUCT", "breakouts": ["PLANNER", "MATTRESS_WARRANTY"]},
                        "filterConfig": {"max-num-filters": 7},
                        "window": {"size": window_size, "offset": offset},
                        "allVariants": False,
                        "forceFilterCalculation": True,
                    }
                ],
            }

            response = requests.post(self.url, data=json.dumps(payload), headers=headers)
            response.raise_for_status()
            data = response.json()

            items = []
            for result in data.get("results", []):
                items.extend(result.get("items", []))

                if total is None:
                    metadata = result.get("metadata") or {}
                    total = metadata.get("itemsPerType", {}).get("PRODUCT")

            all_items.extend(items)
            offset += window_size

            if total is not None:
                if offset >= total:
                    break
            elif len(items) < window_size:
                break

        # Deduplica productos que aparezcan en más de un area
        unique_items = {}
        for item in all_items:
            product = item.get("product") or {}
            sku = product.get("itemNo") or product.get("id")
            if sku:
                unique_items[sku] = item

        return {"items": list(unique_items.values())}

    @override
    def parse(self, raw_data: dict[str, Any]) -> list[Product]:
        products = []

        for item in raw_data.get("items", []):
            if item.get("type") != "PRODUCT":
                continue

            product = item.get("product") or {}
            sales_price = product.get("salesPrice") or {}
            price = sales_price.get("numeral")
            if price is None:
                continue

            type_name = product.get("typeName")
            measurement = product.get("itemMeasureReferenceText")
            if type_name and measurement:
                description = f"{type_name}, {measurement}"
            else:
                description = type_name or measurement

            products.append(
                Product(
                    name=product.get("name", "Desconocido"),
                    sku=product.get("itemNo") or product.get("id", "Desconocido"),
                    price=float(price),
                    currency=sales_price.get("currencyCode", "MXN"),
                    store="IKEA",
                    description=description,
                    image_url=product.get("mainImageUrl"),
                    product_url=product.get("pipUrl"),
                    scraped_at=datetime.now(UTC),
                )
            )

        return products