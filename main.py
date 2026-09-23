import os
import sys

from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, Timeout
from sqlalchemy.exc import SQLAlchemyError

from extractors.home_depot import HomeDepot
from extractors.ikea import Ikea
from load.load import load_products

load_dotenv()


def main():
    api_url = os.getenv("HOME_DEPOT_API_URL")
    if not api_url:
        print("Error: HOME_DEPOT_API_URL no está configurada en .env")
        sys.exit(1)

    ikea_url = os.getenv("IKEA_API_URL")
    ikea_category = os.getenv("IKEA_CATEGORY")
    if not ikea_url or not ikea_category:
        print("Error: IKEA_API_URL / IKEA_CATEGORY no están configuradas en .env")
        sys.exit(1)

    try:
        home_depot = HomeDepot(api_url)
        products = home_depot.run()

        ikea = Ikea(ikea_url, category=ikea_category)
        products += ikea.run()
    except (ConnectionError, Timeout) as e:
        print(f"Error de conexión con la API: {e}")
        sys.exit(1)
    except HTTPError as e:
        print(f"Error HTTP de la API: {e}")
        sys.exit(1)

    try:
        load_products(products)
    except SQLAlchemyError as e:
        print(f"Error al cargar en la BD: {e}")
        sys.exit(1)

    print(f"Se han cargado {len(products)} productos")


if __name__ == "__main__":
    main()
