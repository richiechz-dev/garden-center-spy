import json
from datetime import UTC, datetime
from typing import Any, override

import requests

from extractors.base import Extractor
from models import Product


class HomeDepot(Extractor):
    @override
    def fetch(self) -> dict[str, Any]:
        headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "es-419,es;q=0.9",
        }

        response = requests.get(self.url, headers)

        response.raise_for_status()
        return response.json()

    @override
    def parse(self, raw_data: dict[str, Any]) -> list[Product]:
        products_raw = raw_data.get("contents", [])
        products = []

        for item in products_raw:
            offer_price = None
            for price in item.get("price", []):
                if price.get("usage") == "Offer":
                    offer_price = price["value"]
                    break
            if offer_price is None:
                continue

            seo_href = item.get("seo", {}).get("href")
            sku = item.get("partNumber")

            if seo_href and sku:
                product_url = f"https://www.homedepot.com.mx{seo_href}"
                image_url = f"https://cdn.homedepot.com.mx/productos/{sku}/{sku}.jpg"
            else:
                product_url = None
                image_url = None

            product = Product(
                name=item.get("name", "Desconocido"),
                sku=item.get("partNumber", "Desconocido"),
                price=float(offer_price),
                store="Home Depot MX",
                description=item.get("shortDescription", "Sin Descripción"),
                image_url=image_url,
                product_url=product_url,
                scraped_at=datetime.now(UTC),
            )

            products.append(product)

        return products


home_depot = HomeDepot(
    "https://www.homedepot.com.mx/search/resources/api/v2/products?storeId=10351&searchTerm=kwPlantasComestibles&limit=28&offset=0&contractId=4000000000000000003&currency=MXN&langId=-5&marketId=21&stLocId=12605&extendedCatalog=false&marketOnly=true&physicalStoreId=8702&profileName=HCL_V2_findProductsBySearchTermWithPrice&selectedFacets=%5Bobject+Object%5D&minPrice=-1&maxPrice=-1&selectedPageOffset=0&orderBy=0"
)

if __name__ == "__main__":
    json_data = json.dumps(home_depot.fetch(), indent=4, ensure_ascii=False)
    print(json_data)

    products = home_depot.run()
    print(products)
