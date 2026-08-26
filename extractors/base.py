from abc import ABC, abstractmethod
from typing import Any

from models import Product


class Extractor(ABC):
    def __init__(self, url: str) -> None:
        self.url = url

    @abstractmethod
    def fetch(self) -> dict[str, Any]:
        # Metodo abastracto, aqui sin implementacion. Cada hija lo define
        pass

    @abstractmethod
    def parse(self, raw_data: dict[str, Any]) -> list[Product]:
        # Metodo abastracto, aqui sin implementacion. Cada hija lo define
        pass

    def run(self) -> list[Product]:
        raw_data = self.fetch()
        products = self.parse(raw_data)

        return products
