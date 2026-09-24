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

        limit = 28
        offset = 0
        all_contents = []

        # Primera llamada (offset=0) — obtenemos también el total
        url = self.url.replace("offset=0", f"offset={offset}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        all_contents.extend(data.get("contents", []))
        total = data.get("total", 0)
        breadcrumb = data.get("breadCrumbTrailEntryView", [])
        offset += limit

        # Páginas siguientes, mientras falten productos
        while offset < total:
            url = self.url.replace("offset=0", f"offset={offset}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            all_contents.extend(data.get("contents", []))
            offset += limit

        unique_contents = {}

        for item in all_contents:
            sku = item.get("partNumber")
            unique_contents[sku] = item

        return {
            "contents": list(unique_contents.values()),
            "breadcrumb": breadcrumb,
        }

    @override
    def parse(self, raw_data: dict[str, Any]) -> list[Product]:
        products_raw = raw_data.get("contents", [])
        breadcrumb = raw_data.get("breadcrumb", [])
        products = []

        # La categoría viene en el breadcrumb de nivel superior de la respuesta
        category = None
        if breadcrumb:
            category = breadcrumb[-1].get("label")

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

            attrs = {
                attr.get("identifier"): (attr.get("values") or [{}])[0].get("value")
                for attr in item.get("attributes", [])
            }

            product = Product(
                name=item.get("name", "Desconocido"),
                sku=item.get("partNumber", "Desconocido"),
                price=float(offer_price),
                store="Home Depot MX",
                description=item.get("shortDescription", "Sin Descripción"),
                image_url=image_url,
                product_url=product_url,
                scientific_name=attrs.get("NOMBRECIENTIFICO"),
                category=category or attrs.get("TIPO"),
                measurement=(
                    attrs.get("CAPACIDAD/TAMAÑO")
                    or attrs.get("DIÁMETRO")
                    or attrs.get("ALTO")
                ),
                scraped_at=datetime.now(UTC),
            )

            products.append(product)

        return products
