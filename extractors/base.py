from abc import ABC, abstractmethod


class Extractor(ABC):
    def __init__(self, url) -> None:
        self.url = url

    @abstractmethod
    def fetch(self):
        # Metodo abastracto, aqui sin implementacion. Cada hija lo define
        pass

    @abstractmethod
    def parse(self, raw_data):
        # Metodo abastracto, aqui sin implementacion. Cada hija lo define
        pass

    def run(self):
        raw_data = self.fetch()
        products = self.parse(raw_data)

        return products
