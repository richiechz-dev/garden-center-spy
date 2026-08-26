import os
import sys

from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, Timeout
from sqlalchemy.exc import SQLAlchemyError

from extractors.home_depot import HomeDepot
from load.load import load_products

load_dotenv()


def main():
    api_url = os.getenv("HOME_DEPOT_API_URL")
    if not api_url:
        print("Error: HOME_DEPOT_API_URL no está configurada en .env")
        sys.exit(1)

    try:
        home_depot = HomeDepot(api_url)
        products = home_depot.run()
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
