from extractors.base import Extractor


class TiendaFalsa(Extractor):
    def fetch(self):
        return {
            "contents": [{"id": 1, "nombre_producto": "Yerbabuena", "precio_raw": "150.00"}]
        }

    def parse(self, raw_data):
        products = []

        for item in raw_data.get("contents", []):
            products.append(
                {
                    "name": item["nombre_producto"],
                    "price": float(item["precio_raw"]),
                }
            )

        return products


tienda = TiendaFalsa("http://url-prueba.com")
productos = tienda.run()
print(productos)
